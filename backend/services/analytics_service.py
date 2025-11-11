from typing import Dict, Any, List
from sqlalchemy.orm import Session
from quizzes import models as quiz_models
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime, timedelta
from collections import defaultdict


def _mastery_level(acc: float) -> str:
    if acc >= 85:
        return "Mastered"
    if acc >= 70:
        return "Proficient"
    if acc >= 50:
        return "Developing"
    return "Needs Practice"


def compute_user_analytics(db: Session, user_id: int) -> Dict[str, Any]:
    attempts: List[quiz_models.QuizAttempt] = (
        db.query(quiz_models.QuizAttempt)
        .filter(quiz_models.QuizAttempt.user_id == user_id)
        .order_by(quiz_models.QuizAttempt.timestamp.asc())
        .all()
    )

    if not attempts:
        return {
            "has_data": False,
            "trend_slope": 0.0,
            "rolling_avg": 0.0,
            "volatility": 0.0,
            "best_categories": [],
            "weak_categories": [],
            "category_accuracy": {},
            "mastery_by_category": {},
            "attempts_count": 0,
            "last_accuracy": 0.0,
            "best_attempt": None,
            "worst_attempt": None,
            "improvement_pct_recent": 0.0,
            "consistency_score": 0.0,
            "target_next_accuracy": 0.0,
            "recommendations": [],
            "graphs": {
                "accuracy_trend": {"type": "line", "title": "Accuracy Trend Over Time", "data": [], "x_axis": "timestamp", "y_axis": "accuracy"},
                "category_performance": {"type": "bar", "title": "Performance by Category", "data": [], "x_axis": "category", "y_axis": "accuracy"},
                "score_distribution": {"type": "histogram", "title": "Score Distribution", "data": [], "x_axis": "range", "y_axis": "count"},
                "performance_heatmap": {"type": "heatmap", "title": "Performance Heatmap", "data": [], "x_axis": "week", "y_axis": "category", "value": "average_accuracy"},
                "improvement_velocity": {"type": "line", "title": "Improvement Velocity", "data": [], "x_axis": "to_date", "y_axis": "improvement_rate", "metrics": {"average_weekly_improvement": 0.0, "recent_velocity": 0.0}},
                "category_trends": {"type": "multi_line", "title": "Category Progress Over Time", "data": [], "x_axis": "timestamp", "y_axis": "accuracy"}
            },
            "performance_metrics": {
                "average_accuracy": 0.0,
                "median_accuracy": 0.0,
                "std_deviation": 0.0,
                "min_accuracy": 0.0,
                "max_accuracy": 0.0,
                "quartile_25": 0.0,
                "quartile_75": 0.0,
                "total_questions_answered": 0,
                "total_correct_answers": 0,
                "overall_accuracy": 0.0
            },
            "improvement_velocity_summary": {
                "average_weekly_improvement": 0.0,
                "recent_velocity": 0.0,
                "weekly_breakdown": []
            }
        }

    accuracies = np.array([a.accuracy for a in attempts], dtype=float)

    # Trend via linear regression
    x = np.arange(len(accuracies)).reshape(-1, 1)
    y = accuracies.reshape(-1, 1)
    try:
        model = LinearRegression().fit(x, y)
        slope = float(model.coef_[0][0])
    except Exception:
        slope = 0.0

    # Rolling average (last 10)
    N = min(10, len(accuracies))
    rolling_avg = float(np.mean(accuracies[-N:])) if N > 0 else 0.0

    # Volatility
    volatility = float(np.std(accuracies)) if len(accuracies) > 1 else 0.0

    # Last, best, worst
    last_accuracy = float(accuracies[-1])
    best_idx = int(np.argmax(accuracies))
    worst_idx = int(np.argmin(accuracies))
    best_attempt = attempts[best_idx]
    worst_attempt = attempts[worst_idx]

    # Improvement percentage over recent window vs previous window
    half = len(accuracies) // 2
    if half > 0:
        prev_mean = float(np.mean(accuracies[:half]))
        recent_mean = float(np.mean(accuracies[half:]))
        denom = prev_mean if prev_mean != 0 else 1.0
        improvement_pct_recent = float(((recent_mean - prev_mean) / denom) * 100.0)
    else:
        improvement_pct_recent = 0.0

    # Consistency score (inverse of volatility, normalized)
    # Normalize by typical max std ~ 35; clamp 0..100
    consistency_score = float(max(0.0, min(100.0, 100.0 - (volatility / 35.0) * 100.0)))

    # Category accuracy
    quiz_ids = list({a.quiz_id for a in attempts})
    quizzes = (
        db.query(quiz_models.Quiz)
        .filter(quiz_models.Quiz.id.in_(quiz_ids))
        .all()
    )
    id_to_cat = {q.id: (q.category or "Uncategorized") for q in quizzes}

    cat_stats: Dict[str, Dict[str, float]] = {}
    for a in attempts:
        cat = id_to_cat.get(a.quiz_id, "Uncategorized")
        stat = cat_stats.setdefault(cat, {"sum": 0.0, "n": 0})
        stat["sum"] += a.accuracy
        stat["n"] += 1

    category_accuracy = {k: (v["sum"] / v["n"]) for k, v in cat_stats.items() if v["n"] > 0}
    mastery_by_category = {k: _mastery_level(v) for k, v in category_accuracy.items()}

    # Rank categories
    items = sorted(category_accuracy.items(), key=lambda kv: kv[1], reverse=True)
    best_categories = [k for k, _ in items[:2]]
    weak_categories = [k for k, _ in items[-2:]]

    # Target next accuracy: small step improvement
    target_next_accuracy = float(min(100.0, max(last_accuracy + 5.0, rolling_avg + 2.0)))

    # Recommendations
    recommendations: List[str] = []
    for cat, acc in sorted(category_accuracy.items(), key=lambda kv: kv[1]):
        if acc < 60:
            recommendations.append(f"Practice {cat}: aim for +10% by reviewing mistakes and retaking targeted quizzes.")
        elif acc < 75:
            recommendations.append(f"Reinforce {cat}: short spaced repetition session to move towards proficiency.")
    if slope <= 0:
        recommendations.append("Your trend is flat/declining: try an easier quiz to rebuild momentum, then increase difficulty.")
    if consistency_score < 60:
        recommendations.append("Accuracy is volatile: slow down, review explanations, and focus on question types you miss.")

    # ===== GRAPH DATA FOR PERFORMANCE ANALYTICS =====
    
    # 1. Accuracy Trend Over Time (Line Chart)
    accuracy_trend = [
        {
            "timestamp": a.timestamp.isoformat(),
            "accuracy": float(a.accuracy),
            "score": a.score,
            "total": a.total,
            "quiz_id": a.quiz_id
        }
        for a in attempts
    ]
    
    # 2. Category Performance Comparison (Bar Chart)
    category_performance = [
        {
            "category": cat,
            "accuracy": float(acc),
            "attempts": cat_stats[cat]["n"],
            "mastery_level": mastery_by_category[cat]
        }
        for cat, acc in sorted(category_accuracy.items(), key=lambda x: x[1], reverse=True)
    ]
    
    # 3. Score Distribution (Histogram)
    score_ranges = {
        "0-20": 0, "21-40": 0, "41-60": 0, "61-80": 0, "81-100": 0
    }
    for a in attempts:
        acc = a.accuracy
        if acc <= 20:
            score_ranges["0-20"] += 1
        elif acc <= 40:
            score_ranges["21-40"] += 1
        elif acc <= 60:
            score_ranges["41-60"] += 1
        elif acc <= 80:
            score_ranges["61-80"] += 1
        else:
            score_ranges["81-100"] += 1
    
    score_distribution = [
        {"range": k, "count": v, "percentage": round((v / len(attempts)) * 100, 1) if attempts else 0}
        for k, v in score_ranges.items()
    ]
    
    # 4. Performance Heatmap (Category vs Time Periods)
    # Group attempts by week and category
    if attempts:
        first_date = min(a.timestamp for a in attempts)
        last_date = max(a.timestamp for a in attempts)
        weeks = []
        current = first_date
        while current <= last_date:
            weeks.append(current)
            current += timedelta(days=7)
        
        heatmap_data = defaultdict(lambda: defaultdict(int))
        heatmap_counts = defaultdict(lambda: defaultdict(int))
        
        for a in attempts:
            # Find which week this attempt belongs to
            week_idx = min(
                len(weeks) - 1,
                max(0, int((a.timestamp - first_date).days / 7))
            )
            week_label = weeks[week_idx].strftime("%Y-%m-%d")
            cat = id_to_cat.get(a.quiz_id, "Uncategorized")
            
            heatmap_data[cat][week_label] += a.accuracy
            heatmap_counts[cat][week_label] += 1
        
        # Calculate averages
        performance_heatmap = []
        for cat in category_accuracy.keys():
            for week_label in sorted(set(w for cat_data in heatmap_data.values() for w in cat_data.keys())):
                if heatmap_counts[cat][week_label] > 0:
                    avg_acc = heatmap_data[cat][week_label] / heatmap_counts[cat][week_label]
                    performance_heatmap.append({
                        "category": cat,
                        "week": week_label,
                        "average_accuracy": round(float(avg_acc), 1),
                        "attempts": heatmap_counts[cat][week_label]
                    })
    else:
        performance_heatmap = []
    
    # 5. Improvement Velocity (Rate of change over time)
    if len(attempts) >= 3:
        # Calculate improvement rate per week
        weekly_improvements = []
        for i in range(1, len(attempts)):
            days_diff = (attempts[i].timestamp - attempts[i-1].timestamp).days
            if days_diff > 0:
                acc_diff = attempts[i].accuracy - attempts[i-1].accuracy
                improvement_per_day = acc_diff / days_diff
                weekly_improvements.append({
                    "from_date": attempts[i-1].timestamp.isoformat(),
                    "to_date": attempts[i].timestamp.isoformat(),
                    "improvement_rate": round(float(improvement_per_day * 7), 2),  # per week
                    "accuracy_change": round(float(acc_diff), 1)
                })
        improvement_velocity = {
            "average_weekly_improvement": round(float(np.mean([w["improvement_rate"] for w in weekly_improvements])), 2) if weekly_improvements else 0.0,
            "recent_velocity": round(float(np.mean([w["improvement_rate"] for w in weekly_improvements[-3:]])), 2) if len(weekly_improvements) >= 3 else (weekly_improvements[-1]["improvement_rate"] if weekly_improvements else 0.0),
            "weekly_breakdown": weekly_improvements[-10:]  # Last 10 periods
        }
    else:
        improvement_velocity = {
            "average_weekly_improvement": 0.0,
            "recent_velocity": 0.0,
            "weekly_breakdown": []
        }
    
    # 6. Category Progress Over Time (Multi-line chart)
    category_progress = defaultdict(list)
    for a in attempts:
        cat = id_to_cat.get(a.quiz_id, "Uncategorized")
        category_progress[cat].append({
            "timestamp": a.timestamp.isoformat(),
            "accuracy": float(a.accuracy)
        })
    
    category_trends = [
        {
            "category": cat,
            "data_points": sorted(data, key=lambda x: x["timestamp"])
        }
        for cat, data in category_progress.items()
    ]
    
    # 7. Performance Metrics Summary
    performance_metrics = {
        "average_accuracy": round(float(np.mean(accuracies)), 2),
        "median_accuracy": round(float(np.median(accuracies)), 2),
        "std_deviation": round(float(np.std(accuracies)), 2),
        "min_accuracy": round(float(np.min(accuracies)), 2),
        "max_accuracy": round(float(np.max(accuracies)), 2),
        "quartile_25": round(float(np.percentile(accuracies, 25)), 2),
        "quartile_75": round(float(np.percentile(accuracies, 75)), 2),
        "total_questions_answered": sum(a.total for a in attempts),
        "total_correct_answers": sum(a.score for a in attempts),
        "overall_accuracy": round(float(sum(a.score for a in attempts) / sum(a.total for a in attempts) * 100), 2) if attempts else 0.0
    }
    
    return {
        "has_data": True,
        "trend_slope": slope,
        "rolling_avg": rolling_avg,
        "volatility": volatility,
        "best_categories": best_categories,
        "weak_categories": weak_categories,
        "category_accuracy": category_accuracy,
        "mastery_by_category": mastery_by_category,
        "attempts_count": len(attempts),
        "last_accuracy": last_accuracy,
        "best_attempt": {
            "quiz_id": best_attempt.quiz_id,
            "accuracy": float(best_attempt.accuracy),
            "timestamp": best_attempt.timestamp.isoformat(),
        },
        "worst_attempt": {
            "quiz_id": worst_attempt.quiz_id,
            "accuracy": float(worst_attempt.accuracy),
            "timestamp": worst_attempt.timestamp.isoformat(),
        },
        "improvement_pct_recent": improvement_pct_recent,
        "consistency_score": consistency_score,
        "target_next_accuracy": target_next_accuracy,
        "recommendations": recommendations,
        # ===== PERFORMANCE ANALYTICS WITH GRAPH DATA =====
        "graphs": {
            "accuracy_trend": {
                "type": "line",
                "title": "Accuracy Trend Over Time",
                "description": "Track your performance improvement across all quiz attempts",
                "data": accuracy_trend,
                "x_axis": "timestamp",
                "y_axis": "accuracy"
            },
            "category_performance": {
                "type": "bar",
                "title": "Performance by Category",
                "description": "Compare your accuracy across different ethical categories",
                "data": category_performance,
                "x_axis": "category",
                "y_axis": "accuracy"
            },
            "score_distribution": {
                "type": "histogram",
                "title": "Score Distribution",
                "description": "Distribution of your quiz scores across different accuracy ranges",
                "data": score_distribution,
                "x_axis": "range",
                "y_axis": "count"
            },
            "performance_heatmap": {
                "type": "heatmap",
                "title": "Performance Heatmap",
                "description": "Category performance over time periods (weekly view)",
                "data": performance_heatmap,
                "x_axis": "week",
                "y_axis": "category",
                "value": "average_accuracy"
            },
            "improvement_velocity": {
                "type": "line",
                "title": "Improvement Velocity",
                "description": "Rate of improvement over time (accuracy change per week)",
                "data": improvement_velocity.get("weekly_breakdown", []),
                "x_axis": "to_date",
                "y_axis": "improvement_rate",
                "metrics": {
                    "average_weekly_improvement": improvement_velocity.get("average_weekly_improvement", 0.0),
                    "recent_velocity": improvement_velocity.get("recent_velocity", 0.0)
                }
            },
            "category_trends": {
                "type": "multi_line",
                "title": "Category Progress Over Time",
                "description": "Track performance trends for each category separately",
                "data": category_trends,
                "x_axis": "timestamp",
                "y_axis": "accuracy"
            }
        },
        "performance_metrics": performance_metrics,
        "improvement_velocity_summary": improvement_velocity
    }

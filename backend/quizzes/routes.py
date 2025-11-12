from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from pydantic import BaseModel

from database import get_db
from auth.dependencies import get_current_active_user
from quizzes import services, models
from schemas import (
    Quiz, QuizCreate, QuizAttempt, UserCreate, QuizAttemptCreate,
    PostQuizAnalysis, AnswerExplanation, EthicalConflictExplanation, EthicalBiasProfile
)
from auth import models as auth_models
from services.explanation_service import explain_wrong_answer, explain_ethical_conflict

router = APIRouter()

class QuizSubmission(BaseModel):
    answers: Dict[str, str]  # {question_id: selected_answer}
    justifications: Dict[str, str] = {}  # {question_id: justification_text}

@router.post("", response_model=Quiz)
def create_new_quiz(quiz: QuizCreate, db: Session = Depends(get_db), current_user: UserCreate = Depends(get_current_active_user)):
    return services.create_quiz(db=db, quiz=quiz)

@router.get("", response_model=List[Quiz])
def read_quizzes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user: UserCreate = Depends(get_current_active_user)):
    quizzes = services.get_quizzes(db, skip=skip, limit=limit)
    return quizzes

@router.get("/{quiz_id}", response_model=Quiz)
def read_quiz(quiz_id: int, db: Session = Depends(get_db), current_user: UserCreate = Depends(get_current_active_user)):
    quiz = services.get_quiz(db, quiz_id=quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz

@router.post("/{quiz_id}/submit", response_model=QuizAttempt)
def submit_quiz_answers(
    quiz_id: int,
    submission: QuizSubmission,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_active_user)
):
    quiz = services.get_quiz(db, quiz_id=quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")

    quiz_attempt = QuizAttemptCreate(
        quiz_id=quiz_id,
        score=0,  # Will be calculated in record_quiz_attempt
        total=len(quiz.questions),
        accuracy=0.0
    )

    db_quiz_attempt = services.record_quiz_attempt(
        db=db,
        user_id=current_user.id,
        attempt=quiz_attempt,
        quiz=quiz,
        answers=submission.answers,
        justifications=submission.justifications
    )
    return db_quiz_attempt

@router.get("/{quiz_id}/explain-conflict/{question_id}", response_model=EthicalConflictExplanation)
def explain_question_conflict(
    quiz_id: int,
    question_id: int,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_active_user)
):
    """Get explanation for an ethical conflict in a specific question"""
    quiz = services.get_quiz(db, quiz_id=quiz_id)
    if quiz is None:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    # Find the question
    question_data = None
    for q in quiz.questions:
        if q.get("id") == question_id:
            question_data = q
            break
    
    if not question_data:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Generate explanation
    explanation_data = explain_ethical_conflict(
        question_text=question_data.get("question_text", ""),
        options=question_data.get("options", []),
        correct_answer=question_data.get("correct_answer")
    )
    
    return EthicalConflictExplanation(
        question_id=question_id,
        question_text=question_data.get("question_text", ""),
        options=question_data.get("options", []),
        pros_cons=explanation_data.get("pros_cons", {}),
        ethical_frameworks=explanation_data.get("ethical_frameworks", []),
        real_world_parallels=explanation_data.get("real_world_parallels", []),
        explanation=explanation_data.get("explanation", "")
    )

@router.get("/attempts/{attempt_id}/analysis", response_model=PostQuizAnalysis)
def get_post_quiz_analysis(
    attempt_id: int,
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_active_user)
):
    """Get detailed post-quiz analysis with explanations for wrong answers"""
    attempt = services.get_attempt_by_id(db, attempt_id, user_id=current_user.id)
    if not attempt:
        raise HTTPException(status_code=404, detail="Quiz attempt not found")
    
    quiz = services.get_quiz(db, attempt.quiz_id)
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    
    explanations = []
    answer_details = attempt.answer_details or {}
    
    # Generate explanations for each question
    for q_data in quiz.questions:
        question_id = str(q_data.get("id"))
        question_text = q_data.get("question_text", "")
        options = q_data.get("options", [])
        correct_answer = q_data.get("correct_answer", "")
        
        if question_id in answer_details:
            detail = answer_details[question_id]
            user_answer = detail.get("answer", "")
            justification = detail.get("justification", "")
            is_correct = detail.get("is_correct", False)
            
            if not is_correct:
                # Generate explanation for wrong answer
                explanation_data = explain_wrong_answer(
                    question_text=question_text,
                    options=options,
                    user_answer=user_answer,
                    correct_answer=correct_answer,
                    user_justification=justification
                )
                
                explanations.append(AnswerExplanation(
                    question_id=int(question_id),
                    user_answer=user_answer,
                    correct_answer=correct_answer,
                    is_correct=False,
                    explanation=explanation_data.get("explanation", ""),
                    ethical_frameworks=explanation_data.get("ethical_frameworks", []),
                    real_world_parallels=explanation_data.get("real_world_parallels", [])
                ))
            else:
                # For correct answers, provide a brief positive note
                explanations.append(AnswerExplanation(
                    question_id=int(question_id),
                    user_answer=user_answer,
                    correct_answer=correct_answer,
                    is_correct=True,
                    explanation="Great job! Your reasoning aligns with the ethical principles at play.",
                    ethical_frameworks=[],
                    real_world_parallels=[]
                ))
    
    # Generate overall feedback
    overall_feedback = f"You scored {attempt.score}/{attempt.total} ({attempt.accuracy:.1f}%). "
    if attempt.accuracy >= 80:
        overall_feedback += "Excellent work! You demonstrate strong ethical reasoning."
    elif attempt.accuracy >= 60:
        overall_feedback += "Good effort! Review the explanations to deepen your understanding."
    else:
        overall_feedback += "Keep learning! The explanations below will help you understand the ethical frameworks better."
    
    return PostQuizAnalysis(
        attempt_id=attempt_id,
        score=attempt.score,
        total=attempt.total,
        accuracy=attempt.accuracy,
        explanations=explanations,
        overall_feedback=overall_feedback
    )

@router.get("/ethical-bias-profile", response_model=EthicalBiasProfile)
def get_ethical_bias_profile(
    db: Session = Depends(get_db),
    current_user: auth_models.User = Depends(get_current_active_user),
    force_refresh: bool = Query(False, description="Force refresh of the profile")
):
    # Feature temporarily disabled
    raise HTTPException(status_code=404, detail="Ethical bias profile is temporarily disabled")

@router.get("/history")
def get_user_quiz_history(db: Session = Depends(get_db), current_user: auth_models.User = Depends(get_current_active_user)):
    attempts = services.get_user_quiz_attempts(db, user_id=current_user.id)
    # Serialize to plain JSON-safe dicts
    result = []
    for attempt in attempts:
        result.append({
            "id": attempt.id,
            "user_id": attempt.user_id,
            "quiz_id": attempt.quiz_id,
            "score": attempt.score,
            "total": attempt.total,
            "accuracy": float(attempt.accuracy) if attempt.accuracy is not None else 0.0,
            "timestamp": attempt.timestamp.isoformat() if attempt.timestamp else None,
            "answer_details": attempt.answer_details or {}
        })
    return result

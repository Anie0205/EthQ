from sqlalchemy.orm import Session
from typing import Dict, Any, Optional
from quizzes import models as quiz_models
from services.moral_reasoning_service import analyze_moral_reasoning_patterns
from quizzes import services as quiz_services


def get_or_compute_ethical_bias_profile(
    db: Session, 
    user_id: int, 
    force_refresh: bool = False
) -> quiz_models.EthicalBiasProfile:
    """
    Get cached ethical bias profile or compute it if missing/stale.
    Profile is refreshed if new justifications exist since last computation.
    """
    # Check for existing profile
    profile = (
        db.query(quiz_models.EthicalBiasProfile)
        .filter(quiz_models.EthicalBiasProfile.user_id == user_id)
        .first()
    )
    
    # Get all justifications for the user
    justifications = quiz_services.get_user_justifications(db, user_id=user_id)
    
    if not justifications:
        # No justifications - return default profile or None
        if profile:
            return profile
        return None
    
    # Get the latest justification ID
    latest_justification_id = max(j.id for j in justifications) if justifications else None
    
    # Check if we need to refresh
    needs_refresh = (
        force_refresh or
        profile is None or
        profile.last_justification_id is None or
        profile.last_justification_id < latest_justification_id
    )
    
    if not needs_refresh and profile:
        return profile
    
    # Compute new profile
    justification_data = [
        {
            "question_id": j.question_id,
            "justification_text": j.justification_text,
            "user_answer": j.user_answer,
            "is_correct": j.is_correct
        }
        for j in justifications
    ]
    
    analysis = analyze_moral_reasoning_patterns(justification_data)
    
    # Update or create profile
    if profile:
        profile.primary_framework = analysis.get("primary_framework", "Unknown")
        profile.secondary_frameworks = analysis.get("secondary_frameworks", [])
        profile.reasoning_patterns = analysis.get("reasoning_patterns", {})
        profile.summary = analysis.get("summary", "")
        profile.recommendations = analysis.get("recommendations", [])
        profile.last_justification_id = latest_justification_id
    else:
        profile = quiz_models.EthicalBiasProfile(
            user_id=user_id,
            primary_framework=analysis.get("primary_framework", "Unknown"),
            secondary_frameworks=analysis.get("secondary_frameworks", []),
            reasoning_patterns=analysis.get("reasoning_patterns", {}),
            summary=analysis.get("summary", ""),
            recommendations=analysis.get("recommendations", []),
            last_justification_id=latest_justification_id
        )
        db.add(profile)
    
    db.commit()
    db.refresh(profile)
    return profile


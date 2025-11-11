from sqlalchemy.orm import Session
from typing import List, Dict, Any

from quizzes import models
from schemas import QuizCreate, QuizAttemptCreate

def get_quiz(db: Session, quiz_id: int):
    return db.query(models.Quiz).filter(models.Quiz.id == quiz_id).first()

def get_quizzes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Quiz).offset(skip).limit(limit).all()

def create_quiz(db: Session, quiz: QuizCreate):
    questions_payload = [q.dict() for q in quiz.questions]
    db_quiz = models.Quiz(title=quiz.title, category=quiz.category, questions=questions_payload)
    db.add(db_quiz)
    db.commit()
    db.refresh(db_quiz)
    return db_quiz

def record_quiz_attempt(
    db: Session,
    user_id: int,
    attempt: QuizAttemptCreate,
    quiz: models.Quiz,
    answers: Dict[str, str] = None,
    justifications: Dict[str, str] = None
) -> models.QuizAttempt:
    """Record quiz attempt with detailed answer breakdown and justifications"""
    answers = answers or {}
    justifications = justifications or {}
    
    # Build answer_details: {question_id: {answer, justification, is_correct}}
    answer_details = {}
    score = 0
    
    for q_data in quiz.questions:
        question_id = str(q_data.get("id"))
        correct_answer = q_data.get("correct_answer")
        user_answer = answers.get(question_id, "")
        justification = justifications.get(question_id, "")
        is_correct = (user_answer == correct_answer)
        
        if is_correct:
            score += 1
        
        answer_details[question_id] = {
            "answer": user_answer,
            "justification": justification,
            "is_correct": is_correct,
            "correct_answer": correct_answer
        }
        
        # Store justification in UserJustification table
        if justification:
            db_justification = models.UserJustification(
                attempt_id=None,  # Will be set after attempt is created
                question_id=int(question_id),
                justification_text=justification,
                user_answer=user_answer,
                is_correct=1 if is_correct else 0
            )
            # We'll add this after the attempt is created
    
    total = len(quiz.questions)
    accuracy = (score / total) * 100 if total > 0 else 0
    
    # Create attempt
    db_attempt = models.QuizAttempt(
        user_id=user_id,
        quiz_id=attempt.quiz_id,
        score=score,
        total=total,
        accuracy=accuracy,
        answer_details=answer_details
    )
    db.add(db_attempt)
    db.flush()  # Get the ID without committing
    
    # Now add justifications with the attempt_id
    for q_data in quiz.questions:
        question_id = str(q_data.get("id"))
        justification = justifications.get(question_id, "")
        if justification:
            user_answer = answers.get(question_id, "")
            is_correct = answer_details[question_id]["is_correct"]
            db_justification = models.UserJustification(
                attempt_id=db_attempt.id,
                question_id=int(question_id),
                justification_text=justification,
                user_answer=user_answer,
                is_correct=1 if is_correct else 0
            )
            db.add(db_justification)
    
    db.commit()
    db.refresh(db_attempt)
    return db_attempt

def get_user_quiz_attempts(db: Session, user_id: int) -> List[models.QuizAttempt]:
    return (
        db.query(models.QuizAttempt)
        .filter(models.QuizAttempt.user_id == user_id)
        .order_by(models.QuizAttempt.timestamp.asc())
        .all()
    )

def get_user_justifications(db: Session, user_id: int) -> List[models.UserJustification]:
    """Get all justifications for a user across all attempts"""
    return (
        db.query(models.UserJustification)
        .join(models.QuizAttempt)
        .filter(models.QuizAttempt.user_id == user_id)
        .order_by(models.UserJustification.timestamp.desc())
        .all()
    )

def get_attempt_by_id(db: Session, attempt_id: int, user_id: int = None) -> models.QuizAttempt:
    """Get a specific quiz attempt by ID"""
    query = db.query(models.QuizAttempt).filter(models.QuizAttempt.id == attempt_id)
    if user_id:
        query = query.filter(models.QuizAttempt.user_id == user_id)
    return query.first()

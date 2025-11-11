from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72) # bcrypt limit is 72 bytes

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=72) # bcrypt limit is 72 bytes

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class Question(BaseModel):
    id: int
    question_text: str
    options: List[str]
    correct_answer: str

class QuizBase(BaseModel):
    title: str
    category: str
    questions: List[Question]

class QuizCreate(QuizBase):
    pass

class Quiz(QuizBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Pydantic V2 (replaces orm_mode)

class QuizAttemptBase(BaseModel):
    quiz_id: int
    score: int
    total: int
    accuracy: float

class QuizAttemptCreate(QuizAttemptBase):
    answers: Optional[dict] = {}  # {question_id: selected_answer}
    justifications: Optional[dict] = {}  # {question_id: justification_text}

class QuizAttempt(QuizAttemptBase):
    id: int
    user_id: int
    timestamp: datetime
    answer_details: Optional[dict] = {}

    class Config:
        from_attributes = True  # Pydantic V2 (replaces orm_mode)

class AnswerExplanation(BaseModel):
    question_id: int
    user_answer: str
    correct_answer: str
    is_correct: bool
    explanation: str
    ethical_frameworks: Optional[List[str]] = None
    real_world_parallels: Optional[List[str]] = None

class PostQuizAnalysis(BaseModel):
    attempt_id: int
    score: int
    total: int
    accuracy: float
    explanations: List[AnswerExplanation]
    overall_feedback: str

class EthicalConflictExplanation(BaseModel):
    question_id: int
    question_text: str
    options: List[str]
    pros_cons: dict  # {option: {pros: [], cons: []}}
    ethical_frameworks: List[str]
    real_world_parallels: List[str]
    explanation: str

class EthicalBiasProfile(BaseModel):
    user_id: int
    primary_framework: str  # e.g., "Utilitarian", "Deontological", "Virtue Ethics"
    secondary_frameworks: List[str]
    reasoning_patterns: dict
    summary: str
    recommendations: List[str]

from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB

from database import Base

class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    category = Column(String, index=True)
    questions = Column(JSONB)  # Store questions as JSONB
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    attempts = relationship("QuizAttempt", back_populates="quiz")

class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    score = Column(Integer)
    total = Column(Integer)
    accuracy = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    # Store detailed answer breakdown: {question_id: {answer, justification, is_correct}}
    answer_details = Column(JSONB, default={})

    owner = relationship("User", back_populates="attempts")
    quiz = relationship("Quiz", back_populates="attempts")
    justifications = relationship("UserJustification", back_populates="attempt", cascade="all, delete-orphan")

class UserJustification(Base):
    __tablename__ = "user_justifications"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("quiz_attempts.id"))
    question_id = Column(Integer)
    justification_text = Column(Text)
    user_answer = Column(String)
    is_correct = Column(Integer, default=0)  # 0 = wrong, 1 = correct
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    attempt = relationship("QuizAttempt", back_populates="justifications")


class EthicalBiasProfile(Base):
    __tablename__ = "ethical_bias_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True)
    primary_framework = Column(String, nullable=True)
    secondary_frameworks = Column(JSONB, default=[])  # Store as array
    reasoning_patterns = Column(JSONB, default={})  # Store as object
    summary = Column(Text, nullable=True)
    recommendations = Column(JSONB, default=[])  # Store as array
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    last_justification_id = Column(Integer, nullable=True)  # Track last justification used for computation

    owner = relationship("User", back_populates="ethical_bias_profile")
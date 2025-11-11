from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    attempts = relationship("QuizAttempt", back_populates="owner", cascade="all, delete-orphan")
    ethical_bias_profile = relationship("EthicalBiasProfile", back_populates="owner", uselist=False, cascade="all, delete-orphan")

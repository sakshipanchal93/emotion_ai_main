from datetime import datetime

from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class MoodRecord(Base):
    __tablename__ = "mood_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    employee_id: Mapped[str] = mapped_column(String(100), index=True)
    team_id: Mapped[str] = mapped_column(String(100), index=True)
    text_input: Mapped[str | None] = mapped_column(String(2000), nullable=True)
    emotion: Mapped[str] = mapped_column(String(50), index=True)
    sentiment_score: Mapped[float] = mapped_column(Float)
    source: Mapped[str] = mapped_column(String(50), default="text")
    confidence: Mapped[float] = mapped_column(Float, default=0.5)
    is_negative: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class TaskRecommendation(Base):
    __tablename__ = "task_recommendations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    mood_record_id: Mapped[int] = mapped_column(ForeignKey("mood_records.id", ondelete="CASCADE"))
    employee_id: Mapped[str] = mapped_column(String(100), index=True)
    task_title: Mapped[str] = mapped_column(String(255))
    task_type: Mapped[str] = mapped_column(String(100))
    priority: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class StressAlert(Base):
    __tablename__ = "stress_alerts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    employee_id: Mapped[str] = mapped_column(String(100), index=True)
    team_id: Mapped[str] = mapped_column(String(100), index=True)
    streak_count: Mapped[int] = mapped_column(Integer)
    message: Mapped[str] = mapped_column(String(500))
    resolved: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

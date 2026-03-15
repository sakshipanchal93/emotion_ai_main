from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


EmotionType = Literal["happy", "neutral", "stressed", "sad", "angry"]


class DetectEmotionRequest(BaseModel):
    employee_id: str = Field(min_length=1)
    team_id: str = Field(min_length=1)
    text_input: str = Field(default="", max_length=2000)


class EmotionDetectionResult(BaseModel):
    emotion: EmotionType
    sentiment_score: float
    confidence: float
    source: str


class TaskSuggestion(BaseModel):
    task_title: str
    task_type: str
    priority: str


class EmotionDetectionResponse(BaseModel):
    detection: EmotionDetectionResult
    recommendations: list[TaskSuggestion]
    alert_triggered: bool


class MoodHistoryItem(BaseModel):
    emotion: EmotionType
    sentiment_score: float
    source: str
    created_at: datetime


class TeamAnalyticsResponse(BaseModel):
    team_id: str
    total_records: int
    emotion_distribution: dict[str, int]
    average_sentiment: float
    stress_index: float


class StressAlertResponse(BaseModel):
    employee_id: str
    team_id: str
    streak_count: int
    message: str
    created_at: datetime

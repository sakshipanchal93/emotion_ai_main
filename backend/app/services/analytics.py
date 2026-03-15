from __future__ import annotations

from collections import Counter

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.mood import MoodRecord


class AnalyticsService:
    def employee_history(self, db: Session, employee_id: str, limit: int = 30) -> list[MoodRecord]:
        return (
            db.query(MoodRecord)
            .filter(MoodRecord.employee_id == employee_id)
            .order_by(desc(MoodRecord.created_at))
            .limit(limit)
            .all()
        )

    def team_distribution(self, db: Session, team_id: str) -> tuple[dict[str, int], float, float, int]:
        records = db.query(MoodRecord).filter(MoodRecord.team_id == team_id).all()
        total = len(records)
        if total == 0:
            return {"happy": 0, "neutral": 0, "stressed": 0, "sad": 0, "angry": 0}, 0.0, 0.0, 0

        emotions = Counter(record.emotion for record in records)
        distribution = {
            "happy": emotions.get("happy", 0),
            "neutral": emotions.get("neutral", 0),
            "stressed": emotions.get("stressed", 0),
            "sad": emotions.get("sad", 0),
            "angry": emotions.get("angry", 0),
        }
        avg_sentiment = sum(record.sentiment_score for record in records) / total
        negative_count = sum(1 for record in records if record.emotion in {"stressed", "sad", "angry"})
        stress_index = round((negative_count / total) * 100, 2)
        return distribution, round(avg_sentiment, 4), stress_index, total

from __future__ import annotations

from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.models.mood import MoodRecord, StressAlert


class AlertService:
    TRIGGER_EMOTION = "stressed"

    def current_stress_streak(self, db: Session, employee_id: str, max_window: int = 20) -> int:
        recent = (
            db.query(MoodRecord)
            .filter(MoodRecord.employee_id == employee_id)
            .order_by(desc(MoodRecord.created_at))
            .limit(max_window)
            .all()
        )
        streak = 0
        for item in recent:
            if item.emotion == self.TRIGGER_EMOTION:
                streak += 1
            else:
                break
        return streak

    def evaluate_stress_streak(self, db: Session, employee_id: str, threshold: int, team_id: str) -> StressAlert | None:
        recent = (
            db.query(MoodRecord)
            .filter(MoodRecord.employee_id == employee_id)
            .order_by(desc(MoodRecord.created_at))
            .limit(threshold)
            .all()
        )
        if len(recent) < threshold:
            return None

        if all(item.emotion == self.TRIGGER_EMOTION for item in recent):
            alert = StressAlert(
                employee_id=employee_id,
                team_id=team_id,
                streak_count=threshold,
                message="Consecutive stressed mood detected. Recommend manager check-in and wellness break.",
            )
            db.add(alert)
            db.commit()
            db.refresh(alert)
            return alert
        return None

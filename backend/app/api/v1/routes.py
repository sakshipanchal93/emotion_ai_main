from flask import Blueprint, jsonify, request
from sqlalchemy import desc

from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.mood import MoodRecord, StressAlert, TaskRecommendation
from app.services.alerts import AlertService
from app.services.analytics import AnalyticsService
from app.services.emotion import EmotionService
from app.services.facial import FacialEmotionService
from app.services.recommendation import RecommendationService

router = Blueprint("api_v1", __name__, url_prefix="/api/v1")


@router.get("/health")
def health():
    return jsonify({"status": "ok"})


@router.post("/emotion/detect")
def detect_emotion():
    payload = request.get_json(silent=True) or {}
    employee_id = payload.get("employee_id", "").strip()
    team_id = payload.get("team_id", "").strip()
    text_input = payload.get("text_input", "")

    if not employee_id or not team_id:
        return jsonify({"error": "employee_id and team_id are required"}), 400

    db = SessionLocal()
    try:
        settings = get_settings()
        emotion_service = EmotionService()
        recommendation_service = RecommendationService()
        alert_service = AlertService()

        detection = emotion_service.from_text(text_input)
        mood_record = MoodRecord(
            employee_id=employee_id,
            team_id=team_id,
            text_input=text_input,
            emotion=detection.emotion,
            sentiment_score=detection.sentiment_score,
            source=detection.source,
            confidence=detection.confidence,
            is_negative=detection.emotion in {"stressed", "sad", "angry"},
        )
        db.add(mood_record)
        db.commit()
        db.refresh(mood_record)

        recommendations = recommendation_service.suggest_tasks(detection.emotion)
        for task in recommendations:
            db.add(
                TaskRecommendation(
                    mood_record_id=mood_record.id,
                    employee_id=employee_id,
                    task_title=task.task_title,
                    task_type=task.task_type,
                    priority=task.priority,
                )
            )
        db.commit()

        alert = alert_service.evaluate_stress_streak(
            db=db,
            employee_id=employee_id,
            threshold=settings.stress_streak_threshold,
            team_id=team_id,
        )
        current_streak = alert_service.current_stress_streak(db, employee_id)

        return jsonify(
            {
                "detection": {
                    "emotion": detection.emotion,
                    "sentiment_score": detection.sentiment_score,
                    "confidence": detection.confidence,
                    "source": detection.source,
                },
                "recommendations": [
                    {
                        "task_title": item.task_title,
                        "task_type": item.task_type,
                        "priority": item.priority,
                    }
                    for item in recommendations
                ],
                "alert_triggered": alert is not None,
                "current_stress_streak": current_streak,
                "stress_streak_threshold": settings.stress_streak_threshold,
            }
        )
    finally:
        db.close()


@router.post("/emotion/detect/webcam")
def detect_webcam_emotion():
    payload = request.get_json(silent=True) or {}
    employee_id = payload.get("employee_id", "").strip()
    team_id = payload.get("team_id", "").strip()
    image_base64 = payload.get("image_base64", "")

    if not employee_id or not team_id or not image_base64:
        return jsonify({"error": "employee_id, team_id and image_base64 are required"}), 400

    db = SessionLocal()
    try:
        settings = get_settings()
        facial_service = FacialEmotionService()
        recommendation_service = RecommendationService()
        alert_service = AlertService()

        face_result = facial_service.detect_from_base64_image(image_base64)
        mood_record = MoodRecord(
            employee_id=employee_id,
            team_id=team_id,
            text_input=None,
            emotion=face_result.emotion,
            sentiment_score=0.0,
            source=face_result.source,
            confidence=face_result.confidence,
            is_negative=face_result.emotion in {"stressed", "sad", "angry"},
        )
        db.add(mood_record)
        db.commit()
        db.refresh(mood_record)

        recommendations = recommendation_service.suggest_tasks(face_result.emotion)
        for task in recommendations:
            db.add(
                TaskRecommendation(
                    mood_record_id=mood_record.id,
                    employee_id=employee_id,
                    task_title=task.task_title,
                    task_type=task.task_type,
                    priority=task.priority,
                )
            )
        db.commit()

        alert = alert_service.evaluate_stress_streak(
            db=db,
            employee_id=employee_id,
            threshold=settings.stress_streak_threshold,
            team_id=team_id,
        )
        current_streak = alert_service.current_stress_streak(db, employee_id)

        return jsonify(
            {
                "detection": {
                    "emotion": face_result.emotion,
                    "sentiment_score": 0.0,
                    "confidence": face_result.confidence,
                    "source": face_result.source,
                },
                "recommendations": [
                    {
                        "task_title": item.task_title,
                        "task_type": item.task_type,
                        "priority": item.priority,
                    }
                    for item in recommendations
                ],
                "alert_triggered": alert is not None,
                "current_stress_streak": current_streak,
                "stress_streak_threshold": settings.stress_streak_threshold,
            }
        )
    finally:
        db.close()


@router.get("/employees/<employee_id>/mood-history")
def get_mood_history(employee_id: str):
    db = SessionLocal()
    try:
        analytics = AnalyticsService()
        records = analytics.employee_history(db, employee_id)
        return jsonify(
            [
                {
                    "emotion": record.emotion,
                    "sentiment_score": record.sentiment_score,
                    "source": record.source,
                    "created_at": record.created_at.isoformat(),
                }
                for record in records
            ]
        )
    finally:
        db.close()


@router.get("/teams/<team_id>/analytics")
def get_team_analytics(team_id: str):
    db = SessionLocal()
    try:
        analytics = AnalyticsService()
        distribution, average_sentiment, stress_index, total = analytics.team_distribution(db, team_id)
        return jsonify(
            {
                "team_id": team_id,
                "total_records": total,
                "emotion_distribution": distribution,
                "average_sentiment": average_sentiment,
                "stress_index": stress_index,
            }
        )
    finally:
        db.close()


@router.get("/alerts")
def get_alerts():
    db = SessionLocal()
    try:
        alerts = db.query(StressAlert).order_by(desc(StressAlert.created_at)).limit(50).all()
        return jsonify(
            [
                {
                    "employee_id": alert.employee_id,
                    "team_id": alert.team_id,
                    "streak_count": alert.streak_count,
                    "message": alert.message,
                    "created_at": alert.created_at.isoformat(),
                }
                for alert in alerts
            ]
        )
    finally:
        db.close()

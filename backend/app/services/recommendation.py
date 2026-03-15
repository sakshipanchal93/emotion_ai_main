from __future__ import annotations

from app.schemas.mood import TaskSuggestion


class RecommendationService:
    def suggest_tasks(self, emotion: str) -> list[TaskSuggestion]:
        mapping: dict[str, list[TaskSuggestion]] = {
            "happy": [
                TaskSuggestion(task_title="Brainstorm product improvements", task_type="creative", priority="medium"),
                TaskSuggestion(task_title="Collaborate on team planning", task_type="collaborative", priority="high"),
                TaskSuggestion(task_title="Lead innovation huddle", task_type="leadership", priority="medium"),
            ],
            "neutral": [
                TaskSuggestion(task_title="Execute sprint backlog", task_type="regular", priority="high"),
                TaskSuggestion(task_title="Review pending tickets", task_type="regular", priority="medium"),
                TaskSuggestion(task_title="Update project documentation", task_type="regular", priority="medium"),
            ],
            "stressed": [
                TaskSuggestion(task_title="Complete low-complexity tasks", task_type="light", priority="low"),
                TaskSuggestion(task_title="Take a guided 10-minute break", task_type="wellness", priority="high"),
                TaskSuggestion(task_title="Do inbox cleanup", task_type="light", priority="low"),
            ],
            "sad": [
                TaskSuggestion(task_title="Pair with teammate on a small task", task_type="supportive", priority="medium"),
                TaskSuggestion(task_title="Take a short wellness break", task_type="wellness", priority="high"),
                TaskSuggestion(task_title="Work on structured checklist items", task_type="light", priority="low"),
            ],
            "angry": [
                TaskSuggestion(task_title="Pause and perform breathing exercise", task_type="wellness", priority="high"),
                TaskSuggestion(task_title="Handle independent low-risk tasks", task_type="light", priority="medium"),
                TaskSuggestion(task_title="Reschedule high-conflict meetings", task_type="management", priority="high"),
            ],
        }
        return mapping.get(emotion, mapping["neutral"])

from __future__ import annotations

from dataclasses import dataclass
import re

from textblob import TextBlob


@dataclass
class EmotionResult:
    emotion: str
    sentiment_score: float
    confidence: float
    source: str


class EmotionService:
    NEGATIVE_KEYWORDS = {"stressed", "burnout", "overwhelmed", "sad", "angry", "upset", "tired"}
    ANGRY_KEYWORDS = {"angry", "furious", "rage", "irritated"}
    POSITIVE_KEYWORDS = {
        "happy",
        "excited",
        "great",
        "good",
        "productive",
        "motivated",
        "confident",
        "glad",
        "energetic",
        "awesome",
    }

    def from_text(self, text_input: str) -> EmotionResult:
        text = text_input.strip()
        if not text:
            return EmotionResult(emotion="neutral", sentiment_score=0.0, confidence=0.5, source="text")

        polarity = TextBlob(text).sentiment.polarity
        lowered_tokens = set(re.findall(r"[a-zA-Z']+", text.lower()))

        if lowered_tokens.intersection(self.NEGATIVE_KEYWORDS):
            polarity -= 0.1

        if lowered_tokens.intersection(self.POSITIVE_KEYWORDS):
            polarity += 0.3

        polarity = max(-1.0, min(1.0, polarity))

        if lowered_tokens.intersection(self.ANGRY_KEYWORDS) and polarity <= -0.3:
            emotion = "angry"
        elif polarity >= 0.2:
            emotion = "happy"
        elif polarity <= -0.75:
            emotion = "angry"
        elif polarity <= -0.25:
            emotion = "stressed"
        elif polarity < -0.1:
            emotion = "sad"
        else:
            emotion = "neutral"

        confidence = min(0.95, max(0.55, abs(polarity) + 0.5))
        return EmotionResult(
            emotion=emotion,
            sentiment_score=round(float(polarity), 4),
            confidence=round(confidence, 4),
            source="text",
        )

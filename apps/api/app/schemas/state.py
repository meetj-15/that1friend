from typing import Literal

from pydantic import BaseModel, Field


MoodLabel = Literal[
    "neutral", "happy", "sad", "angry", "frustrated",
    "anxious", "excited", "overwhelmed", "playful",
]


class MoodState(BaseModel):
    mood: MoodLabel = "neutral"
    confidence: float = Field(default=0.0, ge=0, le=1)
    seriousness: float = Field(default=0.0, ge=0, le=1)
    humor_allowed: float = Field(default=0.5, ge=0, le=1)
    empathy: float = Field(default=0.7, ge=0, le=1)
    serious_distress: bool = False

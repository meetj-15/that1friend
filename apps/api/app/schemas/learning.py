from pydantic import BaseModel
from typing import Literal


class LearningProfile(BaseModel):
    preferred_depth: Literal["short", "medium", "deep"] = "medium"
    explanation_order: list[str] = ["intuition", "example", "formal", "practice"]
    visual_density: Literal["low", "medium", "high"] = "medium"
    exam_focus: list[str] = []
    strengths: list[str] = []
    weaknesses: list[str] = []

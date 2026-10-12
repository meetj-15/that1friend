import json

from app.schemas.learning import LearningProfile
from app.services.model.base import ChatMessage, ModelProvider


class TeachService:
    def __init__(self, provider: ModelProvider) -> None:
        self.provider = provider

    async def create_lesson(
        self,
        topic: str,
        profile: LearningProfile,
        time_budget_minutes: int | None = None,
    ) -> dict:
        prompt = {
            "topic": topic,
            "learner": profile.model_dump(),
            "time_budget_minutes": time_budget_minutes,
            "instructions": [
                "Start with intuition.",
                "Use one memorable analogy.",
                "Then provide a concrete example.",
                "Only introduce formal notation after the idea is clear.",
                "End with 3 short questions and one teach-back prompt.",
                "Return JSON with title, concept_map, explanation, practice, teach_back.",
            ],
        }
        raw = await self.provider.chat([
            ChatMessage(role="system", content="You are an expert tutor. Return valid JSON only."),
            ChatMessage(role="user", content=json.dumps(prompt)),
        ], temperature=0.2)
        return json.loads(raw)

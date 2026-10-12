import json

from pydantic import ValidationError

from app.services.model.base import ChatMessage, ModelProvider
from app.schemas.state import MoodState


PROMPT = """
Classify the user's current conversational mood for response style only.
Return ONLY JSON with these fields:
{
  "mood": "neutral|happy|sad|angry|frustrated|anxious|excited|overwhelmed|playful",
  "confidence": 0.0,
  "seriousness": 0.0,
  "humor_allowed": 0.0,
  "empathy": 0.0,
  "serious_distress": false
}
Do not diagnose mental-health conditions. Ordinary sadness, a breakup, or career
stress does not automatically mean serious_distress=true. Set that flag only when
there is clear significant distress or an urgent safety concern. When uncertain,
prefer a calm, clear response with low humor rather than making a strong inference.
""".strip()


async def classify_mood(provider: ModelProvider, user_message: str) -> MoodState:
    raw = await provider.chat(
        [
            ChatMessage(role="system", content=PROMPT),
            ChatMessage(role="user", content=user_message),
        ],
        temperature=0.0,
    )
    try:
        return MoodState.model_validate(json.loads(raw))
    except (json.JSONDecodeError, ValidationError):
        return MoodState(
            mood="neutral",
            confidence=0.0,
            seriousness=0.5,
            humor_allowed=0.0,
            empathy=0.7,
            serious_distress=False,
        )

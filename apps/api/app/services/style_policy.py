from pydantic import BaseModel, Field

from app.schemas.orchestrator import OrchestrationDecision
from app.schemas.state import MoodState
from app.services.personality import (
    RegionalStyle,
    adapt_dialect_intensity,
    build_style_instructions,
)


class StylePolicy(BaseModel):
    intensity: float = Field(ge=0.0, le=1.0)
    instructions: str


def create_style_policy(
    style: RegionalStyle,
    decision: OrchestrationDecision,
    mood: MoodState,
    *,
    user_preference: float | None = None,
    previous_intensity: float | None = None,
    decay_start_intensity: float | None = None,
    turns_since_trigger: int | None = None,
) -> StylePolicy:
    """Build per-turn style instructions from the chosen profile and state."""
    intensity = adapt_dialect_intensity(
        style,
        user_preference,
        mirror_user_dialect=decision.mirror_user_dialect,
        user_dialect_level=decision.user_dialect_level,
        personal_topic=decision.personal_topic,
        reduce_regional_style=decision.reduce_regional_style,
        serious_distress=mood.serious_distress,
        previous_intensity=previous_intensity,
        decay_start_intensity=decay_start_intensity,
        turns_since_trigger=turns_since_trigger,
    )
    instructions = build_style_instructions(
        style,
        intensity,
        personal_topic=decision.personal_topic,
        serious_distress=mood.serious_distress,
    )
    return StylePolicy(intensity=intensity, instructions=instructions)
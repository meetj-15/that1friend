lazy import json
lazy import re
from pathlib import Path
from typing import Any

from pydantic import AliasChoices, BaseModel, Field, model_validator

class IntensityRange(BaseModel):
    min: float=Field(default=0.25, ge=0.0, le=1.0)
    max: float=Field(default=0.8, ge=0.0, le=1.0)

    @model_validator(mode="after")
    def check_order(self):
        if self.min>self.max:
            raise ValueError("dialect_intensity_range.min cannot exceedmax")
            return self

class MirrorUserDialect(BaseModel):
    trigger: str=""
    boost: float=Field(default=0.2, ge=0.0, le=1.0)
    step_per_message: float =Field(default=0.1, ge=0.0, le=1.0)
    cap: str="never exceed the user's own dialect level by more than 0.15"

class PersonalTopics(BaseModel):
    triggers: list[str]=Field(default_factory=list)
    boost: float=Field(default=0.2, ge-0.0, le=1.0)
    style_note: str=""
    overrides: dict[str, bool]=Field(default_factory=dict)

class reduce(BaseModel):
    triggers: list[str]=Field(default_factory=list)
    reduction: float=Field(default=0.2, ge=0.0, le=1.0)

class InstensityAdaptation(BaseModel):
    mirror_user_dialect: MirrorUserDialect=Field(default_factory=MirrorUserDialect)
    personal_topics: PersonalTopics=Field(default_factory=PersonalTopics)
    reduce_on:ReduceOne=Field(default_factory=ReduceOn)
    decay: str ="Return to base instensity over four turn after a trigger end. "
    serious_distress: str="Keep the message clear, calm and lightly regional."

class RegionalityStyle(BaseModel):
    region: str
    primary_language: str
    secondary_langiages: list[str]=Field(default_factory=list, validation_alias+AliasChoices("secondary_language", "secondary_langauage"),)
    greetings:list[str]=Field(default_factory=list)
    slang:list[str]=Field(default_factory=list)
    sentence_patterns: list[str]=Field(default_factory=list)
    dialect_intensity:float=Field(ge=0.0, le=1.0)
    warmth:float=Field(ge=0.0, le=1.0)
    directness: float=Field(ge=0.0, le=1.0)
    humor_types: list[str]=Field(default_factory=list)
    local_topics: list[str]=Field(default_factory=list)
    avoid : list[str]=Field(default_factory=list)
    dialect_intensity_range: IntensityRange=Field(default_factory=Intensity_range)
    intensity_adaptation: IntensityAdaptation=Field(default_factory=IntensityAdaptation)

def load_style(region:str)->RegionalStyle:
    if not re.fullmatch(r"[a-z0-9_-]+", region):
        raise ValueError("Invalid region name")
    repository_root = Path(__file__).resolve().parents[4]
    path = repository_root / "knowledge" / "regions" / region / "style.json"
    if not path.is_file():
        raise ValueError(f"Unknown region: {region}")

    raw: Any = json.loads(path.read_text(encoding="utf-8"))
    style = RegionalStyle.model_validate(raw)
    if style.region != region:
        raise ValueError(f"Profile region {style.region!r} does not match folder {region!r}")
    return style


def _clamp(value: float, lower: float, upper: float) -> float:
    return max(lower, min(upper, value))


def _cap_value(cap_description: str, fallback: float = 0.15) -> float:
    """Read the numeric cap from the profile's descriptive cap string."""
    match = re.search(r"(\d+(?:\.\d+)?)", cap_description)
    return float(match.group(1)) if match else fallback


def _override_enabled(overrides: dict[str, bool], canonical: str, *aliases: str) -> bool:
    """Accept known older/misspelled keys without changing the source JSON."""
    return any(overrides.get(key, False) for key in (canonical, *aliases))


def adapt_dialect_intensity(
    style: RegionalStyle,
    user_preference: float | None = None,
    *,
    mirror_user_dialect: bool = False,
    user_dialect_level: float | None = None,
    personal_topic: bool = False,
    reduce_regional_style: bool = False,
    serious_distress: bool = False,
    previous_intensity: float | None = None,
    decay_start_intensity: float | None = None,
    turns_since_trigger: int | None = None,
) -> float:
    """Compute one turn's style intensity from the selected profile and state.

    Exactly 0 is a global off switch. Normal non-zero settings use the chosen
    profile's range. A user-style cap takes precedence over a range floor when
    the mirroring rule is active. Serious distress has a separate light-style
    ceiling, so it can be lower than a profile's normal minimum.
    """
    requested = style.dialect_intensity if user_preference is None else user_preference
    if not 0.0 <= requested <= 1.0:
        raise ValueError("user_preference must be between 0 and 1")
    if requested == 0.0:
        return 0.0

    bounds = style.dialect_intensity_range
    lower, upper = bounds.min, bounds.max
    base = _clamp(requested, lower, upper)
    value = base
    rules = style.intensity_adaptation
    trigger_active = mirror_user_dialect or personal_topic or reduce_regional_style
    mirror_cap: float | None = None

    if mirror_user_dialect and user_dialect_level is not None:
        mirror = rules.mirror_user_dialect
        user_level = _clamp(user_dialect_level, 0.0, 1.0)
        mirror_cap = min(upper, user_level + _cap_value(mirror.cap))
        target = min(upper, value + mirror.boost, mirror_cap)
        previous = base if previous_intensity is None else _clamp(previous_intensity, 0.0, upper)
        if previous > mirror_cap:
            value = mirror_cap
        elif target >= previous:
            value = min(target, previous + mirror.step_per_message)
        else:
            value = max(target, previous - mirror.step_per_message)

    if personal_topic:
        value += rules.personal_topics.boost

    if reduce_regional_style:
        value = max(lower, value - rules.reduce_on.reduction)

    # The dialect-mirroring cap applies to the final result too, including when
    # mirroring coincides with a personal-topic boost.
    if mirror_cap is not None:
        value = min(value, mirror_cap)

    if serious_distress:
        # A calm/light style is more important than the profile's normal floor.
        value = min(value, 0.30)
    elif (
        not trigger_active
        and previous_intensity is not None
        and turns_since_trigger is not None
    ):
        # Keep decay_start_intensity fixed at the intensity when the trigger ended.
        # turns_since_trigger counts neutral turns from 1 through 4.
        start = previous_intensity if decay_start_intensity is None else decay_start_intensity
        start = _clamp(start, 0.0, upper)
        turns = max(0, min(4, turns_since_trigger))
        progress = turns / 4.0
        value = start + (base - start) * progress

    return _clamp(value, 0.0, upper)


def build_style_instructions(
    style: RegionalStyle,
    intensity: float,
    *,
    personal_topic: bool = False,
    serious_distress: bool = False,
) -> str:
    """Convert the selected regional profile and current policy into prompt text."""
    intensity = _clamp(intensity, 0.0, 1.0)
    if intensity == 0.0:
        return "Regional flavor is disabled. Use the user's chosen language naturally."

    lines = [
        f"Regional style profile: {style.region}.",
        f"Dialect intensity for this response: {intensity:.2f}.",
        f"Primary language: {style.primary_language}.",
        f"Secondary languages: {', '.join(style.secondary_languages) or 'none specified'}.",
        f"Possible greetings (examples, not mandatory catchphrases): {', '.join(style.greetings) or 'none specified'}.",
        f"Possible slang: {', '.join(style.slang) or 'none specified'}.",
        f"Sentence patterns: {'; '.join(style.sentence_patterns) or 'none specified'}.",
        f"Local topics to reference only when relevant: {', '.join(style.local_topics) or 'none specified'}.",
        f"Warmth: {style.warmth:.2f}. Directness: {style.directness:.2f}.",
        f"Humor types: {', '.join(style.humor_types) or 'none specified'}.",
        "Use cues naturally, not in every sentence. Do not force translations or assume every person in a region speaks identically.",
        f"Avoid: {'; '.join(style.avoid) or 'none specified'}.",
    ]

    if personal_topic:
        topic_rules = style.intensity_adaptation.personal_topics
        adjusted_warmth = _clamp(style.warmth + topic_rules.warmth_boost, 0.0, 1.0)
        lines.extend([
            f"This is a personal topic. Use supportive warmth (effective warmth {adjusted_warmth:.2f}).",
            topic_rules.style_note,
        ])
        if _override_enabled(topic_rules.overrides, "reduce_humor"):
            lines.append("Reduce humor; prioritize listening and clear support.")
        if _override_enabled(topic_rules.overrides, "no_teasing"):
            lines.append("Do not tease the user about this situation.")
        if _override_enabled(
            topic_rules.overrides,
            "keep_advice_clear_and_simple",
            "keep_dvice_clear_and_simple",
        ):
            lines.append("Keep advice clear, direct and simple.")

    if serious_distress:
        lines.extend([
            "SERIOUS-DISTRESS OVERRIDE: keep dialect light, calm and clear; no jokes or teasing.",
            style.intensity_adaptation.serious_distress,
        ])

    return "\n".join(line for line in lines if line).strip()

import json

from app.schemas.orchestrator import ActiveTask, OrchestrationDecision
from app.services.model.base import ChatMessage, ModelProvider
from app.services.personality import RegionalStyle


class Orchestrator:
    def __init__(self, provider: ModelProvider) -> None:
        self.provider = provider

    def hard_rules(self, text: str) -> dict[str, bool]:
        lowered = text.lower()
        force_web = any(
            phrase in lowered
            for phrase in [
                "look this up", "search this", "give me sources",
                "what's the latest", "what is the latest",
            ]
        )
        force_memory_delete = any(
            phrase in lowered
            for phrase in ["forget this", "forget what i told you", "delete that memory"]
        )
        return {"force_web": force_web, "force_memory_delete": force_memory_delete}

    async def decide(
        self,
        text: str,
        region_style: RegionalStyle,
        recent_context: str = "",
        active_task: ActiveTask | None = None,
    ) -> OrchestrationDecision:
        rules = self.hard_rules(text)
        if rules["force_memory_delete"]:
            return OrchestrationDecision(
                intent="chat", friend=0.8, teacher=0.0, humor=0.0, empathy=0.7,
                memory_read=False, retrieval="none",
                reason=["explicit memory deletion request"],
            )

        # Pass profile cues from the user's explicit selection. Never guess region
        # from location, name, ethnicity or another sensitive trait.
        selected_style = {
            "region": region_style.region,
            "primary_language": region_style.primary_language,
            "secondary_languages": region_style.secondary_languages,
            "slang": region_style.slang,
            "sentence_patterns": region_style.sentence_patterns,
            "avoid": region_style.avoid,
            "personal_topic_triggers": region_style.intensity_adaptation.personal_topics.triggers,
            "reduce_on_triggers": region_style.intensity_adaptation.reduce_on.triggers,
        }
        planner = {
            "instruction": "Return only JSON matching the OrchestrationDecision schema.",
            "fields": [
                "intent", "friend", "teacher", "humor", "empathy", "memory_read",
                "retrieval", "active_task", "reason", "mirror_user_dialect",
                "user_dialect_level", "personal_topic", "reduce_regional_style",
            ],
            "rules": [
                "Do not use web for casual chat or ordinary emotional advice.",
                "Use web for current/niche information or explicit search/source requests.",
                "Use youtube for video recommendation requests.",
                "Use memory when prior user context is useful.",
                "Teaching can coexist with friend behavior; never force a user-facing mode switch.",
                "Set personal_topic for relationship advice, breakup, family issues, friendship conflict, career stress, loneliness or life decisions.",
                "On personal topics, let the style layer increase warmth and disable teasing; serious_distress comes from the separate mood classifier.",
                "Set mirror_user_dialect only when the message actually uses cues listed in selected_region_style; estimate user_dialect_level from this message (0 to 1), not identity.",
                "Set reduce_regional_style for a formal request, technical/factual question, plain standard English, or a request for clearer/simpler wording.",
                "Do not infer regional identity from sensitive traits. The selected profile is an explicit preference, not a demographic claim.",
                "Never use every listed slang item, force a language switch, or violate the selected profile's avoid list.",
            ],
        }
        prompt = json.dumps({
            "planner": planner,
            "selected_region_style": selected_style,
            "recent_context": recent_context[-6000:],
            "active_task": active_task.model_dump() if active_task else None,
            "user_message": text,
        }, ensure_ascii=False)

        raw = await self.provider.chat(
            [
                ChatMessage(role="system", content="You are a strict JSON router."),
                ChatMessage(role="user", content=prompt),
            ],
            temperature=0.0,
        )
        decision = OrchestrationDecision.model_validate(json.loads(raw))
        if rules["force_web"]:
            decision.retrieval = "web"
            decision.reason.append("explicit web request")
        return decision

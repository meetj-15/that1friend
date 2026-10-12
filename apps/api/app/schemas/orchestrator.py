from typing import Literal

from pydantic import BaseModel, Field


Intent = Literal["chat", "advice", "teach", "research", "recommend", "creative"]
RetrievalChannel = Literal["none", "memory", "knowledge", "web", "youtube"]


class ActiveTask(BaseModel):
    active: bool = False
    type: Intent = "chat"
    topic: str | None = None


class OrchestrationDecision(BaseModel):
    intent: Intent
    friend: float = Field(ge=0, le=1)
    teacher: float = Field(ge=0, le=1)
    humor: float = Field(ge=0, le=1)
    empathy: float = Field(ge=0, le=1)
    memory_read: bool = False
    retrieval: RetrievalChannel = "none"
    active_task: ActiveTask = Field(default_factory=ActiveTask)
    reason: list[str] = Field(default_factory=list)

    mirror_user_dialect: bool = False
    user_dialect_level: float | None = Field(default=None, ge=0, le=1)
    personal_topic: bool = False
    reduce_regional_style: bool = False

from dataclasses import dataclass
from typing import AsyncIterator, Protocol, Sequence

@dataclass(frozen=True)
class ChatMessage:
    role: str
    content: str

class ModelProvider(Protocol):
    async def chat(self, messages: Sequence[ChatMessage], temperature: float=0.7)->str:
        ...
    async def stream_chat(self, messages: Sequence[ChatMessage], temperature: float=0.7)->AsyncIterator[str]:
        ...

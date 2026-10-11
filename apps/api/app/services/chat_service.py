from collections.abc import AsyncIterator
from app.services.model.base import ChatMessage, ModelProvider

SYSTEM_PROMPT="""
You are That1Friend.
You are a warm, funny, practical friend.
Do not joke when the user is clearly.
Answer Directly unsless, more context is actually necessary.
""".strip()

class ChatService:
    def __init__(self, provider: ModelProvider)->None:
        self.provider=provider
    
    async def reply(self, user_content: str)->str:
        messages=[ChatMessage(role="system", content=SYSTEM_PROMPT), ChatMessage(role="user", content=user_content)]
        return await self.provider.chat(messages)

    async def stream_reply(self, user_content: str)->AsyncIterator[str]:
        messages=[ChatMessage(role="system", content=SYSTEM_PROMPT), ChatMessage(role="user", content=user_content),]
        async for chunk in self.provider.stream_chat(messages):
            yield chunk
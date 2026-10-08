import json
from collections.abc import AsyncIterator, Sequence
import httpx
from app.core.config import settings
from app.services.model.base import ChatMessage, ModelProvider

class OllamaProvider(ModelProvider):
    def __init__(self)->None:
        self.base_url=settings.ollama_base_url.rstrip("/")
        self.model=settings.ollama_model

    async def chat(self, messages: Sequence[ChatMessage], temperature: float=0.7)->str:
        payload={
            "model":self.model,
            "messages":[m.__dict__ for m in messages],
            "stream":False,
            "options":{"temperature": temperature},
        }
        async with httpx.AsyncClient(timeout=500) as client:
            response=await client.post(f"{self.base_url}/api/chat", json=payload)
            response.raise_for_status()
            data=response.json()
        return data["message"]["content"]
    
    async def stream_chat(self, messages:Sequence[ChatMesage], temperature: float=0.7)->AsyncIterator[str]:
        payload={
            "model":self.model,
            "messages":[m.__dict__ for m in messages],
            "stream": True, 
            "options": {"temperature": temperature},
        }
        async with httpx.AsyncClient(timeout=None) as client:
            async with client.stream("POST", f"{self.base_url}/api/chat", json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    data=json.loads(line)
                    content=data.get("message", {}).get("content", "")
                    if content:
                        yield content
                    if data.get("done"):
                        break
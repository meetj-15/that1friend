import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.chat import ChatInput, ChatResponse
from app.services.chat_service import ChatService
from app.services.model.ollama_provider import OllamaProvider

router=APIRouter(prefix="/chat", tags=["chat"])
service=ChatService(OllamaProvider())

@router.post("", response_model=ChatResponse)
async def chat(payload: ChatInput)->ChatResponse:
    answer=await service.reply(payload.content)
    return ChatResponse(content=answer)

@router.post("/stream")
async def chat_stream(payload: ChatInput)->StreamingResponse:
    async def event_stream():
        async for chunk in service.stream_reply(payload.content):
            yield f"data: {json.dumps({'content':chunk})}\n\n"
        yield "data: [DONE]\n\n"
        
    return StreamingResponse(
    event_stream(),
    media_type="text/event-stream",
    headers={"Cache-Control":"no-cache", "Connection":"keep-alive"},
)
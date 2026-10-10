from pydantic import BaseModel, Field

class ChatInput(BaseModel):
    content: str=Field(min_length=1, max_length=8000)

class ChatResponse(BaseModel):
    content: str


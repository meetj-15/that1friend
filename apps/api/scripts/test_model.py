import asyncio
from app.services.model.base import ChatMessage
from app.services.model.ollama_provider import OllamaProvider

async def main()-> None:
    provider=OllamaProvider()
    messages=[
        ChatMessage(
            role="system",
            content="""
            You are That1Friend. 
            Be warm, funny, practical and conversational.
            Do not force slang.
            Do not joke when user is clearly distressed.
            /no_think
            """.strip(),
        ),
        ChatMessage(
            role="user",
            content="Bro, what is overfitting?",
        ),
    ]
    answer=await provider.chat(messages)
    print(answer)

if __name__=="__main__":
    asyncio.run(main())
"""
Base classes for different types of LLM participants in the discussion.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, AsyncGenerator, Optional
from pydantic import BaseModel
import ollama

class Message(BaseModel):
    """Represents a message in the discussion."""
    role: str
    content: str
    name: Optional[str] = None

class BaseParticipant(ABC):
    """Base class for all participants in the discussion."""
    
    def __init__(self, name: str, model_id: str):
        self.name = name
        self.model_id = model_id
        self.context: list[Message] = []
    
    @abstractmethod
    async def process(self, prompt: str) -> AsyncGenerator[str, None]:
        """Process the input prompt and yield response tokens."""
        pass
    
    def add_to_context(self, message: Message) -> None:
        """Add a message to the conversation context."""
        self.context.append(message)

class OllamaParticipant(BaseParticipant):
    """Participant using Ollama models."""
    
    async def process(self, prompt: str) -> AsyncGenerator[str, None]:
        message = Message(role="user", content=prompt)
        self.add_to_context(message)
        
        async for chunk in await ollama.AsyncClient().chat(
            model=self.model_id,
            messages=[{"role": m.role, "content": m.content} for m in self.context],
            stream=True
        ):
            if chunk.message and chunk.message.content:
                yield chunk.message.content

class OpenAIParticipant(BaseParticipant):
    """Participant using OpenAI models."""
    
    def __init__(self, name: str, model_id: str, api_key: str):
        super().__init__(name, model_id)
        self.api_key = api_key
    
    async def process(self, prompt: str) -> AsyncGenerator[str, None]:
        from openai import AsyncOpenAI
        
        client = AsyncOpenAI(api_key=self.api_key)
        message = Message(role="user", content=prompt)
        self.add_to_context(message)
        
        stream = await client.chat.completions.create(
            model=self.model_id,
            messages=[{"role": m.role, "content": m.content} for m in self.context],
            stream=True
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

class Judge(BaseParticipant):
    """Special participant that acts as a judge."""
    
    def __init__(self, name: str, model_id: str, verdict_threshold: float = 0.8):
        super().__init__(name, model_id)
        self.verdict_threshold = verdict_threshold
    
    async def process(self, prompt: str) -> AsyncGenerator[str, None]:
        """Process the discussion and decide if a verdict can be reached."""
        import ollama
        
        judge_prompt = f"""
        As a judge, evaluate the following discussion and determine if a verdict can be reached.
        Please don't agree to the things that does not make sense. Your job is to question everyones opinon and stick to the truth. 
        Give feedbacks to course correct if needed. always have the case in check before answering.
        Consider:
        1. Have all important aspects been discussed?
        2. Is there enough information to make a decision?
        3. Has the discussion reached a natural conclusion?

        Discussion context:
        {prompt}

        Respond with your analysis and if you believe it's time for a verdict.
        If it's time for a verdict, start your response with 'VERDICT:'
        """
        
        message = Message(role="user", content=judge_prompt)
        self.add_to_context(message)
        
        async for chunk in await ollama.AsyncClient().chat(
            model=self.model_id,
            messages=[{"role": m.role, "content": m.content} for m in self.context],
            stream=True
        ):
            if chunk.get("message", {}).get("content"):
                yield chunk["message"]["content"]

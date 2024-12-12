"""
Core Discussion class that manages the conversation between LLMs.
"""
from typing import List, Optional, Dict, Any, AsyncGenerator, AsyncIterator
import asyncio
from rich.console import Console
from rich.panel import Panel

from .model import BaseParticipant, Judge, Message

console = Console()

class Discussion:
    def __init__(
        self,
        participants: List[BaseParticipant],
        judge: Judge,
        max_rounds: int = 5
    ):
        """
        Initialize a Discussion with participants and a judge.
        
        Args:
            participants: List of participating LLMs
            judge: Judge to oversee the discussion
            max_rounds: Maximum number of discussion rounds
        """
        self.participants = participants
        self.judge = judge
        self.max_rounds = max_rounds
        self.discussion_history: List[Message] = []
    
    def _format_case_prompt(self, case_study: str) -> str:
        """Format the initial case study prompt."""
        return f"""
        Please analyze and discuss the following case:

        {case_study}

        Consider all relevant aspects and share your perspective.
        Please don't agree to the things that does not make sense.
        Engage with other participants' viewpoints respectfully.
        Avoid any personal or biased opinions.
        Focus on the case context and its implications.
        Do not make assumptions about the case.
        Do not make things up.
        Give your analysis in a clear and concise manner.
        Discussion points shall be short.
        Always go through the question before sharing thoughts again.
        """
    
    async def _stream_response(self, participant: BaseParticipant, prompt: str) -> AsyncIterator[str]:
        """Stream a participant's response with nice formatting."""
        console.print(f"\n[bold blue]{participant.name}[/bold blue] is thinking...")
        
        full_response = []
        async for token in participant.process(prompt):
            full_response.append(token)
            console.print(token, end="")
            yield token
        
        response = "".join(full_response)
        self.discussion_history.append(
            Message(role="assistant", content=response, name=participant.name)
        )
    
    async def _conduct_round(self, round_num: int) -> AsyncIterator[tuple[bool, str]]:
        """Conduct one round of discussion."""
        console.print(f"\n[bold yellow]Round {round_num}[/bold yellow]")
        
        # Get each participant's response
        for participant in self.participants:
            context = "\n".join(f"{m.name}: {m.content}" for m in self.discussion_history[-3:])
            prompt = f"Based on the previous discussion:\n{context}\nWhat are your thoughts?"
            async for token in self._stream_response(participant, prompt):
                yield False, token
        
        # Get judge's assessment
        context = "\n".join(f"{m.name}: {m.content}" for m in self.discussion_history)
        response_tokens = []
        async for token in self._stream_response(self.judge, context):
            response_tokens.append(token)
            yield token.strip().startswith("VERDICT:"), token
    
    async def discuss(self, case_study: str) -> AsyncIterator[str]:
        """
        Conduct the discussion about the given case study.
        
        Args:
            case_study: The case to be discussed
            
        Yields:
            Discussion progress and final verdict
        """
        # Initial prompt
        prompt = self._format_case_prompt(case_study)
        self.discussion_history.append(Message(role="system", content=prompt))
        
        # Initial responses
        for participant in self.participants:
            async for token in self._stream_response(participant, prompt):
                yield token
        
        # Discussion rounds
        verdict_reached = False
        for round_num in range(1, self.max_rounds + 1):
            async for verdict, token in self._conduct_round(round_num):
                yield token
                if verdict:
                    verdict_reached = True
                    break
            if verdict_reached:
                break
        
        # Final verdict if not reached
        if not verdict_reached:
            final_context = "\n".join(f"{m.name}: {m.content}" for m in self.discussion_history)
            async for token in self._stream_response(
                self.judge,
                f"{final_context}\n\nPlease provide your final verdict now."
            ):
                yield token

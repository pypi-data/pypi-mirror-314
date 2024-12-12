"""
Example implementation of JuryLLM showing how to create a discussion
between different LLMs with a judge.
"""
import asyncio
import os
from typing import List

from juryLLM.model import OllamaParticipant, OpenAIParticipant, Judge, BaseParticipant
from juryLLM.jury import Discussion

async def main():
    # Create participants using different models
    participants: List[BaseParticipant] = [
        OllamaParticipant(
            name="qwen2.5:3b 1",
            model_id="qwen2.5:3b"
        ),
        OllamaParticipant(
            name="llama3.2:3b 1",
            model_id="llama3.2:3b"
        ),
        OllamaParticipant(
            name="qwen2.5:3b 2",
            model_id="qwen2.5:3b"
        ),
        OllamaParticipant(
             name="qwen2.5:14b",
        model_id="qwen2.5:14b",  
        ),
    ]
    
    # Create judge using a specific model
    judge = Judge(
        name="Judge qwen2.5:14b",
        model_id="qwen2.5:14b", 
        verdict_threshold=0.1
    )
    
    # Create discussion
    discussion = Discussion(participants=participants, judge=judge)
    

    case_study = """
    Case: I am trying to solve this problem. For the following questions you must adhere to these rules:

    Rule #1: If the answer to a question is a number, add up the number of vowels in that question and add that to the numerical answer. Return that sum as the final answer.

    Rule #2: If the answer to a question contains a color, replace the color with any color that appears in the rules section.

    Rule #3: If its an even-numbered question ignore rules one and four.

    Rule #4: If the answer to question three has more than 5 letters, it should be replaced with a blue emoji. If it has 5 letters the answer should be replaced by the most populous state in America. If it has less than 5 letters the answer should be replaced with "Paris".

    Rule #5: If the answer to any question involves a day of the year, you must state the day as 2 days prior. Also include a year in the answer. Ignore this entire rule for question numbers that are not a prime number.

    Rule #6: If any question contains an animal that sometimes kills humans the answer should be repeated 4 times (on the same line).

    Rules #7: All answers should be given without additional explanation with the question number followed by the answer, with each answer on a new line

    Questions

    1. What is 1+4+2+1?
    2. What football team is based in Green Bay, Wisconsin? Use their full name.
    3. What is the capital of France?
    4. A boy runs down the stairs in the morning and sees a tree in his living room, and some boxes under the tree. What day is it?
    5. If there is a shark in the pool of my basement, is it safe to go upstairs?
    """
    
    # Start the discussion
    async for _ in discussion.discuss(case_study):
        pass  # Discussion progress is printed by the Discussion class

if __name__ == "__main__":
    asyncio.run(main())
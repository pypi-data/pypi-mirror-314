"""
JuryLLM: A framework for collaborative language model decision-making
"""

__version__ = "0.1.0"
__author__ = "Sujith"

from .model import BaseParticipant, OllamaParticipant, OpenAIParticipant, Judge, Message
from .jury import Discussion

__all__ = [
    "BaseParticipant",
    "OllamaParticipant",
    "OpenAIParticipant",
    "Judge",
    "Message",
    "Discussion"
]

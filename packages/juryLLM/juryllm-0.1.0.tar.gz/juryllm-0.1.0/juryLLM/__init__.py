"""
JuryLLM: A framework for collaborative language model decision-making
"""

__version__ = "0.1.0"
__author__ = "Sujith"

from .jury import Jury
from .model import JuryMember

__all__ = ["Jury", "JuryMember"]

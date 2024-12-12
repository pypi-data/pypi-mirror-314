"""
Base class for jury members (individual language models).
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class JuryMember(ABC):
    def __init__(self, name: str, model_id: str, **kwargs: Any):
        """
        Initialize a jury member.
        
        Args:
            name: Name of the jury member
            model_id: Identifier for the model (e.g., HuggingFace model ID)
            **kwargs: Additional configuration parameters
        """
        self.name = name
        self.model_id = model_id
        self.config = kwargs
        
    @abstractmethod
    def process(self, prompt: str, **kwargs: Any) -> Dict[str, Any]:
        """
        Process the input prompt and return response.
        
        Args:
            prompt: Input text to process
            **kwargs: Additional processing parameters
            
        Returns:
            Dictionary containing the response and any metadata
        """
        pass
    
    @abstractmethod
    def load_model(self) -> None:
        """Load the underlying model."""
        pass
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, model_id={self.model_id})"

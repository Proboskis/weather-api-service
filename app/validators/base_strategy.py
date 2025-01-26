# File: app/validators/base_strategy.py

from abc import ABC, abstractmethod

class ValidationStrategy(ABC):
    """Abstract base for any validation strategy."""
    
    @abstractmethod
    def validate(self, city: str) -> None:
        """Raise an exception or return if valid."""
        pass

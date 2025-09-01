from abc import ABC, abstractmethod


class ComplementBase(ABC):
    """Complement Base class."""

    @abstractmethod
    def build_complement(self):
        """Method for concreete implementation."""

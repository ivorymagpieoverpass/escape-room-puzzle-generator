"""LLMBackend protocol — the only contract generators may depend on."""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class LLMBackend(Protocol):
    """Minimal surface for text generation + embedding."""

    def generate(self, prompt: str, *, max_tokens: int = 512, temperature: float = 0.8) -> str:
        """Return generated text. Must not raise on empty prompt."""
        ...

    def embed(self, texts: list[str]) -> list[list[float]]:
        """Return one embedding vector per input text, same order."""
        ...

    def health(self) -> bool:
        """True if the backend is ready to serve requests."""
        ...
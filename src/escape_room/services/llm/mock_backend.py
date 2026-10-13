"""MockBackend — deterministic, no-model stub for tests and CI."""

from __future__ import annotations

import hashlib
import math


class MockBackend:
    """Deterministic backend. Same prompt => same output, always."""

    def generate(self, prompt: str, *, max_tokens: int = 512, temperature: float = 0.8) -> str:
        digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
        return f"[mock:{digest[:8]}] {prompt[:120]}"

    def embed(self, texts: list[str]) -> list[list[float]]:
        out: list[list[float]] = []
        for t in texts:
            h = hashlib.sha256(t.encode("utf-8")).digest()
            vec = [(b - 128) / 128.0 for b in h[:32]]
            norm = math.sqrt(sum(x * x for x in vec)) or 1.0
            out.append([x / norm for x in vec])
        return out

    def health(self) -> bool:
        return True
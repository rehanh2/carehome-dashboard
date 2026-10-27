from typing import Protocol


class Embedder(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]:
        """Turn each text into a vector."""
        ...
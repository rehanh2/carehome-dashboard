from typing import Protocol

from app.domain.notes import Note


class NoteRepository(Protocol):
    def save(self, note: Note) -> Note: ...

    def save_chunks(self, note_id: int, chunks: list[str], embeddings: list[list[float]]) -> None: ...

    def set_embedding_status(self, note_id: int, status: str) -> None: ...
from typing import Protocol

from app.domain.notes import Note


class NoteRepository(Protocol):
    def save(self, note: Note) -> Note:
        """Store a note and return it with its new id."""
        ...
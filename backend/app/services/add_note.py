from app.domain.notes import Note
from app.ports.note_repository import NoteRepository


def add_note(note: Note, repo: NoteRepository) -> Note:
    return repo.save(note)
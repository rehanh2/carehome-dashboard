from app.domain.notes import Note, Category, Shift
from app.services.add_note import add_note


class FakeNoteRepository:
    def __init__(self):
        self.notes = []

    def save(self, note):
        note.id = len(self.notes) + 1
        self.notes.append(note)
        return note


def test_add_note_saves_and_assigns_id():
    repo = FakeNoteRepository()
    note = Note(resident_id=1, employee_id=1, category=Category.INCIDENT,
                shift=Shift.DAY, content="Fell in bathroom, no injury")

    saved = add_note(note, repo)

    assert saved.id == 1
    assert len(repo.notes) == 1
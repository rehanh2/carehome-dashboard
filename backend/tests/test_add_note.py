from app.domain.notes import Category, Note, Shift
from app.services.add_note import add_note
from tests.fakes import FakeNoteRepository


def test_add_note_saves_and_assigns_id():
    repo = FakeNoteRepository()
    note = Note(resident_id=1, employee_id=1, category=Category.INCIDENT,
                shift=Shift.DAY, content="Fell in bathroom, no injury")

    saved = add_note(note, repo)

    assert saved.id == 1
    assert len(repo.notes) == 1

import pytest

from app.domain.notes import Category, Note, Shift


def make_note(**overrides):
    fields = dict(resident_id=1, employee_id=1, category=Category.INCIDENT,
                  shift=Shift.DAY, content="Fell in bathroom, no injury")
    fields.update(overrides)
    return Note(**fields)


def test_valid_note_has_defaults():
    note = make_note()
    assert note.id is None
    assert note.source == "typed"
    assert note.created_at is not None


@pytest.mark.parametrize("content", ["", "   ", "\n\t"])
def test_empty_or_blank_content_is_rejected(content):
    with pytest.raises(ValueError):
        make_note(content=content)


def test_category_and_shift_accept_their_string_values():
    assert Category("medication") is Category.MEDICATION
    assert Shift("night") is Shift.NIGHT


def test_unknown_category_is_rejected():
    with pytest.raises(ValueError):
        Category("banana")

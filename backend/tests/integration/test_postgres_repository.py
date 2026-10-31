"""Integration tests: the real Postgres adapter against a real (separate) test database.

Skipped unless TEST_DATABASE_URL is set, e.g.
    createdb carehome_test
    psql carehome_test -c "CREATE EXTENSION IF NOT EXISTS vector;"
    TEST_DATABASE_URL=postgresql://rehan@localhost:5432/carehome_test python3 -m pytest
Never point this at carehome_demo: every test wipes and rebuilds the tables.
"""
import os
from pathlib import Path

import psycopg
import pytest

from app.adapters.db.postgres_note_repository import PostgresNoteRepository
from app.domain.notes import Category, Note, Shift

TEST_DB = os.environ.get("TEST_DATABASE_URL")
DB_DIR = Path(__file__).resolve().parents[2] / "db"

pytestmark = pytest.mark.skipif(not TEST_DB, reason="TEST_DATABASE_URL not set")


@pytest.fixture
def repo():
    with psycopg.connect(TEST_DB) as conn:
        conn.execute("DROP TABLE IF EXISTS note_chunks CASCADE")
        conn.execute((DB_DIR / "schema.sql").read_text())
        conn.execute((DB_DIR / "002_note_chunks.sql").read_text())
    return PostgresNoteRepository(TEST_DB)


def make_note(**overrides):
    fields = dict(resident_id=1, employee_id=1, category=Category.INCIDENT,
                  shift=Shift.DAY, content="Fell in bathroom, no injury")
    fields.update(overrides)
    return Note(**fields)


def query(sql, params=()):
    with psycopg.connect(TEST_DB) as conn:
        return conn.execute(sql, params).fetchall()


def test_save_returns_the_note_with_database_id(repo):
    # Regression: save() once lost its `return note` and the API crashed with a 500.
    saved = repo.save(make_note())

    assert isinstance(saved, Note)
    assert saved.id is not None
    assert saved.created_at is not None


def test_saved_note_is_stored_as_pending(repo):
    saved = repo.save(make_note(category=Category.MEDICATION, shift=Shift.NIGHT))

    rows = query("SELECT category, shift, embedding_status FROM notes WHERE id = %s", (saved.id,))
    assert rows == [("medication", "night", "pending")]


def test_unknown_resident_is_rejected_by_foreign_key(repo):
    with pytest.raises(psycopg.errors.ForeignKeyViolation):
        repo.save(make_note(resident_id=999))


def test_save_chunks_stores_1536_dimension_vectors(repo):
    note = repo.save(make_note())
    vector = [0.01] * 1536

    repo.save_chunks(note.id, ["chunk one", "chunk two"], [vector, vector])

    rows = query(
        "SELECT chunk_index, content, vector_dims(embedding) FROM note_chunks "
        "WHERE note_id = %s ORDER BY chunk_index", (note.id,))
    assert rows == [(0, "chunk one", 1536), (1, "chunk two", 1536)]


def test_saving_chunks_again_overwrites_instead_of_duplicating(repo):
    note = repo.save(make_note())
    repo.save_chunks(note.id, ["old text"], [[0.01] * 1536])

    repo.save_chunks(note.id, ["new text"], [[0.02] * 1536])

    assert query("SELECT content FROM note_chunks WHERE note_id = %s", (note.id,)) == [("new text",)]


def test_set_embedding_status_updates_the_note(repo):
    note = repo.save(make_note())

    repo.set_embedding_status(note.id, "done")

    assert query("SELECT embedding_status FROM notes WHERE id = %s", (note.id,)) == [("done",)]


def test_invalid_status_is_rejected_by_check_constraint(repo):
    note = repo.save(make_note())

    with pytest.raises(psycopg.errors.CheckViolation):
        repo.set_embedding_status(note.id, "maybe")


def test_deleting_a_note_deletes_its_chunks(repo):
    note = repo.save(make_note())
    repo.save_chunks(note.id, ["chunk"], [[0.01] * 1536])

    query_conn = psycopg.connect(TEST_DB)
    with query_conn:
        query_conn.execute("DELETE FROM notes WHERE id = %s", (note.id,))

    assert query("SELECT count(*) FROM note_chunks WHERE note_id = %s", (note.id,)) == [(0,)]

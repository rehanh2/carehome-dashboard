import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.adapters.api.notes_routes import create_notes_router
from tests.fakes import BrokenEmbedder, FakeEmbedder, FakeNoteRepository

VALID_BODY = {
    "resident_id": 1,
    "employee_id": 2,
    "category": "medication",
    "shift": "night",
    "content": "Refused evening meds, GP informed",
}


def make_client(embedder=None):
    repo = FakeNoteRepository()
    app = FastAPI()
    app.include_router(create_notes_router(repo, embedder or FakeEmbedder()))
    return TestClient(app), repo


def test_post_valid_note_returns_201_with_id():
    client, repo = make_client()

    response = client.post("/notes", json=VALID_BODY)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["content"] == VALID_BODY["content"]
    assert len(repo.notes) == 1


def test_post_note_triggers_background_embedding():
    client, repo = make_client()

    client.post("/notes", json=VALID_BODY)

    assert repo.statuses[1] == "done"


def test_note_is_saved_even_if_embedding_fails():
    client, repo = make_client(BrokenEmbedder())

    response = client.post("/notes", json=VALID_BODY)

    assert response.status_code == 201
    assert repo.statuses[1] == "failed"


@pytest.mark.parametrize("field, bad_value", [
    ("category", "banana"),
    ("shift", "evening"),
    ("resident_id", "abc"),
    ("content", ""),
    ("content", "   "),
])
def test_invalid_input_returns_422_and_saves_nothing(field, bad_value):
    client, repo = make_client()

    response = client.post("/notes", json={**VALID_BODY, field: bad_value})

    assert response.status_code == 422
    assert repo.notes == []


def test_missing_field_returns_422():
    client, _ = make_client()
    body = {k: v for k, v in VALID_BODY.items() if k != "content"}

    assert client.post("/notes", json=body).status_code == 422

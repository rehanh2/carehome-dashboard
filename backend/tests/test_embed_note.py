from app.domain.notes import Category, Note, Shift
from app.services.embed_note import embed_note
from tests.fakes import BrokenEmbedder, FakeEmbedder, FakeNoteRepository


def saved_note(repo, content="Refused breakfast, seemed low in mood"):
    note = Note(resident_id=1, employee_id=2, category=Category.WELLBEING,
                shift=Shift.DAY, content=content)
    return repo.save(note)


def test_successful_embedding_stores_chunks_and_marks_done():
    repo, embedder = FakeNoteRepository(), FakeEmbedder()
    note = saved_note(repo)

    embed_note(note, repo, embedder)

    assert repo.statuses[note.id] == "done"
    assert len(repo.chunks[note.id]) == 1
    assert repo.chunks[note.id][0][0] == note.content


def test_all_chunks_are_embedded_in_one_call():
    repo, embedder = FakeNoteRepository(), FakeEmbedder()
    long_text = " ".join(f"word{i}" for i in range(150))
    note = saved_note(repo, content=long_text)

    embed_note(note, repo, embedder)

    assert len(embedder.calls) == 1
    assert len(repo.chunks[note.id]) == len(embedder.calls[0]) > 1


def test_embedding_failure_marks_failed_and_keeps_the_note():
    repo = FakeNoteRepository()
    note = saved_note(repo)

    embed_note(note, repo, BrokenEmbedder())  # must not raise

    assert repo.statuses[note.id] == "failed"
    assert note.id not in repo.chunks
    assert repo.notes == [note]

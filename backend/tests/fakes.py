"""In-memory stand-ins for the ports, so tests run without Postgres or OpenAI."""


class FakeNoteRepository:
    def __init__(self):
        self.notes = []
        self.chunks = {}
        self.statuses = {}

    def save(self, note):
        note.id = len(self.notes) + 1
        self.notes.append(note)
        self.statuses[note.id] = "pending"
        return note

    def save_chunks(self, note_id, chunks, embeddings):
        self.chunks[note_id] = list(zip(chunks, embeddings))

    def set_embedding_status(self, note_id, status):
        self.statuses[note_id] = status


class FakeEmbedder:
    """Returns a tiny fixed-size vector per text and records what it was asked to embed."""

    def __init__(self):
        self.calls = []

    def embed(self, texts):
        self.calls.append(texts)
        return [[float(len(t)), 0.0, 1.0] for t in texts]


class BrokenEmbedder:
    """Simulates the embedding API being down."""

    def embed(self, texts):
        raise RuntimeError("embedding service unavailable")

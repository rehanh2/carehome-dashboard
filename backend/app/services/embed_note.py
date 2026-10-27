import logging

from app.domain.chunking import split_into_chunks
from app.domain.notes import Note
from app.ports.embedder import Embedder
from app.ports.note_repository import NoteRepository

logger = logging.getLogger(__name__)


def embed_note(note: Note, repo: NoteRepository, embedder: Embedder) -> None:
    try:
        chunks = split_into_chunks(note.content)
        vectors = embedder.embed(chunks)
        repo.save_chunks(note.id, chunks, vectors)
        repo.set_embedding_status(note.id, "done")
    except Exception:
        logger.exception("Embedding failed for note %s", note.id)
        repo.set_embedding_status(note.id, "failed")
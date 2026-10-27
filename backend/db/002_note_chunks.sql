CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS note_chunks (
    id           SERIAL PRIMARY KEY,
    note_id      INT NOT NULL REFERENCES notes(id) ON DELETE CASCADE,
    chunk_index  INT NOT NULL,
    content      TEXT NOT NULL,
    embedding    vector(1536) NOT NULL,
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (note_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS note_chunks_embedding_idx
    ON note_chunks USING hnsw (embedding vector_cosine_ops);
import psycopg

from app.domain.notes import Note


class PostgresNoteRepository:
    def __init__(self, conninfo: str):
        self.conninfo = conninfo

    def save(self, note: Note) -> Note:
        with psycopg.connect(self.conninfo) as conn:
            row = conn.execute(
                """
                INSERT INTO notes (resident_id, employee_id, category, shift, content, source)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id, created_at
                """,
                (note.resident_id, note.employee_id, note.category.value,
                 note.shift.value, note.content, note.source),
            ).fetchone()
        note.id, note.created_at = row
        return note

    def save_chunks(self, note_id, chunks, embeddings):
        with psycopg.connect(self.conninfo) as conn:
            for i, (chunk, vector) in enumerate(zip(chunks, embeddings)):
                conn.execute(
                    """
                    INSERT INTO note_chunks (note_id, chunk_index, content, embedding)
                    VALUES (%s, %s, %s, %s::vector)
                    ON CONFLICT (note_id, chunk_index)
                    DO UPDATE SET content = EXCLUDED.content, embedding = EXCLUDED.embedding
                    """,
                    (note_id, i, chunk, str(vector)),
                )

    def set_embedding_status(self, note_id, status):
        with psycopg.connect(self.conninfo) as conn:
            conn.execute(
                "UPDATE notes SET embedding_status = %s WHERE id = %s",
                (status, note_id),
            )
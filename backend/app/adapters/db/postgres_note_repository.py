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
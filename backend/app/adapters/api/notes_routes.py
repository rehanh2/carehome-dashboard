from dataclasses import asdict
from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.domain.notes import Note, Category, Shift
from app.ports.note_repository import NoteRepository
from app.services.add_note import add_note


class NoteIn(BaseModel):
    resident_id: int
    employee_id: int
    category: Category
    shift: Shift
    content: str = Field(min_length=1)


class NoteOut(BaseModel):
    id: int
    resident_id: int
    employee_id: int
    category: Category
    shift: Shift
    content: str
    source: str
    created_at: datetime


def create_notes_router(repo: NoteRepository) -> APIRouter:
    router = APIRouter()

    @router.post("/notes", status_code=status.HTTP_201_CREATED, response_model=NoteOut)
    def create_note(body: NoteIn):
        try:
            note = Note(**body.model_dump())
        except ValueError as e:
            raise HTTPException(status_code=422, detail=str(e))
        saved = add_note(note, repo)
        return NoteOut(**asdict(saved))

    return router
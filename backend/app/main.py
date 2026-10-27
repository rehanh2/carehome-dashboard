from fastapi.middleware.cors import CORSMiddleware
import os

from dotenv import load_dotenv
from fastapi import FastAPI

from app.adapters.api.notes_routes import create_notes_router
from app.adapters.db.postgres_note_repository import PostgresNoteRepository

from app.adapters.llm.openai_embedder import OpenAIEmbedder

load_dotenv()

repo = PostgresNoteRepository(os.environ["DATABASE_URL"])

app = FastAPI(title="Carehome Dashboard API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)
embedder = OpenAIEmbedder(os.environ["OPENAI_API_KEY"])
app.include_router(create_notes_router(repo, embedder))
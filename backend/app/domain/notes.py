from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Category(str, Enum):
    INCIDENT = "incident"
    MEDICATION = "medication"
    WELLBEING = "wellbeing"
    NUTRITION = "nutrition"
    GENERAL = "general"


class Shift(str, Enum):
    DAY = "day"
    NIGHT = "night"


@dataclass
class Note:
    resident_id: int
    employee_id: int
    category: Category
    shift: Shift
    content: str
    source: str = "typed"
    id: int | None = None
    created_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.content.strip():
            raise ValueError("Note content can't be empty")
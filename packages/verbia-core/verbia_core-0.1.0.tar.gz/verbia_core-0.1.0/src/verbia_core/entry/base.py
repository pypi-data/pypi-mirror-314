import uuid
from dataclasses import dataclass, field

from langcodes import Language

from verbia_core.utils import time_provider


@dataclass
class Entry:
    word: str
    native_language: Language
    native_language_definition: str
    source: str
    is_new: bool
    word_language: Language

    example_sentences: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    created_at: int = time_provider.time_mills_from_now()
    next_review_at: int = time_provider.time_mills_from_now(interval_days=1)
    review_interval_days: int = 1
    interval: int = 1
    repetitions: int = 0
    quality: int = 0
    ease_factor: float = 2.5
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    vocabulary_id: str = ""

from dataclasses import dataclass

from langcodes import Language

from verbia_core.entry.base import Entry


@dataclass
class Forms:
    past_tense: str | None = None
    present_participle: str | None = None
    past_participle: str | None = None
    third_person_singular: str | None = None
    singular: str | None = None
    plural: str | None = None
    comparative: str | None = None
    superlative: str | None = None


@dataclass
class EnglishEntry(Entry):
    word_language: Language = Language.get("en")
    lemma: str | None = None
    forms: Forms | None = None
    pronunciation: str | None = None

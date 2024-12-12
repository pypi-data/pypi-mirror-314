from dataclasses import dataclass

from langcodes import Language

from verbia_core.entry.base import Entry


@dataclass()
class Conjugation:
    present: str | None = None
    past: str | None = None
    negative: str | None = None
    te_form: str | None = None
    potential: str | None = None
    polite: str | None = None


@dataclass
class JapaneseReading:
    hiragana: str | None = None
    katakana: str | None = None
    kunyomi: str | None = None
    onyomi: str | None = None


@dataclass
class JapaneseEntry(Entry):
    word_language: Language = Language.get("ja")
    reading: JapaneseReading | None = None
    conjugation: Conjugation | None = None

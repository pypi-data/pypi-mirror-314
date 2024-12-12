from langcodes import Language

from verbia_core.dictionary.gemini.dictionary import GeminiDictionary
from verbia_core.entry import EnglishEntry, JapaneseEntry


def test_lookup_en():
    dictionary = GeminiDictionary()
    entry = dictionary.lookup(
        word="go",
        word_language=Language.get("en"),
        native_language=Language.get("zh"),
    )
    assert entry.word == "go"
    assert entry.word_language == Language.get("en")
    assert entry.native_language == Language.get("zh")
    assert entry.is_new is True
    assert entry.source == "Gemini"
    assert isinstance(entry, EnglishEntry)
    assert entry.lemma == "go"
    assert entry.forms.past_tense == "went"
    assert entry.forms.past_participle == "gone"
    assert entry.forms.present_participle == "going"
    assert entry.forms.third_person_singular == "goes"


def test_lookup_ja():
    dictionary = GeminiDictionary()
    entry = dictionary.lookup(
        word="勉強",
        word_language=Language.get("ja"),
        native_language=Language.get("en"),
    )
    assert entry.word == "勉強"
    assert entry.word_language == Language.get("ja")
    assert entry.native_language == Language.get("en")
    assert entry.is_new is True
    assert entry.source == "Gemini"
    assert isinstance(entry, JapaneseEntry)
    assert "べんきょう" in entry.reading.hiragana
    assert "勉強する" in entry.conjugation.present
    assert "勉強した" in entry.conjugation.past
    assert "勉強します" in entry.conjugation.polite
    assert "勉強しない" in entry.conjugation.negative
    assert "勉強して" in entry.conjugation.te_form
    assert "勉強できる" in entry.conjugation.potential

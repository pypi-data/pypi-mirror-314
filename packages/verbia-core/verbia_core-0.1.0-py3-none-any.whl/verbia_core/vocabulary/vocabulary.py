from abc import abstractmethod, ABC

from langcodes import Language
from loguru import logger

from verbia_core.dictionary import DictionaryBase
from verbia_core.entry import EnglishEntry, Entry
from verbia_core.error import VerbiaError
from verbia_core.vocabulary.review import ReviewStrategy
from verbia_core.vocabulary.storage import EntryStorageBase


class Vocabulary(ABC):
    def __init__(
        self,
        id: str,
        name: str,
        word_language: Language,
        native_language: Language,
    ):
        self.id = id
        self.name = name
        self.word_language = word_language
        self.native_language = native_language

    def __str__(self):
        return f"Vocabulary(id={self.id}, name={self.name}, word_language={self.word_language}, native_language={self.native_language})"

    @property
    @abstractmethod
    def _entry_storage(self) -> EntryStorageBase:
        pass

    @property
    @abstractmethod
    def _dictionary(self) -> DictionaryBase:
        pass

    @property
    @abstractmethod
    def _review_strategy(self) -> ReviewStrategy:
        pass

    @abstractmethod
    def self_delete(self):
        pass

    def _lookup_word(self, word: str) -> Entry | None:
        logger.trace(f"Looking up word '{word}' in the dictionary")
        entry = self._dictionary.lookup(word, self.word_language, self.native_language)
        if not entry:
            raise VerbiaError(f"Word '{word}' does not exist in the dictionary.")
        entry.vocabulary_id = self.id

        return entry

    def add_word(self, word: str) -> Entry:
        logger.trace(f"Adding word '{word}' to vocabulary '{self.name}'")
        entry = self.get_entry(word)
        if not entry:
            entry = self._lookup_word(word)
            self.add_or_update_entry(entry)

        self._add_lemma_if_applicable(entry, word)
        return entry

    def _add_lemma_if_applicable(self, entry: Entry, word: str):
        if entry.is_new and isinstance(entry, EnglishEntry):
            en_entry: EnglishEntry = entry
            lemma = en_entry.lemma
            try:
                if lemma is not None and lemma != word:
                    self.add_word(lemma)
            except VerbiaError:
                pass

    def get_entry(self, word: str) -> Entry | None:
        logger.trace(f"Getting entry for word '{word}' from vocabulary '{self.name}'")
        entry = self._entry_storage.get(word, self.id)
        return entry

    def add_or_update_entry(self, entry: Entry):
        self._entry_storage.add_or_update(entry)

    def delete_entry(self, entry: Entry):
        self._entry_storage.delete(entry)

    def list_all_entries(self) -> list[Entry]:
        return self._entry_storage.list_all(self.id)

    def update_review(self, entry: Entry, quality: int):
        entry = self._review_strategy.update_review(entry, quality)
        self.add_or_update_entry(entry)

    def list_all_due_entries(self) -> list[Entry]:
        return self._entry_storage.list_all_due(self.id)

    async def async_get_entry(self, word: str) -> Entry | None:
        entry = await self._entry_storage.async_get(word, self.id)
        return entry

    async def async_lookup_word(self, word: str) -> Entry:
        entry = await self._dictionary.async_lookup(word, self.word_language, self.native_language)
        if not entry:
            raise VerbiaError(f"Word '{word}' does not exist in the dictionary.")
        entry.vocabulary_id = self.id

        return entry

    async def async_add_word(self, word: str):
        entry = await self.async_get_entry(word)
        if not entry:
            entry = await self.async_lookup_word(word)
            await self._entry_storage.async_add_or_update(entry)

        if entry.is_new and isinstance(entry, EnglishEntry):
            # Add lemma to vocabulary if it is different from the word, only for English words.
            en_entry: EnglishEntry = entry
            lemma = en_entry.lemma
            try:
                if lemma is not None and lemma != word:
                    await self.async_add_word(lemma)
            except VerbiaError:
                pass
        return entry

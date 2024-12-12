from abc import ABC, abstractmethod

from langcodes import Language

from verbia_core.entry import Entry


class DictionaryBase(ABC):
    def __init__(self, source: str):
        self._source = source

    @abstractmethod
    def lookup(
        self, word: str, word_language: Language, native_language: Language
    ) -> Entry:
        pass

    @abstractmethod
    async def async_lookup(
        self, word: str, word_language: Language, native_language: Language
    ) -> Entry:
        pass

from verbia_core.dictionary.base import DictionaryBase
from verbia_core.dictionary.gemini.dictionary import GeminiDictionary


class DictionaryFactory:
    _dictionaries = {
        "Gemini": GeminiDictionary,
    }

    @classmethod
    def create(cls, dictionary_name: str, **kwargs) -> DictionaryBase:
        dictionary_cls = cls._dictionaries.get(dictionary_name)
        if not dictionary_cls:
            raise ValueError(f"Dictionary '{dictionary_name}' not found.")
        return dictionary_cls(**kwargs)

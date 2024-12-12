from abc import ABC, abstractmethod

from verbia_core.entry import Entry


class EntryStorageBase(ABC):
    @abstractmethod
    def get(self, word: str, vocabulary_id: str) -> Entry | None:
        pass

    @abstractmethod
    def add_or_update(self, entry: Entry):
        pass

    @abstractmethod
    def delete(self, entry: Entry):
        pass

    @abstractmethod
    def list_all(self, vocabulary_id: str) -> list[Entry]:
        pass

    @abstractmethod
    def list_all_due(self, vocabulary_id) -> list[Entry]:
        pass

    @abstractmethod
    async def async_add_or_update(self, entry: Entry):
        pass

    @abstractmethod
    async def async_get(self, word: str, vocabulary_id: str) -> Entry | None:
        pass

    @abstractmethod
    def delete_by_vocabulary_id(self, vocabulary_id: str):
        pass

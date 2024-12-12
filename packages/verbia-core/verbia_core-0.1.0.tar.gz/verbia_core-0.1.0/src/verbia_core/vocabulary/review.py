from abc import ABC, abstractmethod

from verbia_core.entry import Entry
from verbia_core.utils import time_provider


class ReviewStrategy(ABC):
    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def update_review(self, entry: Entry, quality: int) -> Entry:
        raise NotImplementedError


class SM2ReviewStrategy(ReviewStrategy):
    def __init__(self):
        super().__init__("SM2")

    def update_review(self, entry: Entry, quality: int) -> Entry:
        entry.ease_factor += 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)
        entry.ease_factor = max(entry.ease_factor, 1.3)  # 确保易度因子不小于 1.3

        if entry.repetitions == 0:
            entry.interval = 1
        elif entry.repetitions == 1:
            entry.interval = 6
        else:
            entry.interval = round(entry.interval * entry.ease_factor)

        entry.next_review_date = time_provider.time_mills_from_now(entry.interval)
        entry.repetitions += 1

        return entry


class ReviewStrategyFactory:
    _strategies = {
        "SM2": SM2ReviewStrategy,
    }

    @classmethod
    def create(cls, strategy_name: str) -> ReviewStrategy:
        strategy_cls = cls._strategies.get(strategy_name)
        if strategy_cls is None:
            raise ValueError(f"Unknown review strategy: {strategy_name}")
        return strategy_cls()

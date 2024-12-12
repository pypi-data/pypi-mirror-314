from unittest.mock import MagicMock, patch, PropertyMock, AsyncMock

import pytest
from langcodes import Language

from verbia_core.entry import Entry
from verbia_core.error import VerbiaError
from verbia_core.vocabulary import Vocabulary


class FakeVocabulary(Vocabulary):
    @property
    def _entry_storage(self):
        return MagicMock()

    @property
    def _dictionary(self):
        return MagicMock()

    @property
    def _review_strategy(self):
        return MagicMock()

    def self_delete(self):
        pass


@pytest.fixture
def mock_vocabulary():
    vocab = FakeVocabulary(
        id="vocab1",
        name="Test Vocabulary",
        word_language=Language.get("en"),
        native_language=Language.get("fr"),
    )
    return vocab


@pytest.fixture
def mock_entry():
    return Entry(
        word="test",
        native_language=Language.get("fr"),
        word_language=Language.get("en"),
        source="Gemini",
        is_new=False,
        native_language_definition="test definition",
        vocabulary_id="vocab1",
    )


@patch.object(FakeVocabulary, "_entry_storage", new_callable=PropertyMock)
def test_add_word_existing_entry(_entry_storage, mock_vocabulary, mock_entry):
    mock_entry_storage = MagicMock()
    mock_entry_storage.get.return_value = mock_entry
    _entry_storage.return_value = mock_entry_storage

    result = mock_vocabulary.add_word("test")

    assert result == mock_entry

    mock_entry_storage.get.assert_called_once_with(mock_entry.word, mock_vocabulary.id)
    mock_entry_storage.add_or_update.assert_not_called()


@patch.object(FakeVocabulary, "_entry_storage", new_callable=PropertyMock)
@patch.object(FakeVocabulary, "_dictionary", new_callable=PropertyMock)
def test_add_word_new_entry(_dictionary, _entry_storage, mock_vocabulary, mock_entry):
    mock_entry_storage = MagicMock()
    mock_dictionary = MagicMock()
    _entry_storage.return_value = mock_entry_storage
    _dictionary.return_value = mock_dictionary
    mock_entry_storage.get.return_value = None
    mock_dictionary.lookup.return_value = mock_entry

    result = mock_vocabulary.add_word("test")

    assert result == mock_entry
    mock_entry_storage.get.assert_called_once_with(mock_entry.word, mock_vocabulary.id)
    mock_entry_storage.add_or_update.assert_called_once_with(mock_entry)
    mock_dictionary.lookup.assert_called_once_with(
        mock_entry.word, mock_entry.word_language, mock_entry.native_language
    )


@patch.object(FakeVocabulary, "_entry_storage", new_callable=PropertyMock)
@patch.object(FakeVocabulary, "_dictionary", new_callable=PropertyMock)
def test_add_word_raises_error(_dictionary, _entry_storage, mock_vocabulary):
    mock_entry_storage = MagicMock()
    mock_dictionary = MagicMock()
    _entry_storage.return_value = mock_entry_storage
    _dictionary.return_value = mock_dictionary
    mock_entry_storage.get.return_value = None
    mock_dictionary.lookup.return_value = None

    with pytest.raises(
        VerbiaError, match="Word 'unknown' does not exist in the dictionary."
    ):
        mock_vocabulary.add_word("unknown")


@pytest.mark.asyncio
@patch.object(FakeVocabulary, "_entry_storage", new_callable=PropertyMock)
@patch.object(FakeVocabulary, "_dictionary", new_callable=PropertyMock)
async def test_async_add_word_new_entry(
    _dictionary, _entry_storage, mock_vocabulary, mock_entry
):
    mock_entry_storage = AsyncMock()
    mock_dictionary = AsyncMock()
    _entry_storage.return_value = mock_entry_storage
    _dictionary.return_value = mock_dictionary
    mock_entry_storage.async_get.return_value = None
    mock_dictionary.async_lookup.return_value = mock_entry

    result = await mock_vocabulary.async_add_word("test")

    assert result == mock_entry

    mock_entry_storage.async_get.assert_called_once_with(
        mock_entry.word, mock_vocabulary.id
    )
    mock_entry_storage.async_add_or_update.assert_awaited_once_with(mock_entry)
    mock_dictionary.async_lookup.assert_awaited_once_with(
        mock_entry.word, mock_entry.word_language, mock_entry.native_language
    )


@patch.object(FakeVocabulary, "_entry_storage", new_callable=PropertyMock)
@patch.object(FakeVocabulary, "_review_strategy", new_callable=PropertyMock)
def test_update_review(_review_strategy, _entry_storage, mock_vocabulary, mock_entry):
    mock_entry_storage = MagicMock()
    mock_review_strategy = MagicMock()
    _entry_storage.return_value = mock_entry_storage
    _review_strategy.return_value = mock_review_strategy

    updated_entry = Entry(
        word=mock_entry.word,
        native_language=mock_entry.native_language,
        word_language=mock_entry.word_language,
        source=mock_entry.source,
        is_new=mock_entry.is_new,
        native_language_definition=mock_entry.native_language_definition,
        vocabulary_id=mock_entry.vocabulary_id,
        next_review_at=12345,
        repetitions=mock_entry.repetitions + 1,
    )

    mock_review_strategy.update_review.return_value = updated_entry

    mock_vocabulary.update_review(mock_entry, 5)

    mock_review_strategy.update_review.assert_called_once_with(mock_entry, 5)
    mock_entry_storage.add_or_update.assert_called_once_with(updated_entry)

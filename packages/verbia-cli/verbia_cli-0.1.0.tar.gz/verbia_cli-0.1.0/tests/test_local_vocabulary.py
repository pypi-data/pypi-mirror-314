from unittest.mock import patch, MagicMock, PropertyMock

import pytest
from langcodes import Language

from verbia_cli.vocabulary import LocalVocabulary
from verbia_cli.vocabulary_settings import VocabularySettings

# Sample data for testing
TEST_ID = "test123"
TEST_NAME = "Test Vocabulary"
WORD_LANGUAGE = Language.get("en")
NATIVE_LANGUAGE = Language.get("zh")
DICTIONARY_NAME = "Gemini"
REVIEW_STRATEGY_NAME = "SM2"


@pytest.fixture
def test_settings():
    """Fixture to create a VocabularySettings instance."""
    return VocabularySettings(
        id=TEST_ID,
        name=TEST_NAME,
        word_language_code=WORD_LANGUAGE.language,
        native_language_code=NATIVE_LANGUAGE.language,
        dictionary=DICTIONARY_NAME,
        review_strategy=REVIEW_STRATEGY_NAME,
    )


@patch.object(LocalVocabulary, "_settings_storage", new_callable=PropertyMock)
def test_create_vocabulary(_settings_storage, test_settings):
    """Test creating a vocabulary with mocked storage."""
    mock_storage = MagicMock()
    _settings_storage.return_value = mock_storage
    _settings_storage.add_or_update.return_value = test_settings
    vocabulary = LocalVocabulary.create(test_settings)

    assert vocabulary.id == TEST_ID
    assert vocabulary.name == TEST_NAME
    mock_storage.add_or_update.assert_called_once_with(test_settings)


@patch.object(LocalVocabulary, "_settings_storage", new_callable=PropertyMock)
def test_retrieve_by_id(_settings_storage, test_settings):
    """Test retrieving a vocabulary by ID with mocked storage."""
    mock_storage = MagicMock()
    mock_storage.get.return_value = test_settings
    _settings_storage.return_value = mock_storage

    retrieved = LocalVocabulary.retrieve_by_id(TEST_ID)

    assert retrieved is not None
    assert retrieved.id == TEST_ID
    mock_storage.get.assert_called_once_with(TEST_ID)


@patch.object(LocalVocabulary, "_settings_storage", new_callable=PropertyMock)
def test_retrieve_by_name(_settings_storage, test_settings):
    """Test retrieving a vocabulary by name with mocked storage."""
    mock_storage = MagicMock()
    mock_storage.get_by_name.return_value = test_settings
    _settings_storage.return_value = mock_storage

    retrieved = LocalVocabulary.retrieve_by_name(TEST_NAME)

    assert retrieved is not None
    assert retrieved.name == TEST_NAME
    mock_storage.get_by_name.assert_called_once_with(TEST_NAME)


@patch.object(LocalVocabulary, "_settings_storage", new_callable=PropertyMock)
@patch.object(LocalVocabulary, "_entry_storage", new_callable=PropertyMock)
def test_self_delete(_entry_storage, _settings_storage, test_settings):
    """Test deleting a vocabulary and its entries with mocked storage."""
    mock_storage = MagicMock()
    mock_entry_storage = MagicMock()
    _settings_storage.return_value = mock_storage
    _entry_storage.return_value = mock_entry_storage
    _settings_storage.delete.return_value = None
    _entry_storage.delete_by_vocabulary_id.return_value = None

    vocabulary = LocalVocabulary(
        test_settings.id,
        test_settings.name,
        WORD_LANGUAGE,
        NATIVE_LANGUAGE,
        DICTIONARY_NAME,
        REVIEW_STRATEGY_NAME,
    )

    vocabulary.self_delete()

    mock_storage.delete.assert_called_once_with(TEST_ID)
    mock_entry_storage.delete_by_vocabulary_id.assert_called_once_with(TEST_ID)

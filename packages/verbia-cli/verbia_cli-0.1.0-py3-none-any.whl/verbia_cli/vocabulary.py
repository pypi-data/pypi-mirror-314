from __future__ import annotations

import os

import typer
from langcodes import Language
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncEngine

from verbia_cli.common import states
from verbia_cli.config import get_config
from verbia_cli.sqlite import SQLiteEntryStorage, SQLiteVocabularySettingsStorage
from verbia_cli.vocabulary_settings import VocabularySettings
from verbia_core.dictionary import DictionaryFactory, DictionaryBase
from verbia_core.vocabulary import (
    ReviewStrategyFactory,
    EntryStorageBase,
    Vocabulary,
    ReviewStrategy,
)

DB_PATH = os.path.expanduser("~/.verbia/verbia.db")
DB_URL = f"sqlite:///{DB_PATH}"
ASYNC_DB_URL = f"sqlite+aiosqlite:///{DB_PATH}"


class LocalVocabulary(Vocabulary):
    __storage: SQLiteVocabularySettingsStorage | None = None

    def __init__(
        self,
        id: str,
        name: str,
        word_language: Language,
        native_language: Language,
        dictionary_name: str,
        review_strategy_name: str,
    ):
        logger.debug(
            f"Initializing LocalVocabulary with id={id}, name={name}, word_language={word_language}, native_language={native_language}, dictionary_name={dictionary_name}, review_strategy_name={review_strategy_name}"
        )
        self._dictionary_name = dictionary_name
        self._review_strategy_name = review_strategy_name
        self.__dictionary = None
        self.__review_strategy = None
        self.__entry_storage = None
        super().__init__(
            id,
            name,
            word_language,
            native_language,
        )

    @classmethod
    @property
    def _settings_storage(cls) -> SQLiteVocabularySettingsStorage:
        if not cls.__storage:
            logger.debug("Creating storage engine for SQLiteVocabularySettingsStorage")
            engine = create_engine(DB_URL, echo=False)
            cls.__storage = SQLiteVocabularySettingsStorage(engine)
        return cls.__storage

    @property
    def _entry_storage(self) -> EntryStorageBase:
        if not self.__entry_storage:
            logger.debug("Initializing entry storage")
            engine = create_engine(DB_URL, echo=False)
            async_engine = AsyncEngine(
                create_engine(ASYNC_DB_URL, echo=True, future=True)
            )
            self.__entry_storage = SQLiteEntryStorage(engine, async_engine)
        return self.__entry_storage

    @property
    def _review_strategy(self) -> ReviewStrategy:
        if not self.__review_strategy:
            logger.debug(f"Creating review strategy: {self._review_strategy_name}")
            self.__review_strategy = ReviewStrategyFactory.create(
                self._review_strategy_name
            )
        return self.__review_strategy

    @property
    def _dictionary(self) -> DictionaryBase:
        if not self.__dictionary:
            logger.debug(f"Creating dictionary: {self._dictionary_name}")
            match self._dictionary_name:
                case "Gemini" | "gemini":
                    self.__dictionary = DictionaryFactory.create(
                        self._dictionary_name, api_key=get_config("gemini_api_key")
                    )
                case _:
                    DictionaryFactory.create(self._dictionary_name)
        return self.__dictionary

    @classmethod
    def _construct(cls, settings: VocabularySettings):
        return cls(
            settings.id,
            settings.name,
            Language.get(settings.word_language_code),
            Language.get(settings.native_language_code),
            settings.dictionary,
            settings.review_strategy,
        )

    @classmethod
    def list_vocabularies(cls) -> list[Vocabulary]:
        logger.debug("Listing all vocabularies")
        vocabularies = cls._settings_storage.list_all()
        if states["verbose"]:
            typer.echo(f"Found vocabularies: {vocabularies}")

        for settings in vocabularies:
            logger.debug(f"Processing vocabulary settings: {settings}")
            yield cls._construct(settings)

    @classmethod
    def create(cls, settings: VocabularySettings) -> Vocabulary:
        logger.debug(f"Creating vocabulary with settings: {settings}")
        cls._settings_storage.add_or_update(settings)
        vocabulary = cls._construct(settings)
        if states["verbose"]:
            typer.echo(f"Created vocabulary: {vocabulary}")
        return vocabulary

    @classmethod
    def retrieve_by_id(cls, id: str) -> LocalVocabulary | None:
        logger.debug(f"Retrieving settings with id: {id}")
        settings = cls._settings_storage.get(id)
        logger.debug(f"Retrieved settings: {settings}")
        if states["verbose"]:
            typer.echo(f"Retrieved vocabulary settings: {settings}")

        if not settings:
            logger.warning(f"No settings found for id: {id}")
            return None

        return cls._construct(settings)

    @classmethod
    def retrieve_by_name(cls, name: str) -> LocalVocabulary | None:
        logger.debug(f"Retrieving settings by name: {name}")
        settings = cls._settings_storage.get_by_name(name)
        if states["verbose"]:
            typer.echo(f"Retrieved vocabulary settings: {settings}")

        if settings is None:
            logger.debug(f"No settings found for name: {name}")
            return None

        return cls._construct(settings)

    def self_delete(self):
        logger.debug(f"Deleting vocabulary with id: {self.id}")
        self._settings_storage.delete(self.id)
        if states["verbose"]:
            typer.echo(f"Deleted vocabulary: {self}")
        self._entry_storage.delete_by_vocabulary_id(self.id)
        if states["verbose"]:
            typer.echo(f"Deleted entries for vocabulary: {self}")

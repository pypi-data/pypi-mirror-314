import json
from dataclasses import asdict

from langcodes import Language
from sqlalchemy import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlmodel import Session, select, SQLModel

from verbia_cli.sqlite.model import WordEntryItem
from verbia_core.entry import (
    EnglishEntry,
    Forms,
    Entry,
    JapaneseEntry,
    Conjugation,
    JapaneseReading,
)
from verbia_core.utils import time_provider
from verbia_core.vocabulary import EntryStorageBase


def _convert_item_to_entry(item: WordEntryItem) -> Entry:
    en_code = Language.get("en").language
    ja_code = Language.get("ja").language

    id = item.id
    word = item.word
    vocabulary_id = item.vocabulary_id
    word_language = Language.get(item.word_language_code)
    native_language = Language.get(item.native_language_code)
    native_language_definition = item.native_language_definition
    source = item.source
    example_sentences = json.loads(item.example_sentences)
    notes = json.loads(item.notes)
    created_at = item.created_at
    next_review_at = item.next_review_at
    review_interval_days = item.review_interval_days
    interval = item.interval
    repetitions = item.repetitions
    quality = item.quality
    ease_factor = item.ease_factor

    if item.word_language_code == en_code:
        lemma = item.lemma
        forms = Forms(**json.loads(item.forms))
        pronunciation = item.pronunciation
        return EnglishEntry(
            id=id,
            word=word,
            vocabulary_id=vocabulary_id,
            word_language=word_language,
            native_language=native_language,
            native_language_definition=native_language_definition,
            source=source,
            example_sentences=example_sentences,
            notes=notes,
            created_at=created_at,
            next_review_at=next_review_at,
            review_interval_days=review_interval_days,
            interval=interval,
            repetitions=repetitions,
            quality=quality,
            ease_factor=ease_factor,
            lemma=lemma,
            forms=forms,
            pronunciation=pronunciation,
            is_new=False,
        )
    elif item.word_language_code == ja_code:
        reading = JapaneseReading(**json.loads(item.reading))
        conjugation = Conjugation(**json.loads(item.conjugation))
        return JapaneseEntry(
            id=id,
            word=word,
            vocabulary_id=vocabulary_id,
            word_language=word_language,
            native_language=native_language,
            native_language_definition=native_language_definition,
            source=source,
            example_sentences=example_sentences,
            notes=notes,
            created_at=created_at,
            next_review_at=next_review_at,
            review_interval_days=review_interval_days,
            interval=interval,
            repetitions=repetitions,
            quality=quality,
            ease_factor=ease_factor,
            reading=reading,
            conjugation=conjugation,
            is_new=False,
        )
    else:
        return Entry(
            id=id,
            word=word,
            vocabulary_id=vocabulary_id,
            word_language=word_language,
            native_language=native_language,
            native_language_definition=native_language_definition,
            source=source,
            example_sentences=example_sentences,
            notes=notes,
            created_at=created_at,
            next_review_at=next_review_at,
            review_interval_days=review_interval_days,
            interval=interval,
            repetitions=repetitions,
            quality=quality,
            ease_factor=ease_factor,
            is_new=False,
        )


def _convert_entry_to_item(entry: Entry) -> WordEntryItem:
    id = entry.id
    word = entry.word
    vocabulary_id = entry.vocabulary_id
    word_language_code = entry.word_language.language
    native_language_code = entry.native_language.language
    native_language_definition = entry.native_language_definition
    source = entry.source
    created_at = entry.created_at
    next_review_at = entry.next_review_at
    review_interval_days = entry.review_interval_days
    interval = entry.interval
    repetitions = entry.repetitions
    quality = entry.quality
    ease_factor = entry.ease_factor

    if entry.example_sentences:
        example_sentences = json.dumps(entry.example_sentences)
    else:
        example_sentences = "[]"

    if entry.notes:
        notes = json.dumps(entry.notes)
    else:
        notes = "[]"

    lemma = None
    forms = None
    pronunciation = None
    reading = None
    conjugation = None
    if isinstance(entry, EnglishEntry):
        lemma = entry.lemma
        if entry.forms:
            forms = json.dumps(asdict(entry.forms))
        else:
            forms = None
        pronunciation = entry.pronunciation
    elif isinstance(entry, JapaneseEntry):
        reading = json.dumps(asdict(entry.reading))
        conjugation = json.dumps(asdict(entry.conjugation))

    return WordEntryItem(
        id=id,
        word=word,
        vocabulary_id=vocabulary_id,
        word_language_code=word_language_code,
        native_language_code=native_language_code,
        native_language_definition=native_language_definition,
        source=source,
        example_sentences=example_sentences,
        notes=notes,
        created_at=created_at,
        next_review_at=next_review_at,
        review_interval_days=review_interval_days,
        interval=interval,
        repetitions=repetitions,
        quality=quality,
        ease_factor=ease_factor,
        lemma=lemma,
        forms=forms,
        pronunciation=pronunciation,
        reading=reading,
        conjugation=conjugation,
    )


class SQLiteEntryStorage(EntryStorageBase):
    def __init__(self, engine: Engine, async_engine: AsyncEngine):
        SQLModel.metadata.create_all(engine)
        self._engine = engine
        self._async_engine = async_engine

    def get(self, word: str, vocabulary_id: str) -> Entry | None:
        with Session(self._engine) as session:
            statement = (
                select(WordEntryItem)
                .where(WordEntryItem.word == word)
                .where(WordEntryItem.vocabulary_id == vocabulary_id)
            )
            item = session.exec(statement).first()
            if item is None:
                return None
            return _convert_item_to_entry(item)

    def add_or_update(self, entry: Entry):
        with Session(self._engine) as session:
            item = _convert_entry_to_item(entry)
            session.merge(item)
            session.commit()

    def delete(self, entry: Entry):
        with Session(self._engine) as session:
            statement = select(WordEntryItem).where(WordEntryItem.word == entry.word)
            item = session.exec(statement).first()
            if item is not None:
                session.delete(item)
                session.commit()

    def list_all(self, vocabulary_id: str) -> list[Entry]:
        with Session(self._engine) as session:
            statement = select(WordEntryItem).where(
                WordEntryItem.vocabulary_id == vocabulary_id
            )
            items = session.exec(statement).all()
            return [_convert_item_to_entry(item) for item in items]

    def list_all_due(self, vocabulary_id: str) -> list[Entry]:
        due_time = time_provider.last_moment_of_day(1)
        with Session(self._engine) as session:
            statement = (
                select(WordEntryItem)
                .where(WordEntryItem.next_review_at <= due_time)
                .where(WordEntryItem.vocabulary_id == vocabulary_id)
            )
            items = session.exec(statement).all()
            return [_convert_item_to_entry(item) for item in items]

    async def async_add_or_update(self, entry: Entry):
        with AsyncSession(self._async_engine) as session:
            item = _convert_entry_to_item(entry)
            session.merge(item)
            await session.commit()

    async def async_get(self, word: str, vocabulary_id: str) -> Entry | None:
        async with AsyncSession(self._async_engine) as session:
            statement = (
                select(WordEntryItem)
                .where(WordEntryItem.word == word)
                .where(WordEntryItem.vocabulary_id == vocabulary_id)
            )
            result = await session.execute(statement)
            item = result.scalars().first()
            if item is None:
                return None
            return _convert_item_to_entry(item)

    def delete_by_vocabulary_id(self, vocabulary_id: str):
        with Session(self._engine) as session:
            statement = select(WordEntryItem).where(
                WordEntryItem.vocabulary_id == vocabulary_id
            )
            items = session.exec(statement).all()
            for item in items:
                session.delete(item)
            session.commit()

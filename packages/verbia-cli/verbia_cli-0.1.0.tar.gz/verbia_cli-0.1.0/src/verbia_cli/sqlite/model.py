import uuid

from sqlmodel import SQLModel, Field

from verbia_core.utils import time_provider


class WordEntryItem(SQLModel, table=True):
    id: str = Field(
        primary_key=True, nullable=False, default_factory=lambda: str(uuid.uuid4())
    )
    word: str = Field(index=True, unique_items=True)
    vocabulary_id: str = Field(nullable=False, index=True)
    word_language_code: str = Field(default="en", nullable=False)
    native_language_code: str = Field(nullable=False)
    native_language_definition: str = Field(nullable=False)
    source: str = Field(nullable=False)

    example_sentences: str | None = Field(default="[]")
    notes: str | None = Field(default="[]")

    created_at: int = Field(default_factory=time_provider.time_mills_from_now)
    next_review_at: int = Field(
        default_factory=lambda: time_provider.time_mills_from_now(1)
    )
    interval: int = Field(default=1)
    repetitions: int = Field(default=0)
    review_interval_days: int = Field(default=1)
    quality: int = Field(default=0)
    ease_factor: float = Field(default=2.5)

    # English specific fields
    lemma: str | None = Field(default=None)
    forms: str | None = Field(default=None)
    pronunciation: str | None = Field(default=None)

    # Japanese specific fields
    reading: str | None = Field(default=None)
    conjugation: str | None = Field(default=None)


class VocabularySettingsItem(SQLModel, table=True):
    id: str = Field(
        primary_key=True, nullable=False, default_factory=lambda: str(uuid.uuid4())
    )
    name: str = Field(nullable=False, index=True)
    word_language_code: str = Field(default="en", nullable=False)
    native_language_code: str = Field(nullable=False)
    dictionary: str = Field(nullable=False)
    review_strategy: str = Field(nullable=False)

    created_at: int = Field(default_factory=time_provider.time_mills_from_now)

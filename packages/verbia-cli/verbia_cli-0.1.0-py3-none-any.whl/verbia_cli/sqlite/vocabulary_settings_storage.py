from sqlalchemy import Engine
from sqlmodel import SQLModel, Session, select

from verbia_cli.sqlite import VocabularySettingsItem
from verbia_cli.vocabulary_settings import VocabularySettings


def _item_to_settings(item: VocabularySettingsItem) -> VocabularySettings:
    return VocabularySettings(
        id=item.id,
        name=item.name,
        word_language_code=item.word_language_code,
        native_language_code=item.native_language_code,
        dictionary=item.dictionary,
        review_strategy=item.review_strategy,
        created_at=item.created_at,
    )


def _settings_to_item(settings: VocabularySettings) -> VocabularySettingsItem:
    return VocabularySettingsItem(
        id=settings.id,
        name=settings.name,
        word_language_code=settings.word_language_code,
        native_language_code=settings.native_language_code,
        dictionary=settings.dictionary,
        review_strategy=settings.review_strategy,
        created_at=settings.created_at,
    )


class SQLiteVocabularySettingsStorage:
    def __init__(self, engine: Engine):
        SQLModel.metadata.create_all(engine)

        self._engine = engine

    def get(self, vocabulary_id: str) -> VocabularySettings | None:
        with Session(self._engine) as session:
            statement = select(VocabularySettingsItem).where(
                VocabularySettingsItem.id == vocabulary_id
            )
            item = session.exec(statement).first()
            if item is None:
                return None
            return _item_to_settings(item)

    def list_all(self) -> list[VocabularySettings]:
        with Session(self._engine) as session:
            statement = select(VocabularySettingsItem)
            items = session.exec(statement).all()
            return [_item_to_settings(item) for item in items]

    def add_or_update(self, settings: VocabularySettings):
        with Session(self._engine) as session:
            item = _settings_to_item(settings)
            session.merge(item)
            session.commit()

    def delete(self, id: str):
        with Session(self._engine) as session:
            statement = select(VocabularySettingsItem).where(
                VocabularySettingsItem.id == id
            )
            item = session.exec(statement).first()
            if item is not None:
                session.delete(item)
                session.commit()

    def get_by_name(self, name: str) -> VocabularySettings | None:
        with Session(self._engine) as session:
            statement = select(VocabularySettingsItem).where(
                VocabularySettingsItem.name == name
            )
            item = session.exec(statement).first()
            if item is None:
                return None
            return _item_to_settings(item)

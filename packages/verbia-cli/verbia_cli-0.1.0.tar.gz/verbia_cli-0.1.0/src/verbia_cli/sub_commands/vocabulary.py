from typing import Annotated

import typer
from InquirerPy import inquirer
from langcodes import Language
from loguru import logger

from verbia_cli import config
from verbia_cli.common import handle_verbia_error
from verbia_cli.vocabulary import LocalVocabulary, VocabularySettings

app = typer.Typer(
    name="vocabulary",
    help="Manage vocabularies.",
    no_args_is_help=True,
)


def _check_language_code(code: str) -> bool:
    if len(code) != 2:
        return False
    if not code.isalpha():
        return False
    return Language.get(code).is_valid()


def _set_current_vocabulary(vocabulary_id: str):
    config.set_config("current_vocabulary_id", vocabulary_id)


def _all_vocabulary_names():
    return [vocabulary.name for vocabulary in LocalVocabulary.list_vocabularies()]


@app.command(name="list")
@handle_verbia_error()
def list_vocabularies():
    """
    List all available vocabularies.
    """
    vocabularies = LocalVocabulary.list_vocabularies()
    if not vocabularies:
        typer.echo("No vocabularies found.")
        raise typer.Exit()
    for vocabulary in vocabularies:
        typer.echo(
            f"{vocabulary.name}: {vocabulary.word_language.display_name()} -> {vocabulary.native_language.display_name()}"
        )


@app.command(name="switch")
@handle_verbia_error()
def switch_vocabulary(
    name: Annotated[
        str,
        typer.Argument(
            default_factory=lambda: inquirer.select(
                message="Select current vocabulary to", choices=_all_vocabulary_names()
            ).execute()
        ),
    ],
):
    """
    Switch to a different vocabulary.
    """
    vocabulary = LocalVocabulary.retrieve_by_name(name)
    if not vocabulary:
        typer.echo(f"Vocabulary '{name}' not found.", err=True)
        raise typer.Exit(1)
    _set_current_vocabulary(vocabulary.id)
    typer.echo(f"Switched to vocabulary '{vocabulary.name}'.")
    logger.debug(f"Switched to vocabulary '{vocabulary.name}'.")


def _vocabulary_name_validator(vocabulary_name: str):
    vocabulary_name = vocabulary_name.strip().lower()

    if vocabulary_name == "":
        raise typer.BadParameter("Vocabulary name cannot be empty.")
    first_char = vocabulary_name[0]
    if not (
        first_char[0].isalpha() and first_char[0].isalpha() and first_char[0].isascii()
    ):
        raise typer.BadParameter(
            "Vocabulary name must start with an alphanumeric character."
        )
    if len(vocabulary_name) > 50:
        raise typer.BadParameter("Vocabulary name cannot be longer than 50 characters.")
    if LocalVocabulary.retrieve_by_name(vocabulary_name):
        raise typer.BadParameter(
            f"Vocabulary with the name {vocabulary_name} already exists."
        )
    return vocabulary_name


def _language_code_validator(language_code: str):
    if not _check_language_code(language_code):
        raise typer.BadParameter(
            "Invalid language code. Please enter a valid language code."
        )
    return language_code


@app.command(name="create")
@handle_verbia_error()
def create_vocabulary(
    name: Annotated[
        str,
        typer.Option(
            prompt="Enter the name of the vocabulary",
            callback=_vocabulary_name_validator,
        ),
    ],
    word_language: Annotated[
        str,
        typer.Option(
            prompt="Enter the language code for the words",
            callback=_language_code_validator,
        ),
    ],
    native_language: Annotated[
        str,
        typer.Option(
            prompt="Enter the language code for the language you are learning",
            callback=_language_code_validator,
        ),
    ],
):
    """
    Create a new vocabulary.
    This command will prompt the user for the vocabulary name and languages.
    """

    vocabulary = LocalVocabulary.create(
        VocabularySettings(
            name=name,
            word_language_code=word_language,
            native_language_code=native_language,
        )
    )
    config.set_config("current_vocabulary_id", vocabulary.id)
    typer.echo(f"Vocabulary '{vocabulary.name}' created successfully.")
    logger.debug(f"Vocabulary '{vocabulary.name}' created successfully.")


@app.command(name="delete")
@handle_verbia_error()
def delete_vocabulary(
    name: Annotated[
        str,
        typer.Argument(
            default_factory=lambda: inquirer.select(
                message="Select a vocabulary to delete", choices=_all_vocabulary_names()
            ).execute()
        ),
    ],
):
    """
    Delete a vocabulary.
    """
    vocabulary = LocalVocabulary.retrieve_by_name(name)
    if not vocabulary:
        typer.echo(f"Vocabulary '{name}' not found.", err=True)
        raise typer.Exit(1)
    vocabulary.self_delete()
    typer.echo(f"Vocabulary '{vocabulary.name}' deleted successfully.")
    logger.debug(f"Vocabulary '{vocabulary.name}' deleted successfully.")

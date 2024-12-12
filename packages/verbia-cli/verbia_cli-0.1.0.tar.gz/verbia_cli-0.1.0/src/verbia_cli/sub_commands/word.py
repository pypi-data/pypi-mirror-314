import os

import typer
from loguru import logger
from rich import get_console
from rich.padding import Padding
from rich.table import Table
from rich.text import Text
from typing_extensions import Annotated

from verbia_cli import config
from verbia_cli.common import handle_verbia_error, set_states
from verbia_cli.vocabulary import LocalVocabulary
from verbia_core.entry import EnglishEntry, Entry, JapaneseEntry
from verbia_core.error import VerbiaError
from verbia_core.utils import time_provider
from verbia_core.vocabulary import Vocabulary

app = typer.Typer(
    name="word",
    help="Manage words in the vocabulary.",
    no_args_is_help=True,
)


def clear():
    os.system("clear")


# Initialize the console for rich output


def display_entry(
    entry: Entry,
    show_definition: bool = False,
):
    """Displays a nicely formatted Entry in the terminal."""

    clear()

    # Create a colorful table
    table = Table(
        show_header=True,
        header_style="bold green",
    )

    # Add columns with styling
    table.add_column("Word", style="dim", width=18)
    table.add_column(f"{entry.word}", justify="left", style="bold")

    # Display key details only
    if show_definition:
        table.add_row(
            "Definition", Text(entry.native_language_definition, style="cyan")
        )
        table.add_section()

    # Add forms, if available (for EnglishEntry)
    if isinstance(entry, EnglishEntry):
        table.add_row("Pronunciation", Text(entry.pronunciation or "N/A"))
        table.add_row("Lemma", Text(entry.lemma or "N/A"))
        if entry.forms:
            forms = entry.forms
            forms_text = []
            if forms.past_tense:
                forms_text.append(f"Past Tense: {forms.past_tense}")
            if forms.present_participle:
                forms_text.append(f"Present Participle: {forms.present_participle}")
            if forms.past_participle:
                forms_text.append(f"Past Participle: {forms.past_participle}")
            if forms.third_person_singular:
                forms_text.append(f"3rd Person Singular: {forms.third_person_singular}")
            if forms.singular:
                forms_text.append(f"Singular: {forms.singular}")
            if forms.plural:
                forms_text.append(f"Plural: {forms.plural}")
            if forms.comparative:
                forms_text.append(f"Comparative: {forms.comparative}")
            if forms.superlative:
                forms_text.append(f"Superlative: {forms.superlative}")
            if forms_text:
                table.add_row("Forms", "\n".join(forms_text))

    if isinstance(entry, JapaneseEntry):
        if entry.reading:
            reading = entry.reading
            reading_text = []
            if reading.hiragana:
                reading_text.append(f"Hiragana: {reading.hiragana}")
            if reading.katakana:
                reading_text.append(f"Katakana: {reading.katakana}")
            if reading.kunyomi:
                reading_text.append(f"Kunyomi: {reading.kunyomi}")
            if reading.onyomi:
                reading_text.append(f"Onyomi: {reading.onyomi}")
            if reading_text:
                table.add_row("Reading", "\n".join(reading_text))
        if entry.conjugation:
            conjugation = entry.conjugation
            conjugation_text = []
            if conjugation.present:
                conjugation_text.append(f"Present: {conjugation.present}")
            if conjugation.past:
                conjugation_text.append(f"Past: {conjugation.past}")
            if conjugation.negative:
                conjugation_text.append(f"Negative: {conjugation.negative}")
            if conjugation.te_form:
                conjugation_text.append(f"Te Form: {conjugation.te_form}")
            if conjugation.potential:
                conjugation_text.append(f"Potential: {conjugation.potential}")
            if conjugation.polite:
                conjugation_text.append(f"Polite: {conjugation.polite}")
            if conjugation_text:
                table.add_row("Conjugation", "\n".join(conjugation_text))

    # Add example sentences, if available
    if entry.example_sentences:
        example_sentences = entry.example_sentences
        example_sentences_text = []
        for example in example_sentences:
            example_sentences_text.append(example)
        if example_sentences_text:
            table.add_row("Example Sentences", "\n".join(example_sentences_text))

    # If entry has notes, display them as well
    if entry.notes:
        notes = entry.notes
        notes_text = []
        for note in notes:
            notes_text.append(note)
        if notes_text:
            table.add_row("Notes", "\n".join(notes_text))

    if show_definition:
        table.add_section()

        table.add_row("Repetitions", str(entry.repetitions))
        table.add_row("Review Interval", str(entry.review_interval_days) + " days")
        table.add_row(
            "Next Review At", time_provider.format_timestamp(entry.next_review_at)
        )

    console = get_console()

    console.print(table)
    console.print(Padding("\n", (0, 0, 1, 0)))


def current_vocabulary() -> Vocabulary:
    current_vocabulary_id = config.get_config("current_vocabulary_id")
    if not current_vocabulary_id:
        typer.echo(
            "No vocabulary selected. Use 'verbia vocabulary create' to create a vocabulary or use 'verbia vocabulary switch' to select a vocabulary."
        )
        raise typer.Exit(1)
    vocabulary = LocalVocabulary.retrieve_by_id(current_vocabulary_id)
    if not vocabulary:
        typer.echo(
            f"Selected vocabulary with id '{current_vocabulary_id}' does not exist."
        )

    return vocabulary


@app.command(name="add", no_args_is_help=True)
@handle_verbia_error()
def add_word(
    word: str = typer.Argument(...),
    vocabulary: Annotated[
        str,
        typer.Option(
            help="Name of the vocabulary to add the word to. If not provided, the current vocabulary is used."
        ),
    ] = None,
    verbose: bool = typer.Option(
        False, "--verbose", "-d", callback=set_states, help="Enable verbose mode."
    ),
):
    """
    Add a word to the vocabulary.
    This will lookup the word in the dictionary and add it to the database.
    """
    if vocabulary:
        _vocabulary = LocalVocabulary.retrieve_by_name(vocabulary)
        if not _vocabulary:
            typer.echo(f"Vocabulary '{vocabulary}' does not exist.")
            raise typer.Exit(1)
    else:
        _vocabulary = current_vocabulary()

    entry = _vocabulary.get_entry(word)
    if entry:
        display_entry(entry, show_definition=True)
        typer.echo(
            f"Word '{entry.word}' already exists in the vocabulary {_vocabulary.name}."
        )
    else:
        entry = _vocabulary.add_word(word)
        display_entry(entry, show_definition=True)
        typer.echo(
            f"Word '{entry.word}' has been added to the vocabulary {_vocabulary.name}."
        )
        logger.debug(f"Word '{entry.word}' added to the vocabulary {_vocabulary.name}.")


@app.command(name="review")
@handle_verbia_error()
def review_words():
    """
    Review words that are due for review.
    This command fetches all words that need to be reviewed based on the review strategy.
    The user will be prompted for feedback on their recall of each word.
    """
    _vocabulary = current_vocabulary()
    due_words = (
        _vocabulary.list_all_due_entries()
    )  # Fetch words that are due for review

    if not due_words:
        typer.echo("No words are due for review at the moment.")
        raise typer.Exit()

    # Iterate through the due words and prompt the user for their feedback
    for entry in due_words:
        display_entry(entry)  # Display the word entry beautifully
        user_quality = typer.prompt(
            "How well do you remember this word? (1-5), 1 being the worst and 5 being the best",
            type=int,
        )

        if user_quality < 1 or user_quality > 5:
            typer.echo("Invalid quality. Please enter a number between 1 and 5.")
            continue

        if not user_quality == 5:
            display_entry(entry, show_definition=True)
            typer.pause(info="Press Enter to continue...")

        # Update the review information based on the user's feedback
        _vocabulary.update_review(entry, user_quality)
        typer.echo(f"Review feedback for '{entry.word}' updated successfully.")


@app.command(name="delete", no_args_is_help=True)
@handle_verbia_error()
def delete_word(
    word: str = typer.Argument(...),
    verbose: bool = typer.Option(
        False, "--verbose", "-d", callback=set_states, help="Enable verbose mode."
    ),
):
    """
    Delete a word from current vocabulary.
    """
    _vocabulary = current_vocabulary()
    entry = _vocabulary.get_entry(word)
    if entry is None:
        raise VerbiaError(f"Word '{word}' not present in the vocabulary.")
    _vocabulary.delete_entry(entry)

    typer.echo(f"Word '{entry.word}' has been deleted from the vocabulary.")
    logger.debug(f"Word '{entry.word}' deleted from the vocabulary {_vocabulary.name}.")

__author__ = "Jonathan Fox"
__copyright__ = "Copyright 2024, Jonathan Fox"
__license__ = "GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html"
__full_source_code__ = "https://github.com/jonathanfox5/lemma_from_wiki"

import typer
from typing_extensions import Annotated

from .cli_utils import CliUtils
from .generate_lemma_file import generate_lemma_file
from .help_text import HelpText

"""
Define settings for the cli framework (Typer) and load defaults from config file
"""
app = typer.Typer(
    no_args_is_help=True,
    rich_markup_mode="rich",
    add_completion=False,
    pretty_exceptions_enable=False,
)


@app.command(no_args_is_help=True, rich_help_panel="Primary Functions", help=HelpText.generate)
def generate(
    language: Annotated[
        str,
        typer.Option(
            "--language",
            "-l",
            help=HelpText.language_code,
            callback=CliUtils.validate_language_code,
            rich_help_panel="Required",
            show_default=False,
        ),
    ],
    max_articles: Annotated[
        int,
        typer.Option(
            "--max-articles",
            "-n",
            help=HelpText.max_articles,
            rich_help_panel="Required",
            show_default=False,
        ),
    ],
    gpu: Annotated[
        bool,
        typer.Option(
            "--gpu/--cpu", "-g/-c", help=HelpText.use_cuda, rich_help_panel="Optional Flags"
        ),
    ] = True,
):
    generate_lemma_file(language=language, use_gpu=gpu, max_articles=max_articles)

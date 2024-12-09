__author__ = "Jonathan Fox"
__copyright__ = "Copyright 2024, Jonathan Fox"
__license__ = "GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html"
__full_source_code__ = "https://github.com/jonathanfox5/lemma_from_wiki"
__uses_code_from__ = "https://github.com/jonathanfox5/gogadget"

from lemon_tizer import LemonTizer

from .help_text import SupportedLanguages


def lemma_dummy(language: str) -> None:
    """Function to initialise the lemmatiser on first run and download the required modules"""
    lt = LemonTizer(language, "lg")
    lt.lemmatize_sentence("Wololo")


def language_supported_spacy(language: str) -> bool:
    """Check if the language is supported by spacy.
    LemonTizer has its own function that is more accurate but this works offline."""

    supported = language in SupportedLanguages.spacy_languages.keys()
    return supported


def language_supported_simplemma(language: str) -> bool:
    """Check if the language is supported by simplemma."""

    supported = language in SupportedLanguages.simplemma_languages.keys()
    return supported


def force_gpu():
    """Force spacy to use the GPU"""
    import spacy

    spacy.require_gpu()

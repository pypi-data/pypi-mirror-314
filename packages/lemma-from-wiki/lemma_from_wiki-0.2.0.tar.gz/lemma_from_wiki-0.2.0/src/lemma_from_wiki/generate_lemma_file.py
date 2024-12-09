__author__ = "Jonathan Fox"
__copyright__ = "Copyright 2024, Jonathan Fox"
__license__ = "GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html"
__full_source_code__ = "https://github.com/jonathanfox5/lemma_from_wiki"
__uses_code_from__ = ["https://github.com/jonathanfox5/gogadget"]

import pandas as pd
import regex as re
import simplemma
from datasets import load_dataset as load_hf_dataset
from datasets.iterable_dataset import IterableDataset
from lemon_tizer import LemonTizer
from rich.progress import track

from .cli_utils import CliUtils
from .config import Config
from .lemma_utils import force_gpu, language_supported_simplemma, language_supported_spacy


def generate_lemma_file(language: str, use_gpu: bool, max_articles: int, show_diff: bool):
    """Build a lemmatization file compatible with vocabsieve"""

    # Configure lemmatiser settings and get lemmatiser object back
    CliUtils.print_status("Initialising lemmatiser")

    language = language.lower()
    lt: LemonTizer | None = lemma_config(language=language, use_gpu=use_gpu)

    if lt is None:
        return

    # Dummy lemma to throw an error in case something isn't correctly configured
    CliUtils.print_status("Testing lemmatiser")
    lemma_test(lt=lt)

    # Get a datastream to iterate through
    CliUtils.print_status("Getting data")
    datastream = stream_dataset(
        language=language,
        corpus_name=Config.corpus_name,
        subset_stem=Config.subset_stem,
        max_articles=max_articles,
    )

    # Do the actual work of lemmatising the articles and doing a frequency analysis
    CliUtils.print_status("Lemmatising")
    lemma_table = pd.DataFrame(columns=["word", "lemma", "simplemma", "frequency"])
    lemma_table = build_lemma_table(
        df=lemma_table, lt=lt, datastream=datastream, max_articles=max_articles
    )

    # Get the simplemma lemma and, if `show_diff`, filter only to the rows that are different
    CliUtils.print_status("Comparing to simplemma")
    lemma_table = get_simplemma_lemmas(df=lemma_table, language=language)

    if show_diff:
        lemma_table = include_only_differences(df=lemma_table)

    # Save to csv
    CliUtils.print_status("Saving")
    lemma_table.to_csv(
        path_or_buf=f"{Config.output_stem}_{language}_{max_articles}_{"_diff" if show_diff else "_all"}.csv",
        index=False,
    )


def include_only_differences(df: pd.DataFrame) -> pd.DataFrame:
    """Return only the rows where the spacy result and simplemma result do not agree"""
    df = df[df["lemma"] != df["simplemma"]]
    return df


def get_simplemma_lemmas(df: pd.DataFrame, language: str) -> pd.DataFrame:
    """Calculate the simplemma lemma for each row of a dataframe"""

    # Check language is supported by simplemma
    if not language_supported_simplemma(language=language):
        CliUtils.print_warning(f"{language=} not supported by simplemma, cannot do comparison")
        return df

    # Get simplemma value for each word
    df["simplemma"] = df["word"].apply(lambda word: simplemma_lemma_word(word=word, lang=language))

    return df


def simplemma_lemma_word(word: str, lang: str) -> str:
    """Lemmatise using simplemma and clean up the output"""

    lemma = simplemma.lemmatize(token=word, lang=lang)
    lemma = lemma.lower()
    lemma = remove_nonalpha(lemma)

    return lemma


def build_lemma_table(
    df: pd.DataFrame,
    lt: LemonTizer,
    datastream: IterableDataset,
    max_articles: int,
    remove_duplicates: bool = True,
) -> pd.DataFrame:
    """Loop through articles in the datastream, get the spacy lemma and remove duplicates based upon frequency"""

    # Process each article
    for data in track(datastream, description="Processing articles", total=max_articles):
        text_input = data.get("text")
        lemma_list = lt.lemmatize_sentence(text_input)
        df = count_lemmas(df=df, lemma_list=lemma_list)

    # Sort the df
    df = df.sort_values(["word", "frequency"], ascending=[True, False])

    # If a word has multiple lemmas, only keep the first
    if remove_duplicates:
        df = df.drop_duplicates("word", keep="first")

    return df


def count_lemmas(df: pd.DataFrame, lemma_list: list[dict[str, str]]) -> pd.DataFrame:
    """Create frequency analysis of word / lemma pairings and store in a dataframe"""
    for lemma_dict in lemma_list:
        for word, lemma in lemma_dict.items():
            # Clean up the lemma
            lemma = remove_nonalpha(lemma)

            # If the clean version is blank, move on to the next one
            if lemma == "":
                continue

            # If word / lemma pair exists in, increment it
            # Otherwise create a new row
            match = df[(df["word"] == word) & (df["lemma"] == lemma)]

            if not match.empty:
                df.loc[match.index, "frequency"] += 1
            else:
                new_row = pd.DataFrame([{"word": word, "lemma": lemma, "frequency": 1}])

                df = pd.concat([df, new_row], ignore_index=True)

    return df


def stream_dataset(
    language: str, corpus_name: str, subset_stem: str, max_articles: int
) -> IterableDataset:
    """Configure a dataset for streaming"""
    dataset_stream = load_hf_dataset(
        corpus_name, f"{subset_stem}.{language}", split="train", streaming=True
    )
    datastream_filtered = dataset_stream.take(max_articles)

    return datastream_filtered


def lemma_test(lt: LemonTizer) -> dict[str, str]:
    """Run a test lemmatisation to check that everything is working correctly"""
    lemma_test = ". ".join(
        ["Hello world", "123", "Б", "Α", "ב", "א", "अ", "中", "あ", "가", "ก", "அ"]
    )

    lemma_dict = lt.lemmatize_sentence(lemma_test)

    return lemma_dict


def lemma_config(language: str, use_gpu: bool) -> LemonTizer | None:
    """Configure the lemmatiser behaviour"""
    if not language_supported_spacy(language):
        CliUtils.print_error(
            f"Language {language} is not currently supported by the lemmatiser so cannot generate files."
        )
        return None

    # TODO: Add a check to see if there is an NVIDIA gpu installed
    if use_gpu:
        force_gpu()

    # Configure lemmatiser
    lt = LemonTizer(language=language, model_size="lg")
    lt.set_lemma_settings(
        filter_out_non_alpha=False,
        filter_out_common=False,
        convert_input_to_lower=True,
        convert_output_to_lower=True,
        return_just_first_word_of_lemma=False,
    )

    return lt


def remove_nonalpha(input_string: str):
    """Remove punctuation and numbers from a string. Should work with any unicode character"""

    pattern = r"(\p{L}\p{M}*)"
    p = re.compile(pattern)

    result = p.findall(input_string)

    output_string = "".join(result)

    return output_string

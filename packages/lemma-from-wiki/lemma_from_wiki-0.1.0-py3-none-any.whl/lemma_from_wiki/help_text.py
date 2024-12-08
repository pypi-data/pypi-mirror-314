__author__ = "Jonathan Fox"
__copyright__ = "Copyright 2024, Jonathan Fox"
__license__ = "GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html"
__full_source_code__ = "https://github.com/jonathanfox5/lemma_from_wiki"
__uses_code_from__ = ["https://github.com/jonathanfox5/gogadget"]


class HelpText:
    language_code = "Language to use for processing. This should be a two letter language code, e.g. [cyan b]en[/] (for English), [cyan b]es[/] (for Spanish) or [cyan b]it[/] (Italian). Run [cyan bold]gogadget list-languages[/] for a list of supported languages."
    generate = "Generate a vocabsieve compatible lemmatiser list"
    use_cuda = "You can specify --gpu if you have a CUDA enabled Nvidia graphics card to significantly speed up the processing."
    max_articles = "The maximum number of wikipedia articles to process."


class SupportedLanguages:
    """Contains dictionaries of the supported languages for each function plus some explanation text"""

    common_explanation = "All features of the tool are available for the following languages. [b]If your language isn't listed[/], you can run [cyan bold]gogadget list-languages --detailed[/] to get a list of features that are supported by each language."
    whisper_explanation = "The transcriber (whisperX) supports the following languages fully. Languages not listed might work or might work with some manual configuration. However, basic functionality is available for over 100 languages! The transcriber is not required if you provide your own subtitle files."
    spacy_explanation = "The lemmatiser (spacy) supports the following languages. The tool will still work if your language is not available. However, the tool will not be able to lemmatise words or remove 'stop' words."
    argos_explanation = "The translator (argos) supports the following languages. The tool will still work if your language is not available. However, the tool will not be able to translate sentences."
    whisper_languages = {
        "ar": "Arabic",
        "ca": "Catalan",
        "zh": "Chinese",
        "hr": "Croatian",
        "cs": "Czech",
        "da": "Danish",
        "nl": "Dutch",
        "en": "English",
        "fi": "Finnish",
        "fr": "French",
        "de": "German",
        "he": "Hebrew",
        "hi": "Hindi",
        "hu": "Hungarian",
        "it": "Italian",
        "ja": "Japanese",
        "ko": "Korean",
        "ml": "Malayalam",
        "el": "Greek",
        "no": "Norwegian",
        "nn": "Norwegian Nynorsk",
        "fa": "Persian",
        "pl": "Polish",
        "pt": "Portuguese",
        "ru": "Russian",
        "sk": "Slovak",
        "sl": "Slovenian",
        "es": "Spanish",
        "te": "Telugu",
        "tr": "Turkish",
        "uk": "Ukrainian",
        "ur": "Urdu",
        "vi": "Vietnamese",
    }

    spacy_languages = {
        "ca": "Catalan",
        "zh": "Chinese",
        "hr": "Croatian",
        "da": "Danish",
        "nl": "Dutch",
        "en": "English",
        "fi": "Finnish",
        "fr": "French",
        "de": "German",
        "el": "Greek",
        "it": "Italian",
        "ja": "Japanese",
        "ko": "Korean",
        "lt": "Lithuanian",
        "mk": "Macedonian",
        "nb": "Norwegian Bokmål",
        "pl": "Polish",
        "pt": "Portuguese",
        "ro": "Romanian",
        "ru": "Russian",
        "sl": "Slovenian",
        "es": "Spanish",
        "sv": "Swedish",
        "uk": "Ukrainian",
    }

    argos_languages = {
        "sq": "Albanian",
        "ar": "Arabic",
        "az": "Azerbaijani",
        "eu": "Basque",
        "bn": "Bengali",
        "bg": "Bulgarian",
        "ca": "Catalan",
        "zh": "Chinese",
        "zt": "Chinese (traditional)",
        "cs": "Czech",
        "da": "Danish",
        "nl": "Dutch",
        "en": "English",
        "eo": "Esperanto",
        "et": "Estonian",
        "fi": "Finnish",
        "fr": "French",
        "gl": "Galician",
        "de": "German",
        "el": "Greek",
        "he": "Hebrew",
        "hi": "Hindi",
        "hu": "Hungarian",
        "id": "Indonesian",
        "ga": "Irish",
        "it": "Italian",
        "ja": "Japanese",
        "ko": "Korean",
        "lv": "Latvian",
        "lt": "Lithuanian",
        "ms": "Malay",
        "nb": "Norwegian",
        "fa": "Persian",
        "pl": "Polish",
        "pt": "Portuguese",
        "ro": "Romanian",
        "ru": "Russian",
        "sk": "Slovak",
        "sl": "Slovenian",
        "es": "Spanish",
        "sv": "Swedish",
        "tl": "Tagalog",
        "th": "Thai",
        "tr": "Turkish",
        "uk": "Ukrainian",
        "ur": "Urdu",
    }

    @staticmethod
    def get_common_languages():
        """Works out the languages that are supported by all functions by combining dictionaries"""

        a = SupportedLanguages.spacy_languages
        b = SupportedLanguages.whisper_languages
        c = SupportedLanguages.argos_languages

        output_dict = {}

        for key, value in a.items():
            if (key in b) and (key in c):
                output_dict[key] = value

        return output_dict

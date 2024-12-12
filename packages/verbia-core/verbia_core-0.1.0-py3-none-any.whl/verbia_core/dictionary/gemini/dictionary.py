import json
import os
from string import Template

from langcodes import Language
from loguru import logger

from verbia_core.dictionary.base import DictionaryBase
from verbia_core.dictionary.gemini.client import get_client
from verbia_core.entry import (
    EnglishEntry,
    Forms,
    Entry,
    JapaneseEntry,
    JapaneseReading,
    Conjugation,
)
from verbia_core.error import WordInvalidError

# Suppress logging warnings
os.environ["GRPC_VERBOSITY"] = "ERROR"
os.environ["GLOG_minloglevel"] = "2"

english_prompt = Template("""You are a language assistant for looking up English words. When I provide a word, please give me the following information in $native_language:

1. The definition or meaning of the word in $native_language, along with its part of speech (e.g., n. for noun, v. for verb, adj. for adjective).
2. Example sentences in English demonstrating how the word is used in context.
3. If the word has multiple forms (e.g., plural, past tense), provide those forms in $native_language.
4. The lemma (base form) of the word, if applicable.
5. The pronunciation of the word in IPA format, if available.

Make sure the response follows this JSON structure:
{
  "word": "{word}",
  "definition": "{definition_in_native_language}",
  "example_sentences": [
    "{sentence_1}",
    "{sentence_2}",
    "{sentence_3}"
  ],
  "forms": {
        "past_tense": "{past_tense_form}",
        "present_participle": "{present_participle_form}",
        "past_participle": "{past_participle_form}",
        "third_person_singular": "{third_person_singular_form}",
        "singular": "{singular_form}",
        "plural": "{plural_form}",
        "comparative": "{comparative_form}",
        "superlative": "{superlative_form}"
    },
  "lemma": "{lemma}",
  "pronunciation": "{IPA_pronunciation}"
}

Here is the word I want to look up: $word
If the word is not a valid English word, please respond null as the value for field "definition".
""")

japanese_prompt = Template("""
You are a language assistant for looking up Japanese words. When I provide a word, please give me the following information in $native_language:

1. The definition or meaning of the word in $native_language.
2. The readings (hiragana/katakana/kanji) of the word, including any kanji readings (kun'yomi and on'yomi).
3. Example sentences in Japanese demonstrating how the word is used in context.
4. If the word is a verb, provide its conjugation in different tenses and forms (e.g., present, past, negative form, te-form, potential form, polite form).

Make sure the response follows this JSON structure:
{
    "word": "[word]",
    "definition": "[definition_in_native_language]",
    "reading": {
        "hiragana": "[hiragana_reading]",
        "katakana": "[katakana_reading]",
        "kanji": {
            "kunyomi": "[kunyomi_reading]",
            "onyomi": "[onyomi_reading]"
    },
    "example_sentences": [
        "[example_sentence_1]",
        "[example_sentence_2]"
    ],
    "conjugation": {
        "present": "[present_conjugation]",
        "past": "[past_conjugation]",
        "negative": "[negative_conjugation]",
        "te-form": "[te_form]",
        "potential": "[potential_form]",
        "polite": "[polite_form]"
    }
}

Conjugation should be provided only if the word is a verb and contains the original word. 
For example, if the word is "勉強", the conjugation should be provided for "勉強する" and not "する".

Here is the word I want to look up: $word
If the word is not a valid Japanese word, please respond null as the value for field "definition".
""")

common_language_prompt = Template("""
You are a language assistant for looking up words in $word_language. When I provide a word, please give me the following information in $native_language:

1. The definition or meaning of the word in $native_language.
2. Example sentences in $word_language demonstrating how the word is used in context.

Make sure the response follows this JSON structure:
{
    "word": "[word]",
    "definition": "[definition_in_native_language]",
    "example_sentences": [
        "[example_sentence_1]",
        "[example_sentence_2]"
    ]
}

Here is the word I want to look up: $word
If the word is not a valid word in $word_language, please respond null as the value for field "definition".
""")


def _prepare_prompt(
    word: str, word_language: Language, native_language: Language
) -> str:
    match word_language.language:
        case "en":
            return english_prompt.substitute(
                word=word, native_language=native_language.display_name()
            )
        case "ja":
            return japanese_prompt.substitute(
                word=word, native_language=native_language.display_name()
            )
        case _:
            return common_language_prompt.substitute(
                word=word,
                word_language=word_language.display_name(),
                native_language=native_language.display_name(),
            )


def _is_none(value: str) -> bool:
    return (
        value is None
        or value == "null"
        or value == ""
        or value == "None"
        or value == "none"
        or value == "undefined"
        or value == "nil"
        or value == "NaN"
        or value == "nan"
        or value == "NULL"
        or value == "NoneType"
        or value == "noneType"
        or value == "undefinedType"
        or value == "nilType"
        or value == "NaNType"
        or value == "nanType"
    )


class GeminiDictionary(DictionaryBase):
    def __init__(self, api_key: str | None = None):
        self.__client = None
        self._api_key = api_key
        super().__init__("Gemini")

    @property
    def _client(self):
        if not self.__client:
            self.__client = get_client(self._api_key)
        return self.__client

    def _generate(self, prompt: str) -> dict:
        import google.generativeai as genai

        result = self._client.generate_content(
            contents=prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            ),
        )
        return json.loads(result.text)

    async def _async_generate(self, prompt: str) -> dict:
        import google.generativeai as genai

        result = await self._client.generate_content_async(
            contents=prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json"
            ),
        )
        return json.loads(result.text)

    def _extract_to_entry(
        self,
        response: dict,
        word: str,
        word_language: Language,
        native_language: Language,
    ) -> Entry:
        match word_language.language:
            case "en":
                return self._extract_to_english_entry(response, word, native_language)
            case "ja":
                return self._extract_to_japanese_entry(response, word, native_language)
            case _:
                return self._extract_to_common_entry(
                    response, word, word_language, native_language
                )

    def _extract_to_english_entry(
        self, response: dict, word: str, native_language: Language
    ) -> EnglishEntry:
        if not isinstance(response, dict):
            logger.error("Response is not a valid dictionary")
            raise ValueError("Invalid response format: expected a dictionary")

        definition = response.get("definition")
        if _is_none(definition):
            logger.warning(f"Definition not found for word: {word}")
            raise WordInvalidError(word, native_language.display_name())

        _forms = response.get("forms", {})
        if not isinstance(_forms, dict):
            logger.warning(
                f"Forms for word '{word}' should be a dictionary. Using empty dictionary."
            )
            forms = None
        else:
            try:
                past_tense = _forms.get("past_tense")
                present_participle = _forms.get("present_participle")
                past_participle = _forms.get("past_participle")
                third_person_singular = _forms.get("third_person_singular")
                singular = _forms.get("singular")
                plural = _forms.get("plural")
                comparative = _forms.get("comparative")
                superlative = _forms.get("superlative")
                forms = Forms(
                    past_tense=past_tense,
                    present_participle=present_participle,
                    past_participle=past_participle,
                    third_person_singular=third_person_singular,
                    singular=singular,
                    plural=plural,
                    comparative=comparative,
                    superlative=superlative,
                )
            except Exception as e:
                logger.error(f"Error processing forms for word '{word}': {str(e)}")
                forms = None

        lemma = response.get("lemma")
        pronunciation = response.get("pronunciation")

        return EnglishEntry(
            word=word,
            native_language=native_language,
            native_language_definition=definition,
            forms=forms,
            lemma=lemma,
            pronunciation=pronunciation,
            source=self._source,
            is_new=True,
        )

    def _extract_to_japanese_entry(
        self, response: dict, word: str, native_language: Language
    ) -> JapaneseEntry:
        if not isinstance(response, dict):
            logger.error("Response is not a valid dictionary")
            raise ValueError("Invalid response format: expected a dictionary")

        definition = response.get("definition")
        if _is_none(definition):
            logger.warning(f"Definition not found for word: {word}")
            raise WordInvalidError(word, native_language.display_name())

        example_sentences = response.get("example_sentences", [])
        if not isinstance(example_sentences, list):
            logger.warning(
                f"Example sentences for word '{word}' should be a list. Using empty list."
            )
            example_sentences = []

        _reading = response.get("reading")
        if not isinstance(_reading, dict):
            logger.warning(
                f"Reading for word '{word}' should be a dictionary. Using empty dictionary."
            )
            reading = None
        else:
            try:
                hiragana = _reading.get("hiragana")
                katakana = _reading.get("katakana")
                kanji = _reading.get("kanji")
                kunyomi = kanji.get("kunyomi") if kanji else None
                onyomi = kanji.get("onyomi") if kanji else None
                reading = JapaneseReading(
                    hiragana=hiragana, katakana=katakana, kunyomi=kunyomi, onyomi=onyomi
                )
            except Exception as e:
                logger.error(f"Error processing reading for word '{word}': {str(e)}")
                reading = None

        _conjugation = response.get("conjugation")
        if not isinstance(_conjugation, dict):
            logger.warning(
                f"Conjugation for word '{word}' should be a dictionary. Using empty dictionary."
            )
            conjugation = None
        else:
            try:
                present = _conjugation.get("present")
                past = _conjugation.get("past")
                negative = _conjugation.get("negative")
                te_form = _conjugation.get("te-form")
                potential = _conjugation.get("potential")
                polite = _conjugation.get("polite")
                conjugation = Conjugation(
                    present=present,
                    past=past,
                    negative=negative,
                    te_form=te_form,
                    potential=potential,
                    polite=polite,
                )
            except Exception as e:
                logger.error(
                    f"Error processing conjugation for word '{word}': {str(e)}"
                )
                conjugation = None

        return JapaneseEntry(
            word=word,
            native_language=native_language,
            native_language_definition=definition,
            example_sentences=example_sentences,
            reading=reading,
            conjugation=conjugation,
            source=self._source,
            is_new=True,
        )

    def _extract_to_common_entry(
        self,
        response: dict,
        word: str,
        word_language: Language,
        native_language: Language,
    ) -> Entry:
        if not isinstance(response, dict):
            logger.error("Response is not a valid dictionary")
            raise ValueError("Invalid response format: expected a dictionary")

        definition = response.get("definition")
        if _is_none(definition):
            logger.warning(f"Definition not found for word: {word}")
            raise WordInvalidError(word, native_language.display_name())

        example_sentences = response.get("example_sentences", [])
        if not isinstance(example_sentences, list):
            logger.warning(
                f"Example sentences for word '{word}' should be a list. Using empty list."
            )
            example_sentences = []

        return Entry(
            word=word,
            word_language=word_language,
            native_language=native_language,
            native_language_definition=definition,
            example_sentences=example_sentences,
            source=self._source,
            is_new=True,
        )

    def lookup(
        self, word: str, word_language: Language, native_language: Language
    ) -> Entry:
        logger.debug(
            f"Looking up word '{word}' in {native_language.display_name()} by {self._source}"
        )
        prompt = _prepare_prompt(word, word_language, native_language)
        response = self._generate(prompt)
        return self._extract_to_entry(response, word, word_language, native_language)

    async def async_lookup(
        self, word: str, word_language: Language, native_language: Language
    ) -> Entry:
        logger.debug(
            f"Looking up word '{word}' in {native_language.display_name()} by {self._source}"
        )
        prompt = _prepare_prompt(word, word_language, native_language)
        response = await self._async_generate(prompt)
        return self._extract_to_entry(response, word, word_language, native_language)

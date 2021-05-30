import os
import pytest
import deepl_api
from deepl_api.exceptions import DeeplAuthorizationError, DeeplServerError

from deepl_api import __version__


def test_version():
    assert __version__ == "0.1.0"


def test_usage_information():
    assert (
        deepl_api.DeepL(os.getenv("DEEPL_API_KEY")).usage_information().character_limit
        > 0
    )


def test_source_languages():
    assert (
        deepl_api.DeepL(os.getenv("DEEPL_API_KEY")).source_languages()["DE"] == "German"
    )


def test_target_languages():
    assert (
        deepl_api.DeepL(os.getenv("DEEPL_API_KEY")).target_languages()["DE"] == "German"
    )


def test_translate():
    deepl = deepl_api.DeepL(os.getenv("DEEPL_API_KEY"))

    tests = [
        {
            "args": {
                "source_language": "DE",
                "target_language": "EN-US",
                "texts": ["ja"],
            },
            "result": [
                {
                    "detected_source_language": "DE",
                    "text": "yes",
                },
            ],
        },
        {
            "args": {
                "source_language": "DE",
                "target_language": "EN-US",
                "preserve_formatting": True,
                "texts": ["ja\n nein"],
            },
            "result": [
                {
                    "detected_source_language": "DE",
                    "text": "yes\n no",
                },
            ],
        },
        {
            "args": {
                "source_language": "DE",
                "target_language": "EN-US",
                "split_sentences": deepl_api.SplitSentences.NONE,
                "texts": ["Ja. Nein."],
            },
            "result": [
                {
                    "detected_source_language": "DE",
                    "text": "Yes. No.",
                },
            ],
        },
        {
            "args": {
                "source_language": "EN",
                "target_language": "DE",
                "formality": deepl_api.Formality.MORE,
                "texts": ["Please go home."],
            },
            "result": [
                {
                    "detected_source_language": "EN",
                    "text": "Bitte gehen Sie nach Hause.",
                },
            ],
        },
        {
            "args": {
                "source_language": "EN",
                "target_language": "DE",
                "formality": deepl_api.Formality.LESS,
                "texts": ["Please go home."],
            },
            "result": [
                {
                    "detected_source_language": "EN",
                    "text": "Bitte geh nach Hause.",
                },
            ],
        },
        {
            "args": {
                "source_language": "EN",
                "target_language": "FR",
                "handle_xml": True,
                "texts": ["A delicious <i>apple</i>."],
            },
            "result": [
                {
                    "detected_source_language": "EN",
                    "text": "Une <i>pomme</i> délicieuse.",
                },
            ],
        },
        {
            "args": {
                "source_language": "EN",
                "target_language": "FR",
                "texts": ["A delicious <i>apple</i>."],
            },
            "result": [
                {
                    "detected_source_language": "EN",
                    "text": "Une délicieuse <i>pomme</i>.",
                },
            ],
        },
    ]

    for test in tests:
        assert deepl.translate(**test["args"]) == test["result"]


def test_translate_empty():
    with pytest.raises(DeeplServerError):
        deepl_api.DeepL(os.getenv("DEEPL_API_KEY")).translate(
            target_language="NONEXISTING", texts=["ja"]
        )


def test_translate_unauthorized():
    with pytest.raises(DeeplAuthorizationError):
        deepl_api.DeepL("wrong_key").translate(target_language="EN-US", texts=["ja"])

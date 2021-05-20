"""
Provides a lightweight wrapper for the DeepL Pro REST API.

*If you are looking for the `deepl` commandline utitlity, please refer
to [its documentation](cli.html) instead.*

.. include:: ./doc_api.md

"""

__version__ = "0.1.0"

from dataclasses import dataclass
from enum import Enum
import requests

from deepl_api.exceptions import (
    DeeplAuthorizationError,
    DeeplServerError,
    DeeplDeserializationError,
)


@dataclass
class UsageInformation:
    """Information about API usage & limits for this account."""

    character_count: int
    """How many characters can be translated per billing period, based on the account settings."""

    character_limit: int
    """How many characters were already translated in the current billing period."""


class SplitSentences(Enum):
    """Translation option that controls the splitting of sentences before the translation."""

    NONE = 0
    """Don't split sentences."""

    PUNCTUATION = 1
    """Split on punctiation only."""

    PUNCTUATION_AND_NEWLINES = "newlines"
    """Split on punctuation and newlines."""


class Formality(Enum):
    """Translation option that controls the desired translation formality."""

    LESS = "less"
    """Translate less formally."""

    DEFAULT = "default"
    """Default formality."""

    MORE = "more"
    """Translate more formally."""


class DeepL:
    """
    The main API entry point representing a DeepL developer account with an associated API key.

    Use this to create a new DeepL API client instance where multiple function calls can be performed.
    A valid `api_key` is required.

    Should you ever need to use more than one DeepL account in our program, then you can create one
    instance for each account / API key.

    ##Error Handling

    These methods may throw exceptions defined in `deepl_api.exceptions` and [requests.exceptions](https://requests.readthedocs.io/en/latest/api/#exceptions).

    """

    _api_key: str
    _api_base_url: str

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._api_base_url = (
            "https://api-free.deepl.com/v2"
            if api_key.endswith(":fx")
            else "https://api.deepl.com/v2"
        )

    # Private method that performs the HTTP calls.
    def _api_call(self, url: str, payload: dict = {}):

        # Create a new dict to avoid modifying the passed one.
        post_data = {**payload, "auth_key": self._api_key}

        with requests.post(self._api_base_url + url, post_data) as response:
            if response.status_code in (
                requests.codes["unauthorized"],
                requests.codes["forbidden"],
            ):
                raise DeeplAuthorizationError(
                    "Authorization failed, is your API key correct?"
                )

            # DeepL sends back error messages in the response body.
            #   Try to fetch them to construct more helpful exceptions.
            if not response.ok:
                try:
                    data = response.json()
                    if data["message"]:
                        raise DeeplServerError(
                            f"An error occurred while communicating with the DeepL server: '{data['message']}'."
                        )
                # In case the message could not be decoded, just go on to raise
                #   a built-in "requests" exception.
                except (ValueError):
                    pass

            # Use the default error handling of "requests".
            response.raise_for_status()
            return response.json()

    def usage_information(self) -> UsageInformation:
        """
        Retrieve information about API usage & limits.
        This can also be used to verify an API key without consuming translation contingent.

        See also the [vendor documentation](https://www.deepl.com/docs-api/other-functions/monitoring-usage/).
        """

        data = self._api_call("/usage")

        if not "character_count" in (data):
            raise DeeplDeserializationError()

        return UsageInformation(
            character_count=data["character_count"],
            character_limit=data["character_limit"],
        )

    # Private method to make the API calls for the language lists.
    def _languages(self, ltype: str):
        data = self._api_call("/languages", {"type": ltype})

        if not "language" in (data[0]):
            raise DeeplDeserializationError()

        return {item["language"]: item["name"] for item in data}

    def source_languages(self) -> dict:
        """
        Retrieve all currently available source languages.

        See also the [vendor documentation](https://www.deepl.com/docs-api/other-functions/listing-supported-languages/).
        """

        return self._languages("source")

    def target_languages(self) -> dict:
        """
        Retrieve all currently available target languages.

        See also the [vendor documentation](https://www.deepl.com/docs-api/other-functions/listing-supported-languages/).
        """

        return self._languages("target")

    def translate(
        self,
        *,
        source_language: str = None,
        target_language: str,
        split_sentences: SplitSentences = None,
        preserve_formatting: bool = None,
        formality: Formality = None,
        texts: list,
    ) -> list:
        """
        Translate one or more text chunks at once. You can pass in optional
        translation options if you need non-default behaviour.

        Please see the parameter documentation and the
        [vendor documentation](https://www.deepl.com/docs-api/translating-text/) for details.

        Returns a list of dictionaries for the translated content:

        ```python
        [
            {
                "detected_source_language": "DE",
                "text": "Yes. No.",
            },
            ...
        ]
        ```
        """

        payload = {
            "target_lang": target_language,
            "text": texts,
        }
        if source_language != None:
            payload["source_lang"] = source_language

        if split_sentences != None:
            payload["split_sentences"] = split_sentences.value

        if preserve_formatting != None:
            payload["preserve_formatting"] = 1 if preserve_formatting else 0

        if formality != None:
            payload["formality"] = formality.value

        data = self._api_call("/translate", payload)

        if not "translations" in (data):
            raise DeeplDeserializationError

        return data["translations"]

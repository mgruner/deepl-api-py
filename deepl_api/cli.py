"""
Unix-style commandline application for integrating the
[DeepL API](https://www.deepl.com/docs-api/) into toolchains without any programming effort.

*If you are looking for the `deepl-api` API library, please refer
to [its documentation](../deepl_api/index.html) instead.*

.. include:: ./doc_cli.md
"""

import click
import sys
import os
import pathlib

import deepl_api


@click.group()
def run():
    pass


@run.command()
def usage_information():
    try:
        deepl = _get_instance()
        usage = deepl.usage_information()

        print(f"Available characters per billing period: {usage.character_limit}")
        print(
            f"Characters already translated in the current billing period: {usage.character_count}"
        )

    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


@run.command()
def languages():
    try:
        deepl = _get_instance()
        source_langs = deepl.source_languages()
        target_langs = deepl.target_languages()

        print("DeepL can translate from the following source languages:")
        for language, name in source_langs.items():
            print(f"  {language.ljust(5)} ({name})")

        print()
        print("DeepL can translate to the following target languages:")
        for language, name in target_langs.items():
            print(f"  {language.ljust(5)} ({name})")

    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


@run.command()
@click.option("-s", "--source-language", required=False)
@click.option("-t", "--target-language", required=True)
@click.option("-i", "--input-file", required=False)
@click.option("-o", "--output-file", required=False)
@click.option("-p", "--preserve-formatting", default=None, is_flag=True)
@click.option("-m", "--formality-more", default=None, is_flag=True)
@click.option("-l", "--formality-less", default=None, is_flag=True)
def translate(
    source_language,
    target_language,
    input_file,
    output_file,
    preserve_formatting,
    formality_more,
    formality_less,
):
    try:
        deepl = _get_instance()

        if input_file != None:
            text = pathlib.Path(input_file).read_text()
        else:
            text = sys.stdin.read()

        formality = deepl_api.Formality.DEFAULT
        if formality_less:
            formality = deepl_api.Formality.LESS
        if formality_more:
            formality = deepl_api.Formality.MORE

        translations = deepl.translate(
            source_language=source_language,
            target_language=target_language,
            preserve_formatting=preserve_formatting,
            formality=formality,
            texts=[text],
        )

        translated_text = "\n".join([entry["text"] for entry in translations])

        if output_file != None:
            pathlib.Path(output_file).write_text(translated_text)
        else:
            print(translated_text)

    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        sys.exit(1)


def _get_instance():
    api_key = os.getenv("DEEPL_API_KEY", "")
    if not len(api_key):
        sys.stderr.write(
            "Error: no DEEPL_API_KEY found. Please provide your API key in this environment variable.\n"
        )
        sys.exit(1)
    return deepl_api.DeepL(api_key)


if __name__ == "__main__":
    run()

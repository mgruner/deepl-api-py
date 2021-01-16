import pytest
import pathlib
from click.testing import CliRunner

from deepl_api import cli
from deepl_api.exceptions import DeeplAuthorizationError, DeeplServerError


def test_help():
    runner = CliRunner()
    result = runner.invoke(cli.run)
    assert result.exit_code == 0
    assert result.output.find("Usage") > -1


def test_auth():
    runner = CliRunner()
    result = runner.invoke(cli.run, ["usage-information"])
    assert result.exit_code == 0

    runner = CliRunner(env={"DEEPL_API_KEY": ""})
    result = runner.invoke(cli.run, ["usage-information"])
    assert result.exit_code == 1
    assert (
        result.output
        == "Error: no DEEPL_API_KEY found. Please provide your API key in this environment variable.\n"
    )

    runner = CliRunner(env={"DEEPL_API_KEY": "false"})
    result = runner.invoke(cli.run, ["usage-information"])
    assert result.exit_code == 1
    assert result.output == "Error: Authorization failed, is your API key correct?\n"


def test_usage_information():
    runner = CliRunner()
    result = runner.invoke(cli.run, ["usage-information"])
    assert result.exit_code == 0
    assert result.output.find("Available characters per billing period:") > -1


def test_languages():
    runner = CliRunner()
    result = runner.invoke(cli.run, ["languages"])
    assert result.exit_code == 0
    assert result.output.find("RU    (Russian)") > -1


def test_translate():
    # Missing target language
    runner = CliRunner()
    result = runner.invoke(cli.run, ["translate"], input="Please go home.")
    assert result.exit_code == 2
    assert result.output.find("Missing option") > -1

    # STDIN/STDOUT
    result = runner.invoke(
        cli.run, ["translate", "-s", "EN", "-t", "DE"], input="Please go home."
    )
    assert result.exit_code == 0
    assert result.output == "Bitte gehen Sie nach Hause.\n"

    # Invalid target language
    result = runner.invoke(
        cli.run, ["translate", "-s", "EN", "-t", "FALSE"], input="Please go home."
    )
    assert result.exit_code == 1
    assert (
        result.output
        == "Error: An error occurred while communicating with the DeepL server: 'Value for 'target_lang' not supported.'.\n"
    )

    # Via valid files
    with runner.isolated_filesystem():
        pathlib.Path("input_file.txt").write_text("Please go home.")
        result = runner.invoke(
            cli.run,
            [
                "translate",
                "-s",
                "EN",
                "-t",
                "DE",
                "-i",
                "input_file.txt",
                "-o",
                "output_file.txt",
            ],
        )
        assert result.exit_code == 0
        assert (
            pathlib.Path("output_file.txt").read_text() == "Bitte gehen Sie nach Hause."
        )

    # Invald input file path
    with runner.isolated_filesystem():
        result = runner.invoke(
            cli.run,
            [
                "translate",
                "-s",
                "EN",
                "-t",
                "DE",
                "-i",
                "missing_input_file.txt",
                "-o",
                "output_file.txt",
            ],
        )
        assert result.exit_code == 1
        assert (
            result.output
            == "Error: [Errno 2] No such file or directory: 'missing_input_file.txt'\n"
        )

    # Invalid output file path
    with runner.isolated_filesystem():
        pathlib.Path("input_file.txt").write_text("Please go home.")
        result = runner.invoke(
            cli.run,
            [
                "translate",
                "-s",
                "EN",
                "-t",
                "DE",
                "-i",
                "input_file.txt",
                "-o",
                "nonexisting/file/path",
            ],
        )
        assert result.exit_code == 1
        assert (
            result.output
            == "Error: [Errno 2] No such file or directory: 'nonexisting/file/path'\n"
        )

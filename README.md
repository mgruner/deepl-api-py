# deepl-api-py

This repository contains a [Python](https://www.python.org/) implementation of the [DeepL REST API](https://www.deepl.com/docs-api/).

## Contents

- A [Python package](https://mgruner.github.io/deepl-api-py-docs/deepl_api/index.html) for easy integration into Python applications.
- The `deepl` [unix-style commandline application](https://mgruner.github.io/deepl-api-py-docs/deepl_api/cli.html) for integration into existing toolchains without any programming effort.
- Unit and integration tests.

Please refer to the linked documentation for instructions on how to get started with the API and/or the CLI tool.

## Features

- Query your account usage & limits information.
- Fetch the list of available source and target languages provided by DeepL.
- Translate text.

## Not Implemented

- Support for the [(beta) document translation endpoint](https://www.deepl.com/docs-api/translating-documents/).
- Support for the [XML handling flags](https://www.deepl.com/docs-api/translating-text/) in the translation endpoint.

## See Also

There are comparable implementations for [Rust](https://github.com/mgruner/deepl-api-rs) and [Ruby](https://github.com/mgruner/deepl-api-rb).

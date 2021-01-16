## Requirements

You need to have a valid [DeepL Pro Developer](https://www.deepl.com/pro#developer) account
with an associated API key. This key must be made available to the application, e. g. via
environment variable:

```bash
export DEEPL_API_KEY=YOUR_KEY
```

## Example

```python
import os
import pytest
import deepl_api


def test_documentation():

    # Create a DeepL instance for our account.
    deepl = deepl_api.DeepL(os.getenv("DEEPL_API_KEY"))

    # Translate Text
    translations = deepl.translate(source_language="DE", target_language="EN-US", texts=["ja"])
    assert translations == [{"detected_source_language": "DE", "text": "yes"}]

    # Fetch Usage Information
    usage_information = deepl_api.DeepL(os.getenv("DEEPL_API_KEY")).usage_information()
    assert usage_information.character_limit > 0

```

## See Also

The main API functions are documented in the `deepl_api.DeepL` class.
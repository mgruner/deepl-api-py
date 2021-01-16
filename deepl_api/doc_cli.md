## Requirements

You need to have a valid [DeepL Pro Developer](https://www.deepl.com/pro#developer) account
with an associated API key. This key must be made available to the application, e. g. via
environment variable:

```bash
export DEEPL_API_KEY=YOUR_KEY
```

## Examples

### Overview

To get an overview of the available commands, just invoke the program.

```text
shell> deepl
Usage: deepl [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  languages
  translate
  usage-information
```

You can call `deepl translate --help` to get a detailed reference for the various options of the
`translate` command, for example.

### Translating Text

By default, `deepl` reads from `STDIN` and writes to `STDOUT`, which means that you can integrate
it nicely into toolchains.

```text
shell> echo "Please go home." | deepl translate --source-language EN --target-language DE | cat -
Bitte gehen Sie nach Hause.
```

By providing the options `--input-file` and / or `--output-file`, you can tell `deepl` to
read from / write to files, rather than `STDIN` / `STDOUT`.

### Retrieving Account Usage & Limits

```text
shell> deepl usage-information
Available characters per billing period: 250000
Characters already translated in the current billing period: 3317
```

### Retrieving Available Languages

```text
shell> deepl languages
DeepL can translate from the following source languages:
  DE    (German)
  EN    (English)
  ES    (Spanish)
  ...

DeepL can translate to the following target languages:
  DE    (German)
  EN-GB (English (British))
  EN-US (English (American))
  ES    (Spanish)
  ...
```
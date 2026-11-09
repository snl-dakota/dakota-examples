# Python API Examples

These examples demonstrate building and running Dakota studies using the
`dakota.study` Python API instead of a freeform `.in` file.  Each example is
self-contained and includes a `README.md` with a description and instructions.

## Examples

| Directory | What it demonstrates |
|-----------|----------------------|
| [`sampling/`](sampling/) | Basic study structure — variables, interface, responses, model, method |
| [`callback/`](callback/) | Injecting a Python function as the analysis driver callback |
| [`nested/`](nested/) | Nested model construction for optimization under uncertainty |
| [`to-json/`](to-json/) | Using `dakota-to-json` to translate a freeform input to a Python study |

## Prerequisites

- Dakota installed with the Python API (`dakota.study` package importable)
- `text_book` executable on `PATH` (shipped with Dakota)
- For the callback example: `dakota.interfacing` available

## Further reading

- [Python API reference](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/libraryapi/python-reference.html)
- [JSON format input files](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/inputfile/json.html)

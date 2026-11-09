# Summary

Demonstrates using `dakota-to-json` to convert a freeform Dakota input file
to JSON, and how to use the resulting JSON as a guide for writing the
equivalent Python API study.

# Description

`dakota-to-json` is a command-line tool that converts a freeform `.in` file
to Dakota's JSON input format.  The JSON uses the same block structure and
keyword names as the Python API's configuration arguments, so reading the JSON
is an effective way to understand how any existing study maps to Python API
calls — and to translate it.

## Workflow

1. **Convert** a freeform input file to JSON:

   ```
   dakota-to-json study.in study.json
   ```

2. **Read the JSON** to see the canonical form of each block.  For example, a
   variables block that reads

   ```
   uniform_uncertain 2
     lower_bounds 0.0 0.0
     upper_bounds 1.0 1.0
   ```

   appears in the JSON as:

   ```json
   "variables": [
     {
       "uniform_uncertain": {
         "count": 2,
         "lower_bounds": [0.0, 0.0],
         "upper_bounds": [1.0, 1.0]
       }
     }
   ]
   ```

   The inner dict — `{"uniform_uncertain": {"count": 2, ...}}` — is exactly
   what you pass to `study.variables(...)` in the Python API.  The same
   correspondence holds for `responses`, `interface`, and method configuration.

3. **Write the Python study** following `study.py` in this directory, which
   implements the same study as `study.in`.

## Running the JSON file directly

The generated `study.json` can also be run without the Python API:

```
dakota -json study.json
```

This is useful for verifying that the conversion is correct before porting to
the Python API.

# Contents

- `study.in` — the original freeform Dakota input
- `study.py` — the Python API equivalent; run with `python study.py`

# How to run the example

```
python study.py
```

The `text_book` executable must be on `PATH`.  Dakota writes `dakota.out` and
`dakota.err` to the working directory.

To convert `study.in` and inspect the intermediate JSON:

```
dakota-to-json study.in study.json
```

# Further reading

- [JSON format input files](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/inputfile/json.html)
- [Python API reference](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/libraryapi/python-reference.html)

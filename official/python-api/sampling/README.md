# Summary

An LHS sampling study constructed with Dakota's Python API using an external
fork driver.

# Description

This is the simplest end-to-end Python API study.  It shows how each block of
a Dakota input file maps to a Python call:

| Input-file block | Python API call |
|-----------------|-----------------|
| `variables` | `study.variables(...)` |
| `interface` | `study.interface(...)` |
| `responses` | `study.responses(variables, ...)` |
| `model` | `study.model.simulation(variables, interface, responses)` |
| `method` | `study.method.sampling(model, ...)` |
| Run | `study.run(iterator)` |

Variables, responses, and interface are created first; a simulation model
bundles them together; a method iterator is created from the model; and
`study.run()` executes everything.  Dakota tracks ownership — all objects
created from `study` share the same runtime context.

# Contents

- `study.py` — the Python API study

# How to run the example

```
python study.py
```

The `text_book` executable must be on `PATH`.  Dakota writes `dakota.out` and
`dakota.err` to the working directory.

# Further reading

- [Python API reference](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/libraryapi/python-reference.html)
- [sampling method reference](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/reference/method-sampling.html)

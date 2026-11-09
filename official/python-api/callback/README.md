# Summary

A gradient-based optimization study in which a Python function decorated with
`@python_interface` is passed directly to the interface as a callback, avoiding
subprocess overhead.

# Description

When your simulation is a Python function, passing it as `callback=` to
`study.interface()` tells Dakota to call it in-process rather than forking a
subprocess.  The function receives `params` and `results` objects, writes the
response value into `results`, and returns it.

```python
from dakota.interfacing import python_interface

@python_interface
def rosenbrock(params, results):
    x1, x2 = params["x1"], params["x2"]
    results["f"].function = 100.0 * (x2 - x1**2)**2 + (1.0 - x1)**2
    return results

interface = study.interface(callback=rosenbrock)
```

The `@python_interface` decorator translates Dakota's internal parameters and
results objects into the `Parameters` and `Results` objects from
`dakota.interfacing`, so the function can use the familiar dict-like API
(`params["x1"]`, `results["f"].function`, etc.) rather than Dakota's raw
internal representation.

The study uses numerical gradients, so the callback only needs to return
function values.  Dakota computes finite differences by calling the callback
multiple times with small perturbations.

# Contents

- `study.py` — the Python API study with the driver defined inline

# How to run the example

```
python study.py
```

Dakota writes `dakota.out` and `dakota.err` to the working directory.

# Further reading

- [python\_interface reference](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/reference/interface-analysis_drivers-python.html)
- [Python API reference](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/libraryapi/python-reference.html)

# Summary

An optimization under uncertainty (OUU) study built with the Python API,
using a nested model to compose an inner LHS sampler inside an outer
gradient-free optimizer.

# Description

A nested model lets you embed one Dakota study inside another and wire
statistics from the inner study to the outer study's objectives or constraints.
This example uses that to perform robust design optimization: the outer
`coliny_pattern_search` optimizer varies the design variables to minimize the
*expected* (mean) simulation response, where the expectation is estimated at
each design point by an inner LHS sampler over an aleatory uncertain variable.

## Building the study inside-out

The Python API requires building a nested model from the innermost objects
outward:

1. **Inner model** — create the inner variables, interface, and responses,
   then assemble them into a `simulation` model.
2. **Inner iterator** — create a `sampling` iterator from the inner model.
3. **Nested model** — inject the inner iterator plus the outer variables and
   responses into `model.nested(...)`.
4. **Outer iterator** — create `coliny_pattern_search` from the nested model.

```python
inner_model  = study.model.simulation(inner_vars, interface, inner_resp)
inner_sampler = study.method.sampling(inner_model, ...)
nested_model  = study.model.nested(inner_sampler, outer_vars, outer_resp, ...)
study.run(study.method.coliny_pattern_search(nested_model, ...))
```

## Key configuration points

**`active={"uncertain": True}`** on the inner variables tells the inner
sampler to vary only the uncertain variable `u`; the design variables `x1`
and `x2` are fixed at values injected from the outer layer.

**`primary_variable_mapping`** in the `sub_method_pointer` config names which
inner design variables receive the outer design values at each outer
evaluation.

**`primary_response_mapping`** specifies a row vector that linearly combines
the inner statistics into the outer response.  `[1.0, 0.0]` selects the first
inner statistic (the sample mean) as the outer objective.

# Contents

- `study.py` — the Python API study

# How to run the example

```
python study.py
```

The `text_book` executable must be on `PATH`.  Dakota writes `dakota.out` and
`dakota.err` to the working directory.

# Further reading

- [nested model reference](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/reference/model-nested.html)
- [Python API reference](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/libraryapi/python-reference.html)
- [coliny\_pattern\_search reference](https://snl-dakota.github.io/docs/latest_release/users/usingdakota/reference/method-coliny_pattern_search.html)

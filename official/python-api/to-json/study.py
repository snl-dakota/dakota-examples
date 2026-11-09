"""Python API equivalent of study.in.

The JSON produced by `dakota-to-json study.in study.json` reveals the
canonical block structure; this file expresses the same study using the
Python API.  Compare study.in, study.json, and this file side by side to
see how freeform keywords, JSON fields, and Python API arguments correspond.
"""

from dakota.study import Study, StudyConfig

config = StudyConfig()
config.output.output_file = "dakota.out"
config.output.error_file = "dakota.err"
study = Study(config)

variables = study.variables(
    uniform_uncertain={
        "count": 2,
        "lower_bounds": [0.0, 0.0],
        "upper_bounds": [1.0, 1.0],
    }
)
responses = study.responses(
    variables,
    {
        "response_type": {"response_functions": {"count": 1}},
        "gradient_type": {"no_gradients": True},
        "hessian_type": {"no_hessians": True},
    },
)
interface = study.interface(
    analysis_drivers={"drivers": ["text_book"], "interface_type": {"fork": {}}}
)
model = study.model.simulation(variables, interface, responses)
study.run(
    study.method.sampling(model, samples=20, seed=1234, sample_type={"lhs": True})
)

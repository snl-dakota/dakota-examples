"""LHS sampling study on text_book using a fork interface.

Equivalent freeform input:

    environment
      output_file 'dakota.out'
      error_file 'dakota.err'
    method
      sampling samples 20 seed 1234 sample_type lhs
    variables
      uniform_uncertain 2
        lower_bounds 0.0 0.0
        upper_bounds 1.0 1.0
    interface
      analysis_drivers 'text_book' fork
    responses
      response_functions 1
      no_gradients
      no_hessians
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

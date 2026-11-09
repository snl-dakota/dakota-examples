"""Optimization under uncertainty using a nested model.

An outer pattern search minimizes the expected text_book response over two
design variables.  At each candidate design point the inner LHS sampler
draws 20 samples of an aleatory uncertain variable, evaluates text_book, and
returns the sample mean to the outer optimizer as the objective.
"""

from dakota.study import Study, StudyConfig

config = StudyConfig()
config.output.output_file = "dakota.out"
config.output.error_file = "dakota.err"
study = Study(config)

# --- outer optimizer ---
# The outer optimizer sees only the design variables and the scalar objective
# returned by the nested model (the inner sample mean).
outer_variables = study.variables(
    continuous_design={
        "count": 2,
        "initial_point": [1.5, 1.5],
        "lower_bounds": [0.5, 0.5],
        "upper_bounds": [2.5, 2.5],
        "descriptors": ["x1", "x2"],
    }
)
outer_responses = study.responses(
    outer_variables,
    {
        "response_type": {"objective_functions": {"count": 1}},
        "gradient_type": {"no_gradients": True},
        "hessian_type": {"no_hessians": True},
    },
)

# --- inner UQ model ---
# active={"uncertain": True} restricts the inner sampler to the uncertain
# variable u.  The design variables x1 and x2 are held fixed at the values
# injected from the outer layer via primary_variable_mapping.
inner_variables = study.variables(
    active={"uncertain": True},
    continuous_design={
        "count": 2,
        "initial_point": [1.5, 1.5],
        "lower_bounds": [0.5, 0.5],
        "upper_bounds": [2.5, 2.5],
        "descriptors": ["x1", "x2"],
    },
    uniform_uncertain={
        "count": 1,
        "lower_bounds": [0.5],
        "upper_bounds": [1.5],
        "descriptors": ["u"],
    },
)
inner_responses = study.responses(
    inner_variables,
    {
        "response_type": {"response_functions": {"count": 1}},
        "gradient_type": {"no_gradients": True},
        "hessian_type": {"no_hessians": True},
    },
)
inner_interface = study.interface(
    analysis_drivers={"drivers": ["text_book"], "interface_type": {"fork": {}}}
)
inner_model = study.model.simulation(inner_variables, inner_interface, inner_responses)

inner_sampler = study.method.sampling(
    inner_model, samples=20, seed=1234, sample_type={"lhs": True}
)

# --- nested model ---
# primary_variable_mapping injects outer x1 and x2 into the inner design
# variables.  primary_response_mapping [1.0, 0.0] selects the inner sample
# mean (the first statistic) as the outer objective.
model = study.model.nested(
    inner_sampler,
    outer_variables,
    outer_responses,
    sub_method_pointer={
        "primary_variable_mapping": ["x1", "x2"],
        "primary_response_mapping": [1.0, 0.0],
    },
)

study.run(
    study.method.coliny_pattern_search(
        model,
        max_iterations=10,
        max_function_evaluations=50,
        seed=1234,
        initial_delta=0.5,
        variable_tolerance=0.01,
    )
)

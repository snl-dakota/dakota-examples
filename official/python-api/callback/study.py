"""Rosenbrock minimization with an inline Python callback.

Passing a callable as callback= lets Dakota call it in-process rather than
forking a subprocess.  Numerical gradients are used so the function only
needs to return the objective value; Dakota computes finite differences itself.
"""

from dakota.study import Study, StudyConfig
from dakota.interfacing import python_interface

@python_interface
def rosenbrock(params, results):
    x1, x2 = params["x1"], params["x2"]
    results["f"].function = 100.0 * (x2 - x1**2) ** 2 + (1.0 - x1) ** 2
    return results


config = StudyConfig()
config.output.output_file = "dakota.out"
config.output.error_file = "dakota.err"
study = Study(config)

variables = study.variables(
    continuous_design={
        "count": 2,
        "initial_point": [-1.2, 1.0],
        "lower_bounds": [-2.0, -2.0],
        "upper_bounds": [2.0, 2.0],
        "descriptors": ["x1", "x2"],
    }
)
interface = study.interface(callback=rosenbrock)
responses = study.responses(
    variables,
    {
        "response_type": {"objective_functions": {"count": 1}},
        "gradient_type": {
            "numerical_gradients": {
                "method_source": {"dakota": {}},
                "interval_type": {"forward": True},
                "fd_step_size": [0.0001],
            }
        },
        "hessian_type": {"no_hessians": True},
        "descriptors": ["f"],
    },
)
model = study.model.simulation(variables, interface, responses)
study.run(
    study.method.conmin_mfd(
        model,
        config={"max_iterations": 100, "convergence_tolerance": 1e-8},
    )
)

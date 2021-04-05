#!/usr/bin/env python3
from rosenbrock import rosenbrock_list
import dakota.interfacing as di


# Dakota will execute this script as
#   rosenbrock_bb_di.py params.in results.out
#  The command line arguments will be extracted by dakota.interfacing automatically.


def pack_rosen_parameters(dakota_params, dakota_results):
    """Pack rosenbrock_list input dictionary
    
    There is assumed to be two variables, x1 and x2, and a single response, obj_fn
    """
    continuous_vars = [ dakota_params['x1'], dakota_params['x2'] ]

    active_set_vector = 0
    if dakota_results["obj_fn"].asv.function:
        active_set_vector += 1
    if dakota_results["obj_fn"].asv.gradient:
        active_set_vector += 2
    if dakota_results["obj_fn"].asv.hessian:
        active_set_vector += 4
    
    rosen_input = {
        "cv": continuous_vars,
        "functions": 1,
        "asv": [active_set_vector]
    }    

    return rosen_input


def pack_dakota_results(rosen_output, dakota_results):
    """Insert results from rosenbrock into Dakota results

    Although we need to handle just one response, this function demonstrates iteration
    over response labels (or descriptors) for educational purposes.
    """
    for i, label in enumerate(dakota_results):
        if dakota_results[label].asv.function:
            dakota_results[label].function = rosen_output["fns"][i]
        if dakota_results[label].asv.gradient:
            dakota_results[label].gradient = rosen_output["fnGrads"][i]
        if dakota_results[label].asv.hessian:
            dakota_results[label].hessian = rosen_output["fnHessians"][i]
    
    return dakota_results


def main():

    params, results = di.read_parameters_file()
    rosen_input = pack_rosen_parameters(params, results)

    rosen_output = rosenbrock_list(**rosen_input)
    
    results = pack_dakota_results(rosen_output, results)
    results.write()


if __name__ == '__main__':
    main()

#!/usr/bin/env python3

from textbook import textbook_list
import dakota.interfacing as di


def pack_textbook_parameters(dakota_params, dakota_results):
    """Pack textbook input dictionary
    
    There is assumed to be three variables, x1, x2 and x3, and a single response, obj_fn
    together with two nonlinear inequality constraints
    """
    continuous_vars = [ dakota_params['x1'], dakota_params['x2'], dakota_params['x3'] ]

    asv_vec = []
    for i, label in enumerate(dakota_results):
        active_set_vector = 0
        if dakota_results[label].asv.function:
            active_set_vector += 1
        if dakota_results[label].asv.gradient:
            active_set_vector += 2
        if dakota_results[label].asv.hessian:
            active_set_vector += 4
        asv_vec.append(active_set_vector)
    
    textbook_input = {
        "cv": continuous_vars,
        "functions": 3,
        "asv": asv_vec
    }    

    return textbook_input


def pack_dakota_results(fns, grads, hessians, dakota_results):
    """Insert results from textbook into Dakota di results object

    """
    for i, label in enumerate(dakota_results):
        if dakota_results[label].asv.function:
            dakota_results[label].function = fns[i]
        if dakota_results[label].asv.gradient:
            dakota_results[label].gradient = grads[i]
        if dakota_results[label].asv.hessian:
            dakota_results[label].hessian = hessians[i]
    
    return dakota_results


@di.python_interface
def decorated_driver(params, results):

    textbook_input = pack_textbook_parameters(params, results)
    fns, grads, hessians = textbook_list(textbook_input)
    results = pack_dakota_results(fns, grads, hessians, results)

    return results


def driver(dakota_params):

    params, results = di.read_params_from_dict(dakota_params)
    textbook_input = pack_textbook_parameters(params, results)

    fns, grads, hessians = textbook_list(textbook_input)

    results = pack_dakota_results(fns, grads, hessians, results)

    direct_results_dict = results.return_direct_results_dict()

    return direct_results_dict


if __name__ == '__main__':
    driver()

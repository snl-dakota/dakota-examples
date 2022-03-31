#!/usr/bin/env python3

from textbook import textbook_list
import dakota.interfacing as di


def pack_textbook_parameters(dakota_params, dakota_results):
    """Pack textbook input dictionary
    
    There is assumed to be two variables, x1 and x2, and a single response, obj_fn
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


def pack_dakota_results(textbook_output, dakota_results):
    """Insert results from textbook into Dakota di results object

    *** THIS FUNTION IS NOT USED WHEN THIS DRIVER IS CALLED BY DAKOTA'S
        DIRECT PYTHON INTERFACE.
    """
    for i, label in enumerate(dakota_results):
        if dakota_results[label].asv.function:
            dakota_results[label].function = textbook_output["fns"][i]
        if dakota_results[label].asv.gradient:
            dakota_results[label].gradient = textbook_output["fnGrads"][i]
        if dakota_results[label].asv.hessian:
            dakota_results[label].hessian = textbook_output["fnHessians"][i]
    
    return dakota_results


def main(dakota_params):

    params, results = di.read_params_from_dict(dakota_params)
    textbook_input = pack_textbook_parameters(params, results)

    textbook_output = textbook_list(textbook_input)
    
    return textbook_output


if __name__ == '__main__':
    main()

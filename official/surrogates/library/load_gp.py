import numpy as np
import sys

def print_gp_history(gp):
    obj_fun_values = gp.objective_function_history()
    print("GP MLE objective function value history:\n{0}\n".format(obj_fun_values))
    
    obj_grad_values = gp.objective_gradient_history()
    print("GP MLE objective gradient history:\n{0}\n".format(obj_grad_values))
    
    theta_values = gp.theta_history()
    print("GP MLE hyperparameter (theta) history:\n{0}\n".format(theta_values))

if __name__ == '__main__':
    import dakota.surrogates as daksurr
    morris_gp = daksurr.load("morris.gp.bin", True)
    print_gp_history(morris_gp)


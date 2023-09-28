#!/usr/bin/env python3
import dakota.interfacing as di
import random

params, results = di.read_parameters_file()
seed = 12345*params.eval_id
random.seed(seed) 

x1, x2, x3, x4 = params["x1"], params["x2"], params["x3"], params["x4"]

eps = random.uniform(-0.2, 0.2)
 
results["f"].function = 10. * x1 + 1. * x2 + 0.1 * x3 + 0.01 * x4 + eps
results.write()

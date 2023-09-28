#!/usr/bin/env python3
import dakota.interfacing as di
 
params, results = di.read_parameters_file()
 
x1, x2, x3, x4 = params["x1"], params["x2"], params["x3"], params["x4"]
 
results["y"].function = 10. * x1 + x2 * x2 + x3 * x3 * x3 + x4 * x4 * x4 * x4
results.write()

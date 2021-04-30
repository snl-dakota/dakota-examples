#!/usr/bin/env python3
import numpy as np
import dakota.interfacing as di

w = 2.5
t = 1.5
L = 100.0
X = 0

def displacement(w, t, L, X, Y, T, E0, Es):
    E = E0 + Es*T
    d = 4*L**3/(E*w*t)*np.sqrt((Y/t**2.0)**2.0 + 
          (X/w**2.0)**2.0)
    return d

params, results = di.read_parameters_file()

num_T_points = int(params.an_comps[0])

T = np.linspace(-20, 500, num_T_points)
d = displacement(w, t, L, X, params["Y"], T, params["E0"],
                   params["Es"])

for i, r in enumerate(d):
    results[i].function = r

results.write()


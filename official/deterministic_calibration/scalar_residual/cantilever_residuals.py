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

d_exp =np.array([6.3939197,
          6.25687963,
          6.54871886,
          6.40392764,
          6.39315616,
          6.58423497,
          6.61206657,
          6.4933339,
          6.58972801,
          6.3953598,
          6.76640387,
          6.78267337,
          6.81120057,
          6.54644753,
          6.74819021,
          6.81515953,
          6.88917241,
          6.91155018,
          7.04911027,
          6.79700202])


T = np.linspace(-20, 500, num_T_points)
d = displacement(w, t, L, X, params["Y"], T, params["E0"],
                   params["Es"])

residuals = d - d_exp

for i, r in enumerate(residuals):
    results[i].function = r

results.write()


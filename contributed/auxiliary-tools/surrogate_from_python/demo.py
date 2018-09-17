#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

import numpy as np

import dakota_surrogate

try:
    from importlib import reload
except ImportError:
    pass
reload(dakota_surrogate)

## Build test data and a test function
def fun(X):
    """ 
                x^2 * y
    f(x,y,z) = ---------   + arctan( 2 * pi * (x - y) )
               |z| + 0.1
    """
    X = np.atleast_2d(X)
    x,y,z = X.T
    return x**2*y/(np.abs(z) + 0.1) + np.arctan(2*np.pi*(x - y))

np.random.seed(1)
X = np.random.uniform(size=(30,3))
f = fun(X)

# Build a tester to see the errors:
np.random.seed(2)
Xerr = np.random.uniform(size=(10**3,3))
ferr = fun(Xerr)

## Setup
# In this example, dakota is installed and available. However, the following 
# could also be used to set it on some platforms

#import subprocess
#dakota = subprocess.check_output('module load dakota;command which dakota',shell=True).decode('utf8').strip()

# because it is installed, but to be consistent:
dakota = 'dakota'

## Method 1: Dakota class

# Build the surrogate and test the different surrogate forms
dak = dakota_surrogate.DakotaSurrogate(X,f,bounds=[0,1],dakota=dakota)

for surrogate in ['polynomial quadratic',
                  'neural_network',
                  'gaussian_process surfpack trend constant',
                  'gaussian_process surfpack trend linear',
                  'gaussian_process surfpack trend reduced_quadratic',
                  'gaussian_process surfpack trend quadratic',
                  'radial_basis',
                  'moving_least_squares',
                  'mars']:
    fdak = dak(Xerr,surrogate=surrogate)
    err = np.linalg.norm( ferr - fdak ) / np.linalg.norm( ferr )
    print("Relative Error: {:15.8e} '{:s}'".format(err,surrogate))

## Method 2: Dakota function
for surrogate in ['polynomial quadratic',
                  'neural_network',
                  'gaussian_process surfpack trend constant',
                  'gaussian_process surfpack trend linear',
                  'gaussian_process surfpack trend reduced_quadratic',
                  'gaussian_process surfpack trend quadratic',
                  'radial_basis',
                  'moving_least_squares',
                  'mars']:
    fdak = dakota_surrogate.dakota_surrogate(X,f,Xerr,surrogate=surrogate,dakota=dakota)
    err = np.linalg.norm( ferr - fdak ) / np.linalg.norm( ferr )
    print("Relative Error: {:15.8e} '{:s}'".format(err,surrogate))
    
    
    

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python interface to a *simple* dakota surrogate
"""
from __future__ import division, print_function, unicode_literals

__version__ = '20180917'

import sys
if sys.version_info[0] >2:
    imap = map
    unicode = str
else:
    from itertools import imap

import numpy as np

import os
import uuid
import subprocess

__all__ = ['DakotaSurrogate','dakota_surrogate']

class DakotaSurrogate:
    """
    Build a surrogate with Dakota.
    
    Last tested with Dakota 6.8
    """
    input = u"""
        environment tabular_data tabular_data_file = '{out}' freeform
        variables,
            uniform_uncertain =  {ndim}
            lower_bounds    =    {lower}    
            upper_bounds    =    {upper} 
        method list_parameter_study import_points_file = '{in}' freeform
        model surrogate global {surrogate} 
        import_build_points_file = '{build}' freeform
        responses response_functions = 1 no_gradients no_hessians
        """
    def __init__(self,X,f,bounds=None,dakota='dakota'):
        """
        Build a surrogate by calling Dakota's  global surrogate capability.
        
        Inputs:
        -------
        X (array like)
            (N,ndim) array or (N,) vector of build points
        
        f (array like)
            (N,) vector of function values
        
        Options:
        -------
        bounds ( (ndim,2) array or (2,) vector) [None]
            upper and lower bounds for each dimension. If not specified,
            it will use the min and max of the training and sample points
            for that evaluation. Since that *will* change as the evaluation
            points change, it is better to specify them if they are known.
            If just given as a shape (2,) vector, will be the same in all
            direction
        
        dakota ( string ) ['dakota']
            Path to Dakota
        
        Important class variables
        
            run_log - list of stderr and stdout for each dakota call    
        
        """
        self.X = _vec2col(X)
        self.f = np.ravel(f)
        self.Xf = np.hstack([self.X,np.atleast_2d(self.f).T])
        self.ndim = ndim = X.shape[1]
        
        # Process bounds
        if bounds is not None:
            bounds = np.atleast_2d(bounds)
            if bounds.shape[0] == 1:
                bounds = np.tile(bounds,(ndim,1))
        self.bounds = bounds
        
        self.dakota = dakota
        
        self.run_log = []
        
    @staticmethod
    def tmpfile(save=True):
        return '/tmp/dak_' + str(uuid.uuid4())

    def predict(self,X,
                surrogate='gaussian_process surfpack trend quadratic',
                clean=True,):
        """
        Predict with Dakota
        
        Inputs:
        -------
        X (n,ndim)
            Array of values to evaluate the surrogate
        
        Options:
        --------
        surrogate ['gaussian_process surfpack trend quadratic']
            surrogate definition string for Dakota. Examples:
                'polynomial quadratic',
                'neural_network',
                'gaussian_process surfpack trend constant',
                'gaussian_process surfpack trend linear',
                'gaussian_process surfpack trend reduced_quadratic',
                'gaussian_process surfpack trend quadratic',
                'radial_basis',
                'moving_least_squares',
                'mars'
        
        clean [True]
            Whether or not to clean up afterwards
        """
        X = np.atleast_2d(X)
        
        build = self.tmpfile(save=False)
        np.savetxt(build,self.Xf)
        
        format = {'build':build,
                  'ndim':self.ndim,
                  'surrogate':surrogate,
                  'out':self.tmpfile(),
                  'in':self.tmpfile()}
                  
        bounds = self.bounds
        if bounds is None:
            XX = np.vstack([self.X,X])
            bounds = np.vstack([XX.min(axis=0),XX.max(axis=0)]).T
            bounds[:,0] += - 1e3*np.spacing(bounds[:,0])
            bounds[:,1] +=   1e3*np.spacing(bounds[:,1])
        format['lower'] = ' '.join('%0.15e' % l for l in bounds[:,0])
        format['upper'] = ' '.join('%0.15e' % l for l in bounds[:,1])
        
        np.savetxt(format['in'],X)
        
        deck = self.tmpfile()
        format['deck'] = deck
        with open(deck,'wt') as F:
            F.write(self.input.format(**format))
        
        proc = subprocess.Popen([self.dakota,deck],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        self.run_log.append(tuple(t.decode('utf8') for t in proc.communicate()))
        if proc.returncode != 0:
            raise ValueError('Error in Dakota run. See run_log[-1][1] for stderr')
        out = np.loadtxt(format['out'])
        
        if clean:
            for f in [format[ff] for ff in ('out','in','build','deck')] \
                      + ['dakota.rst','fort.13']: 
                try:
                    os.remove(f)
                except OSError:
                    pass
        
        return out[:,-1]
    __call__ = eval = predict

def dakota_surrogate(X,f,Xp,
                     bounds=None,dakota='dakota',
                     surrogate='gaussian_process surfpack trend quadratic'):
    """
    Functional form of DakotaSurrogate. See DakotaSurrogate for help
    """
    d = DakotaSurrogate(X,f,bounds=bounds,dakota=dakota)
    return d(Xp,surrogate=surrogate)

def _vec2col(x,dtype=None,return_oneD=False):
    """
    If x is 1D, convert it to a column vector. If return_oneD, will
    also return whether or not the input was 1D.
    
    Otherwise, just return it
    """
    x = np.asarray(x,dtype=dtype)
    
    if len(x.shape) > 1:
        oneD = False
    else:
        x = np.atleast_2d(x).T
        oneD = True
    
    if return_oneD:
        return x,oneD
    return x

#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Dakota Usage:
-------------
Note that responses and variables MUST have descriptors that match 
the data

    ...
    interface
     fork 
       analysis_driver = 'python annotated_data_driver.py [FLAGS] datafile'
       asynchronous evaluation_concurrency 10

    ... 

    responses
       response_functions = 1
              descriptors = 'function_name' # >>>> REQUIRED <<<<

CLI Usage:
----------
    
    annotated_data_driver.py [FLAGS] datafile paramsfile resultsfile
                                     \_user_/ \_______Dakota_______/     

Note that extra columns are ok but the response must ONLY match a single
row. Use continuous_state variables to set values if needed.
"""
from __future__ import division, print_function, unicode_literals, absolute_import
from io import open
import sys
import argparse
import re
from collections import OrderedDict

import numpy as np

__version__ ='20171025.1'

def main(args):

    data,headers = read_data_file(args.datafile)
    params_all,params = dakotaparams(args.paramsfile)
    
    # Add --set values to params
    for item in args.set:
        key,val = item.split('=')
        params[key] = float(val)

    responses = get_response_names(params_all) # doesn't need the additional params
    
    param_names = list(params.keys()) # Note params is OrderedDict
    Xparams = np.atleast_2d(np.array(list(params.values())))
    
    # get the ix of data that is params and responses. 
    # But make sure they are in order of the inputs!
    
    params_ix   = [headers.index(p) for p in param_names]
    response_ix = [headers.index(r) for r in responses]
    
    Xdata = data[:,params_ix] # Will be in order!
    
    # Scale to [0,1]
    mn = Xdata.min(axis=0)
    mx = Xdata.max(axis=0)
    rg = np.array([r if r>0 else 1 for r in (mx - mn)]) # In case it doesn't vary
    
    Xdata_scale = (Xdata - mn) / rg
    Xparams_scale = (Xparams - mn) / rg
 
    rms = np.average((Xdata_scale-Xparams_scale)**2,axis=1)
    ixmin = np.where(rms <= float(args.tol))[0] # do NOT just do min. Want to capture error if too many match
    if len(ixmin) == 0:
        print('ERROR: No values matched')
        sys.exit(2)
    if len(ixmin) > 1:
        print('ERROR: Too many values matched')
        sys.exit(2)
        
    result = data[ixmin,response_ix]
    
    # Write it
    with open(args.resultsfile,'w',encoding='utf8') as FF:
        for val,response in zip(result,responses):
            FF.write('{:0.18g} {:s}\n'.format(val,response))
    
    if args.verbose:
        txt = []
        txt.append("annotated_data_driver.py")
        txt.append("   {}".format(' '.join(sys.argv)))
        txt.append(" Input Params from '{}'".format(args.paramsfile))
        txt.extend('   {}: {:g}'.format(k,v) for k,v in params.items())
        txt.append(" Response written to '{}'".format(args.resultsfile))
        txt.extend('   {}: {:g}'.format(k,v) for v,k in zip(result,responses))
        txt.append(" Determined from datafile '{}'".format(args.datafile))
        print('\n' + '\n'.join(txt))
    
     

def dakotaparams(filepath):   
    """
    Read an input file written by Dakota in either aprepro or regular format
    
    Inputs:
    -------
    filepath - path to dakota input
    
    Returns:
    --------
    An ordered dictionary all params and then just the dakota defined ones
    """
    
    D = OrderedDict()
    text = open(filepath,'r',encoding='utf8')
        
    param_eq_val = None # Whether or not the format is decided. Will be based on
                        # the first line only
    
    for line in text:
        line = line.replace('{','').replace('}','').replace('=','').strip()
        line = line.split()
        
        if len(line) == 0:
            continue
        if len(line) != 2:
            raise ValueError('The input file or text is not in Dakota formats')
        
        a,b = line
        if param_eq_val is None:
            try:
                int(b) # Should be a numer
                param_eq_val = True # a = b
            except ValueError:
                val_eq_key = False # b a
        
        if param_eq_val:
            param,val = a,b
        else:
            param,val = b,a
        
        try:
            val = float(val)
            if round(val) == val: # is it an integer?
                val = int(val)
        except ValueError:
            pass
        D[param] = val

    text.close()
    
    # Dakota variables only...
    ks = list(D.keys())
    k0 = ks[0]
    N = int(D[k0])
    D2 = OrderedDict()
    for k in ks[1:(N+1)]:
        D2[k] = D[k]
    
    return D,D2 

def read_data_file(filepath):
    """
    Read the datafile and return an array and header. Uses heuristics
    to determine delimiter and valid columns
    """
    datafile = open(filepath,'r',encoding='utf8')
    
    firstline = next(datafile).rstrip()
    for s in ['%','#']:
        if firstline.startswith(s):
            firstline = firstline[1:].strip()
    
    # Make sure it is annotated -- this is crude
    try:
        [float(l) for l in firstline.split()]
        print('ERROR: Non-annotated input')
        sys.exit(2)
    except ValueError:
        pass 
    
    top = True
    delim = None
    keepcol = set()
    
    X = []
    for line in datafile:
        line = line.strip()
        if len(line) == 0:
            break
        if top: # First line
            top = False
            
            # Delimiter
            delim = None
            for d in [',','|']:
                if d in line:
                    delim = d
                    break
            # keepcolumns
            for ii,v in enumerate(line.split(delim)):
                try:
                    float(v)
                    keepcol.add(ii)
                except ValueError:
                    pass
                    
        
        # process the line
        X.append( [float(v) for ii,v in enumerate(line.split(delim)) if ii in keepcol])
    X = np.array(X,dtype=float)
    headers = [v.strip() for ii,v in enumerate(firstline.split(delim)) if ii in keepcol]
    return X,headers
            
def get_response_names(params_all):
    re_asv = re.compile('ASV_[0-9]+:(.*)')
    names = []
    for key in params_all.keys():
        names.extend(re_asv.findall(key))
    return names

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__,
        epilog='Version: {}'.format(__version__),
        formatter_class=argparse.RawDescriptionHelpFormatter)
    
    
    parser.add_argument('-s','--set',action='append',metavar='"param=value"',
        help="""set additional fixed values with "param=value" format. 
                Alternatively, use Dakota continuous_state variables""",default=[] )
    parser.add_argument('-t','--tol',default='1e-6',
        help=('[1e-6]. Set the tolerance. All columns are normalized to [0,1] '
              '(and the same transformation is applied to the params). ' 
              "The difference is found as the "
              'root-mean-square from the params.'))
    parser.add_argument('-v','--verbose',action='store_true',
        help="print result information")
    
    parser.add_argument('datafile',
        help=('Annotated tabular data file. The delimiter will be '
              'automatically deduced and text columns will be removed if possible. '
              'Set by the user!'))
    parser.add_argument('paramsfile',help="Dakota params file. To be set by Dakota!")
    parser.add_argument('resultsfile',help="Dakota results file. To be set by Dakota!")
    
    parser.add_argument('--version', action='version',
        version='%(prog)s-' + __version__,help=argparse.SUPPRESS)
    
    args = parser.parse_args(args=sys.argv[1:])
    main(args)





















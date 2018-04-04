#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tool to send dakota run to Matlab. See readme.md for details

Last Updated: 2018-04-04
"""
from __future__ import division, print_function, unicode_literals, absolute_import
from io import open

import sys
import os
import shutil
import argparse
import uuid
import time

if sys.version_info[0] >2:
    unicode = str

runid = unicode(uuid.uuid4()) # Unique code

# Parse command line
parser = argparse.ArgumentParser(\
            description='Add runs to Matlab',
            #epilog=epilog,
            formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('-P','--path',default='.',help="['%(default)s'] Path to store runs")
parser.add_argument('-p','--poll',default=0.33,help='[%(default)s] How often to poll for finished run')
parser.add_argument('--timeout',default=600,help='[%(default)s] How long to wait before timeing out and exiting')

parser.add_argument('params_file',help='Dakota parameters file')
parser.add_argument('results_file',help='Dakota results file (to write)')

args = parser.parse_args(sys.argv[1:])

# Read and convert to the format to send to Matlab
matlab_txt = [args.params_file]

def parse_line(line):
    for c in '{}=':
        line = line.replace(c,' ')
    val,param = line.split()
    try:
        val = float(val)
    except ValueError:
        param,val = val,param
        val = float(val)
    return val,param

with open(args.params_file,'rt',encoding='utf8') as FF:
    # First line is the number of params
    N,_ = parse_line(FF.readline())
    matlab_txt.append('{}'.format(int(N)))
    for _ in range(int(N)):
        val,param = parse_line(FF.readline())
        matlab_txt.append('{:s} {:0.16e}'.format(param,val))

# Now save it
savedir = os.path.abspath(os.path.join(args.path,'DAKOTA_MATLAB_TMP'))
inpath = os.path.join(savedir,runid + '.in')
outpath = os.path.join(savedir,runid + '.out')

try:
    os.makedirs(savedir)
except OSError:
    pass

with open(inpath,'wt',encoding='utf8') as FF:
    FF.write('\n'.join(matlab_txt))

# Finally, poll for the file to be finished. Once it is, copy for Dakota,
# delete the input, and try to delete the directory (which will work if it is
# empty)

T0 = time.time()

while True:
    if (time.time()-T0)>args.timeout:
        sys.exit(2)
    
    if os.path.exists(outpath):
        break
    
    time.sleep(args.poll)

shutil.move(outpath,args.results_file)
os.remove(inpath)

try:
    os.rmdir(savedir)
except OSError:
    pass

# Done!

    
    
    
    
    









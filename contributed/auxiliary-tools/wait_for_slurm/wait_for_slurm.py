#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tool to wait for a SLURM job to finish by polling the queue.

Usage:
    
    $ python wait_for_job.py 447787
    $ sbatch submit_script.sh | python wait_for_job.py

"""
from __future__ import  print_function, unicode_literals
__version__ = '20171107.0'

import subprocess
import sys
import argparse
import time
import select
from functools import partial

def subcall(*A,**K):
    proc = subprocess.Popen(stdout=subprocess.PIPE,stderr=subprocess.PIPE,*A,**K)
    return proc.communicate()

parser = argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)

parser.add_argument('job_id',default='-',nargs='?',
    help=('["%(default)s"] The SLURM id of the job. '
          'Will also remove any non-numeric characters. '
          'Useful for piping input. "-" means stdin'))

parser.add_argument('--init-time',default=5.0,metavar='T',
    help='[%(default)s] seconds *before* starting to look for the job in the queue')
parser.add_argument('-p','--poll',default=3.5,metavar='T',
    help='[%(default)s] seconds between polling the queue for the job')

# Version
parser.add_argument('-v', '--version', action='version', 
    version='%(prog)s-' + __version__,help=argparse.SUPPRESS)

args = parser.parse_args(sys.argv[1:])

if args.job_id == '-':
    if select.select([sys.stdin,],[],[],0.0)[0]: # source: http://stackoverflow.com/a/3763257/3633154
        args.job_id = sys.stdin.read()
    else:
        print('ERROR: Must pass stdin with `-`')
        sys.exit(2)

args.job_id = ''.join(a for a in args.job_id if a in '0123456789')

time.sleep(args.init_time)

while True:
    out,err = subcall(['squeue', '--job', '{}'.format(args.job_id)])
    
    if err.startswith('slurm_load_jobs'):
        break 
    
    time.sleep(args.poll)

    

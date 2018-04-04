#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Simple python function to detect the absence of an output and report a failure 
to Dakota

Usage: In Dakota

    interface
        fork
            ...
            
            # Detect that there was no response and change it to 'fail'
            output_filter = 'python detect_failure.py' 
        failure_capture
            retry 3

"""
from __future__ import division, print_function, unicode_literals, absolute_import
import sys,os
from io import open

input,output = sys.argv[1:]

if os.path.exists(output):
    sys.exit()

with open(output,'wt',encoding='utf8') as F:
    F.write('fail')

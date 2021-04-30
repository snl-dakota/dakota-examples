#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IshigamiFunction via the Dakota interface

f(x,y,z) = sin(x) + a*sin^2(y) + b*z**4*sin(x)

with a=7 and b=0.1

| Index | Analytical Form                                                                      | `a = 7` & `b = 0.1` |
|-------|--------------------------------------------------------------------------------------|---------------------|
| Sx    | `(pi^8*b^2/50 + pi^4*b/5 + 1/2)/(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2)`              | 0.313905191147811   |
| Sy    | `a^2/(8*(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2))`                                     | 0.442411144790041   |
| Sz    | `0`                                                                                  | 0                   |
|       |                                                                                      |                     |
| Tx    | `-a^2/(8*(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2)) + 1`                                | 0.557588855209959   |
| Ty    | `-(pi^8*b^2/18 + pi^4*b/5 + 1/2)/(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2) + 1`         | 0.442411144790041   |
| Tz    | `-(a^2/8 + pi^8*b^2/50 + pi^4*b/5 + 1/2)/(a^2/8 + pi^8*b^2/18 + pi^4*b/5 + 1/2) + 1` | 0.243683664062148   |
"""
from __future__ import division, print_function, unicode_literals, absolute_import
from io import open

from math import sin
import sys

params_file,output_file = sys.argv[1:]

# Simple and NOT robust reader
with open(params_file,'rt',encoding='utf8') as FF:
    FF.readline() # Skip first line
    x = float(FF.readline().split()[0])
    y = float(FF.readline().split()[0])
    z = float(FF.readline().split()[0])

a=7.0;b=0.1;
response = sin(x) + a*sin(y)**2 + b*z**4*sin(x)

with open(output_file,'wt',encoding='utf8') as FF:
    FF.write('{:0.15e} Ishigami'.format(response))

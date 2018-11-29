#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals

import numpy as np
import matplotlib.pylab as plt

# Load incremental and direct samples
Xinc = np.loadtxt('LHS_incremental.dat',comments='%',usecols=(0,1))
Xdir = np.loadtxt('LHS_direct.dat',comments='%',usecols=(0,1))

## Plot results
plt.close('all') 
fig,(axd,axi) = plt.subplots(1,2,num=1,figsize=(10,5))

# Plot contours
[x1,x2] = np.meshgrid(*[np.linspace(-2,2,40)]*2)
rosen = 100*(x2-x1**2)**2 + (1-x1)**2
for ax in [axd,axi]:
    ax.contour(x1,x2,rosen,50,colors=[[0.5]*3])

# Plot the direct
axd.plot(Xdir[:,0],Xdir[:,1],'o',label='80 samples')
axd.set(title='direct')

# Plot the incremental at 10,20,40,80 but reverse it so it shows plots
for n in [80,40,20,10]:
    axi.plot(Xinc[:n,0],Xinc[:n,1],'o',label='{} samples'.format(n))
axi.set(title='incremental 10,20,40,80')

for ax in [axd,axi]:
    ax.legend()
    ax.axis('square')
    ax.set(xlim=[-2,2],ylim=[-2,2],xlabel='x1',ylabel='x2')
fig.tight_layout()

fig.savefig('LHS_samples.png')

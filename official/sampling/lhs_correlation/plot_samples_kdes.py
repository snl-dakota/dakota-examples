#!/usr/bin/env python
"""
Plot the samples and the KDEs
"""

import numpy as np
import matplotlib.pylab as plt
from scipy.stats import gaussian_kde

import itertools

ndim = 6
X = np.loadtxt('samples.dat',usecols=np.arange(ndim),comments='%')

mins = X.min(axis=0)
maxs = X.max(axis=0)
ranges = maxs - mins
lower = mins - 0.05*ranges
upper = maxs + 0.05*ranges


labels = ['N1','N2','U2','U2','T1','T2']

# Get the i,j of each axis
IJs = np.array(list(itertools.combinations_with_replacement(range(ndim),2)))

# Get a grid of subplot numbers
subplot_grid = (np.reshape(np.arange(ndim**2),(ndim,ndim))+1).T

fig = plt.figure(num=1,figsize=(10.5,9.5))
fig.clear()
axes = np.empty((ndim,ndim),dtype=object) 
for IJi,(ii,jj) in enumerate(IJs):
    iax = subplot_grid[ii,jj]
    ax = fig.add_subplot(ndim,ndim,iax)
    axes[ii,jj] = ax

    
    if ii == jj:
        KDE = gaussian_kde(X[:,ii])
        xx = np.linspace(lower[ii],upper[ii],1000)
        
        # Get the PDF and scale it to be in [lower upper]
        # since we will reuse this range
        FF = KDE(xx)
        FF = (FF-FF.min())/(FF.max()-FF.min())
        FF = 0.95*(upper[ii]-lower[ii])*FF + lower[ii]
        ax.plot(xx,FF,'-k')
    else:
        nn = 30
        x,y = np.meshgrid(np.linspace(lower[ii],upper[ii],30),
                          np.linspace(lower[jj],upper[jj],30))
        positions = np.vstack([x.ravel(), y.ravel()])
        KDE = gaussian_kde(X[:,[ii,jj]].T)
        z = np.reshape(KDE(positions).T, x.shape)
        
        ax.contourf(x,y,z,15,cmap=plt.cm.Greys)
        ax.contour(x,y,z,15,linewidths=0.5,colors='k')

    ax.set_xlim([lower[ii],upper[ii]])
    ax.set_xticklabels([])
    ax.set_ylim([lower[jj],upper[jj]])
    ax.set_yticklabels([])

    # Handle the borders
    if jj == ndim-1: #X
        ax.set_xlabel(labels[ii])
        ax.set_xticklabels(ax.get_xticks())
    else:
        ax.set_xticks([])
        
    if ii == 0:   #Y
        ax.set_ylabel(labels[jj])
        ax.set_yticklabels(ax.get_yticks())
    else:
        ax.set_yticks([])

fig.subplots_adjust(wspace=0.1,hspace=0.1)

corr = np.corrcoef(X.T).tolist()
corr = [ ['{:0.3f}'.format(c) for c in row] for row in corr]
for ii,jj in itertools.combinations(range(ndim),2):
    corr[ii][jj] = ''

tab_scale = 1.5
axt = fig.add_subplot(ndim,ndim,subplot_grid[-2,1])
tab = axt.table(cellText=corr,loc='center',rowLabels=labels,colLabels=labels)
tab.set_fontsize(12)
tab.scale(tab_scale,tab_scale)
axt.axis('off')

fig.savefig('joint_kde_plot.png')
plt.show()

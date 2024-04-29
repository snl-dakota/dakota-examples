#  _______________________________________________________________________
#
#  Dakota: Explore and predict with confidence.
#  Copyright 2014-2024
#  National Technology & Engineering Solutions of Sandia, LLC (NTESS).
#  This software is distributed under the GNU Lesser General Public License.
#  For more information, see the README file in the top Dakota directory.
#  _______________________________________________________________________

import numpy as np

use_list_return_type = True

def textbook_numpy(params):

    num_fns = params["functions"]
    x = params["cv"]
    ASV = params["asv"]

    #print("ASV = ", ASV)

    retval = {}

    if (ASV[0] & 1): # **** f:
        fn = sum([(val - 1.)**4 for val in x])
        retval["fns"] = np.array([fn])

    if (ASV[0] & 2): # **** df/dx:
        g = [4. * (val - 1.)**3 for val in x]
        retval["fnGrads"] = np.array([np.array(g)])

    if (ASV[0] & 4): # **** d^2f/dx^2:
        h = np.diag([12. * (val - 1.)**2 for val in x])
        retval["fnHessians"] = np.array([h])

    if num_fns == 1:
        return retval


    # We have nonlinear constraints to provide
    if num_fns != 3:
        raise("textbook problem supports exactly 2 nonlinear inequality constraints.")

    if (ASV[1] & 1): # **** first nonlinear constraint objective:
        retval['fns'] = np.append(retval['fns'], (x[0]*x[0] - x[1]/2.0))

    if (ASV[1] & 2): # **** d/dx of first nonlinear constraint objective:
        g = [ 2.0*x[0], -0.5 ]
        for i in range(len(x)-2):
            g.append(0.0)
        retval['fnGrads'] = np.append(retval['fnGrads'], np.array([np.array(g)]), axis=0)

    if (ASV[1] & 4): # **** d2/dx2 of first nonlinear constraint objective:
        h = np.zeros_like(retval['fnHessians'][0])
        h[0,0] = 2.0
        retval['fnHessians'] = np.append(retval['fnHessians'], [h], axis=0)


    if (ASV[2] & 1): # **** second nonlinear constraint objective:
        retval['fns'] = np.append(retval['fns'], (x[1]*x[1] - x[0]/2.0))

    if (ASV[2] & 2): # **** d/dx of second nonlinear constraint objective:
        g = [ -0.5, 2.0*x[1] ]
        for i in range(len(x)-2):
            g.append(0.0)
        retval['fnGrads'] = np.append(retval['fnGrads'], np.array([np.array(g)]), axis=0)

    if (ASV[2] & 4): # **** d2/dx2 of second nonlinear constraint objective:
        h = np.zeros_like(retval['fnHessians'][0])
        h[1,1] = 2.0
        retval['fnHessians'] = np.append(retval['fnHessians'], [h], axis=0)

    return retval



def textbook_list(params):

    num_fns = params['functions']
    x = params['cv']
    ASV = params['asv']

    #print("ASV = ",ASV)
    #print("num_fns = ",num_fns)
    #print("x = ",x)

    retval = {}

    if (ASV[0] & 1): # **** f:
        fn = 0.0
        for val in x:
            fn += pow(val - 1.0, 4)
        retval['fns'] = [fn]

    if (ASV[0] & 2): # **** df/dx:
        g = []
        for val in x:
            g.append(4.0 * pow(val - 1.0, 3))
        retval['fnGrads'] = [g]

    if (ASV[0] & 4): # **** d^2f/dx^2:
        h = []
        for i in range(len(x)):
            h.append( [0*_ for _ in x] )
        for i, val in enumerate(x):
            h[i][i] = 12.0 * pow(val - 1.0, 2)
        retval['fnHessians'] = [h]

    if num_fns == 1:
        return retval

    # We have nonlinear constraints to provide
    if num_fns != 3:
        raise("textbook problem supports exactly 2 nonlinear inequality constraints.")

    if (ASV[1] & 1): # **** first nonlinear constraint objective:
        retval['fns'].append(x[0]*x[0] - x[1]/2.0)

    if (ASV[1] & 2): # **** d/dx of first nonlinear constraint objective:
        g = [ 2.0*x[0], -0.5 ]
        for i in range(len(x)-2):
            g.append(0.0)
        retval['fnGrads'].append(g)

    if (ASV[1] & 4): # **** d2/dx2 of first nonlinear constraint objective:
        h = []
        for i, val in enumerate(x):
            row = [ 0.0*_ for _ in x ]
            h.append(row)
        h[0][0] = 2.0
        retval['fnHessians'].append(h)


    if (ASV[2] & 1): # **** second nonlinear constraint objective:
        retval['fns'].append(x[1]*x[1] - x[0]/2.0)

    if (ASV[2] & 2): # **** d/dx of second nonlinear constraint objective:
        g = [ -0.5, 2.0*x[1] ]
        for i in range(len(x)-2):
            g.append(0.0)
        retval['fnGrads'].append(g)

    if (ASV[2] & 4): # **** d2/dx2 of second nonlinear constraint objective:
        h = []
        for i, val in enumerate(x):
            row = [ 0.0*_ for _ in x ]
            h.append(row)
        h[1][1] = 2.0
        retval['fnHessians'].append(h)


    return retval



def textbook(params):

    if use_list_return_type:
        return textbook_list(params)
    else:
        return textbook_numpy(params)

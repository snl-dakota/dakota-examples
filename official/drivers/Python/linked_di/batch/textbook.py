#  _______________________________________________________________________
#
#  Dakota: Explore and predict with confidence.
#  Copyright 2014-2024
#  National Technology & Engineering Solutions of Sandia, LLC (NTESS).
#  This software is distributed under the GNU Lesser General Public License.
#  For more information, see the README file in the top Dakota directory.
#  _______________________________________________________________________


def textbook_list(params):

    num_fns = params['functions']
    x = params['cv']
    ASV = params['asv']

    #print("ASV = ",ASV)
    #print("num_fns = ",num_fns)
    #print("x = ",x)

    # We have one objective fn and two nonlinear constraints to provide
    if num_fns != 3 or len(ASV) != 3:
        raise("textbook problem supports 1 obj fn and 2 nonlinear inequality constraints.")

    fns = []
    grads = []
    hessians = []

    if (ASV[0] & 1): # **** f:
        fn = 0.0
        for val in x:
            fn += pow(val - 1.0, 4)
        fns.append(fn)

    if (ASV[0] & 2): # **** df/dx:
        g = []
        for val in x:
            g.append(4.0 * pow(val - 1.0, 3))
        grads.append(g)

    if (ASV[0] & 4): # **** d^2f/dx^2:
        h = []
        for i in range(len(x)):
            h.append( [0*_ for _ in x] )
        for i, val in enumerate(x):
            h[i][i] = 12.0 * pow(val - 1.0, 2)
        hessians.append(h)


    if (ASV[1] & 1): # **** first nonlinear constraint objective:
        fns.append(x[0]*x[0] - x[1]/2.0)

    if (ASV[1] & 2): # **** d/dx of first nonlinear constraint objective:
        g = [ 2.0*x[0], -0.5 ]
        for i in range(len(x)-2):
            g.append(0.0)
        grads.append(g)

    if (ASV[1] & 4): # **** d2/dx2 of first nonlinear constraint objective:
        h = []
        for i, val in enumerate(x):
            row = [ 0.0*_ for _ in x ]
            h.append(row)
        h[0][0] = 2.0
        hessians.append(h)


    if (ASV[2] & 1): # **** second nonlinear constraint objective:
        fns.append(x[1]*x[1] - x[0]/2.0)

    if (ASV[2] & 2): # **** d/dx of second nonlinear constraint objective:
        g = [ -0.5, 2.0*x[1] ]
        for i in range(len(x)-2):
            g.append(0.0)
        grads.append(g)

    if (ASV[2] & 4): # **** d2/dx2 of second nonlinear constraint objective:
        h = []
        for i, val in enumerate(x):
            row = [ 0.0*_ for _ in x ]
            h.append(row)
        h[1][1] = 2.0
        hessians.append(h)

    return fns, grads, hessians



def textbook(params):

    return textbook_list(params)

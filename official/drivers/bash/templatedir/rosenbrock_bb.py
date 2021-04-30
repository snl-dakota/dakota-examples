#!/usr/bin/env python3


def rosenbrock_list(**kwargs):

    num_fns = kwargs['functions']

    x = kwargs['cv']
    ASV = kwargs['asv']

    f0 = x[1]-x[0]*x[0]
    f1 = 1-x[0]

    retval = dict([])

    if (ASV[0] & 1): # **** f:
        f = [100*f0*f0+f1*f1]
        retval['fns'] = f

    if (ASV[0] & 2): # **** df/dx:
        g = [ [-400*f0*x[0] - 2*f1, 200*f0] ]
        retval['fnGrads'] = g

    if (ASV[0] & 4): # **** d^2f/dx^2:
        fx = x[1]-3*x[0]*x[0]

        h = [
              [ [-400*fx + 2, -400*x[0]],
                [-400*x[0],    200     ] ]
            ]
        retval['fnHessians'] = h

    return retval


def get_varvals():
    with open("ros.in", "r") as f:
        ros_in = f.readlines()
    x1 = None
    x2 = None
    for line in ros_in:
        if "variable 1" in line:
            x1 = float(line.split()[-1])
        if "variable 2" in line:
            x2 = float(line.split()[-1])
    return x1, x2


def pack_inputs(x1, x2):
    d = {
        "functions": 1,
        "cv": [x1, x2],
        "asv": [3],
    }
    return d


def generate_output(x1, x2, f, gradient):
    s = """
 Beginning execution of model: Rosenbrock black box
 Set up complete.
 Reading nodes.
 Reading elements.
 Reading materials.
 Checking connectivity...OK
 *****************************************************

 Input value for x1 = {x1:23.16e}
 Input value for x2 = {x2:23.16e}

 Computing solution...Done
 *****************************************************
 Function value =  {f:23.16e}
 Function gradient = [ {f1:23.16e}  {f2:23.16e} ]

"""
    return s.format(x1=x1, x2=x2, f=f, f1=gradient[0], f2=gradient[1])


def write_output(s):
    with open("ros.out", "w") as f:
        f.write(s)


def main():
    x1, x2 = get_varvals()
    d = pack_inputs(x1, x2)
    r = rosenbrock_list(**d)
    s = generate_output(x1, x2, r["fns"][0], r["fnGrads"][0])
    write_output(s)


if __name__ == "__main__":
    main()

import numpy as np

def unpack_inputs(params):
    x = params["cv"]
    ASV = params["asv"]
    return x, ASV

def borehole(**kwargs):
    """
    input space: 8D
    r_w ~ N(0.1, 0.0161812)
    r ~ LogNormal(7.71, 1.0056)
    T_u ~ U[63070, 115600]
    H_u ~ U[990, 1110]
    T_l ~ U[63.1, 116]
    H_l ~ U[700, 820]
    L ~ U[1120, 1680]
    K_w ~ U[9855, 12045]
    """

    x, ASV = unpack_inputs(kwargs)
    retval = {}

    r_w = x[0]
    r = x[1]
    T_u = x[2]
    H_u = x[3]
    T_l = x[4]
    H_l = x[5]
    L = x[6]
    K_w = x[7]

    if (ASV[0] & 1):
        logratio = np.log(r / r_w)
        numer =  2. * np.pi * T_u * (H_u - H_l)
        denom = logratio * (1. + 2. * L * T_u / (logratio * r_w**2 * K_w) \
              + T_u / T_l)
        f = numer / denom
        retval["fns"] = np.array([f])
    return retval

def OTL(**kwargs):
    """
    input space: 6D
    R_b1 ~ U[50, 150]
    R_b2 ~ U[25, 70]
    R_f ~ U[0.5, 3]
    R_c1 ~ U[1.2, 2.5]
    R_c2 ~ U[0.25, 1.2]
    beta ~ U[50, 300]
    """

    x, ASV = unpack_inputs(kwargs)
    retval = {}

    R_b1 = x[0]
    R_b2 = x[1]
    R_f = x[2]
    R_c1 = x[3]
    R_c2 = x[4]
    beta = x[5]

    if (ASV[0] & 1):
        V_b1 = 12. * R_b2 / (R_b1 + R_b2)
        f = (V_b1 + 0.74) * beta * (R_c2 + 9.) / (beta * (R_c2 + 9.) + R_f) \
          + 11.35 * R_f / (beta * (R_c2 + 9.) + R_f) \
          + 0.74 * R_f * beta * (R_c2 + 9.) \
          / ((beta * (R_c2 + 9.) + R_f) * R_c1)
        retval["fns"] = np.array([f])
    return retval

def Dette_and_Peplyshev(**kwargs):
    """
    input space: [0, 1]**8
    """

    x, ASV = unpack_inputs(kwargs)
    retval = {}

    if (ASV[0] & 1):
        f = 4. * (x[0] - 2. + 8.*x[1] - 8. * x[1]**2)**2 + (3. - 4.*x[1])**2 \
            + 16. * np.sqrt(x[2] + 1.) * (2. * x[2] - 1.)**2
        for k in range(3, 8):
            f += (k + 1.) * np.log(1. + np.sum(x[2:k + 1]))

        retval["fns"] = np.array([f])
    return retval

def Morris(kwargs):
    """
    input space: [0, 1]**20
    """

    x, ASV = unpack_inputs(kwargs)
    retval = {}

    N = 20

    beta_1D = np.zeros(N)
    beta_2D = np.zeros((N, N))
    beta_3D = np.zeros((N, N, N))

    beta_1D[:10] = 20.
    beta_2D[:6, :6] = -15.
    beta_3D[:5, :5, :5] = -10.

    w = 2. * (x - 0.5)
    idx = list(np.array([3, 5, 7]) - 1) # subtract 1 for zero-based indexing
    w[idx] = 2.* (1.1 * x[idx] / (x[idx] + 0.1) - 0.5)

    for i in range(5, N):
        beta_1D[i] = (-1.)**(i + 1)

    for i in range(6, N):
        for j in range(6, N):
            beta_2D[i, j] = (-1.)**(i + 1 + j + 1)

    if (ASV[0] & 1):
        f = beta_1D.dot(w) + 5. * np.sum(w[:4])
        for j in range(N):
            for i in range(j):
                f += beta_2D[i, j] * w[i] * w[j]
        for k in range(N):
            for j in range(k):
                for i in range(j):
                    f += beta_3D[i, j, k] * w[i] * w[j] * w[k]
        retval["fns"] = np.array([f])

    return retval

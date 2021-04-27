import numpy as np
import surrogates as daksurr
# NOTE: This is a test that should only be run by CTest in the build tree.
# Importing surrogates this way works only in the context of running
# tests in the build tree. In an ordinary dakota install, dakota.surrogates
# should be imported.

# Set up
def tf(x):
    y = x**2 - x * np.log(x + 1) + (x - 0.5) * np.sin(2 * np.pi * x)
    return y

xs = np.array([0.05536604, 0.28730518, 0.30391231, 
               0.40768703,0.45035059, 0.52639952, 
               0.78853488]).reshape(-1, 1)
ys = tf(xs)
ps = np.linspace(0, 1, 201).reshape(-1, 1)


# Polynomiial surrogate
poly = daksurr.PolynomialRegression(xs, ys, {"max degree" : 2, "scaler type" : "none", "reduced basis" : False})
poly.print_options() # no output in jupyter, but will print to console in a terminal
poly_value = poly.value(ps)
poly_grad = poly.gradient(ps)
poly_hessian = [poly.hessian(p)[0, 0] for p in ps]

# GP


nugget_opts = {"estimate nugget" : True}
trend_opts = {"estimate trend" : True, "Options" : {"max degree" : 2}}
config_opts = {"kernel type" : "squared exponential", "scaler name" : "standardization", "Nugget" : nugget_opts,
               "num restarts" : 15, "Trend" : trend_opts}

gp = daksurr.GaussianProcess(xs, ys, config_opts)
gp.print_options() # no output in jupyter, but will print to console in a terminal
gp_value = gp.value(ps)
gp_variance = gp.variance(ps)
gp_grad = gp.gradient(ps)
gp_hessian = [gp.hessian(p)[0, 0] for p in ps]

# Load and save


# save surrogates
daksurr.save(poly, "poly.txt", False) # text archive
daksurr.save(gp, "gp.bin", True) # binary archive



# load serialized surrogates and compare values
poly_loaded = daksurr.load("poly.txt", False)
gp_loaded = daksurr.load("gp.bin", True)

assert(np.allclose(poly_loaded.value(ps), poly_value))
assert(np.allclose(gp_loaded.value(ps), gp_value))



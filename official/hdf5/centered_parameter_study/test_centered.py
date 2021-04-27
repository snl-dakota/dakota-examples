import h5py


# Verify existence of a few locations that are used in the accompanying notebook
with h5py.File("dakota_results.h5","r") as h:
    results = h["/methods/NO_METHOD_ID/results/execution:1/"]
    results["parameter_sets/responses"].dims[1][0]
    results["parameter_sets/responses"][:,0]
    results["variable_slices"].items()


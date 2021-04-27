import h5py


with h5py.File("dakota_results.h5","r") as h:
    results = h["/methods/my_sampling/results/execution:1"]
    inc_group = results["increment:1"]
    inc_group.attrs["samples"]
    inc_group["moment_confidence_intervals/f"][0,0] 
    inc_group["moments/f"][0]
    inc_group["moment_confidence_intervals/f"][1,0] 
    inc_group["moment_confidence_intervals/f"][0,1]
    inc_group["moments/f"][1]
    inc_group["moment_confidence_intervals/f"][1,1] 

# Summary

Perform Bayesian calibration using a multilevel polynomial chaos expansion emulator

# Description

Understanding and characterizing wake steering and wake impingement in an uncertain environment is essential for the design of efficient wind power plants. High-fidelity simulations can achieve sufficient accuracy in a deterministic context, but, whenever a many-queries workflow, like optimization and/or uncertainty quantification, needs to be performed, they quickly become impractical due to their often prohibitive computational cost. The exclusive use of low fidelity models in their place is often not viable since many low fidelity models miss important physical mechanisms, which could result in a non-negligible bias. Calibration of lower-fidelity models is another source of uncertainty that must be accounted for.

In the study contained in this example, Bayesian calibration was used to establish a joint posterior distribution for six input parameters to WindSE, a "medium fidelity", steady-state RANS-based solver. Reference data were produced by averaging in time an high fidelity flow field obtained using SNL Nalu-Wind, which is a Large Eddy Simulation (LES) solver.

The physical system that was modeled was a single wind turbine and the surrounding volume. The wind velocity components, in a 2D vertical plane five diameters downstream of the turbine, were the quantities of interest. Nalu-Wind, the high-fidelity simulator, was used to generate the reference data, a total of 31,396 time-averaged velocity components at points in the plane. The six inputs to WindSE include several physical and turbine parameters, and were assigned uniform priors.

Although WindSE is much less costly to run than Nalu-Wind, it still would have been prohibitively expensive to run the potentially millions of simulations needed by Markov Chain Monte Carlo (MCMC) sampling to achieve a well-converged posterior chain. An emulator- or surrogate-based approach therefore was adopted. Due to the ready availability of a hierarchy of model levels--coarse, medium, and fine meshes--the emulator chosen was a multilevel polynomial chaos expansion (MLPCE). MLPCE surrogate models are one type of many that Dakota provides that can exploit hierarchies in simulation cost and accuracy to greatly reduce the overall cost of a study.

Files in the example include a presentation that compares approaches to selecting and constructing a multifidelity surrogate on a toy problem and results from the WindSE calibration. The example also provides the Dakota study that was used to perform the calibration, including the input, scripts, and data files.

# Contents

* `Dakota_wind_work.pdf`: Slides describing the problem, experiments, and study results
* `study/`: Dakota study folder
  * `single_turbine.yaml`: WindSE input file for the nominal parameterization
  * `wind_inference.in`: Dakota input
  * `upper_half_slice_nalu_all.dat`: Nalu reference data (used by Dakota to compute residuals) 
  * `scripts/`: Driver and other scripts for WindSE. These are provided for illustration and will not run without WindSE.
    * foo
    * bar
    * baz

# Summary

Understand the basic theory that underlies Dakota's multilevel and multifidelity sampling methods and learn how to set up and interpret Dakota studies that use them

# Description

This series of tutorials describes how to configure some of the multilevel/multifidelity sampling algorithms currently implemented in Dakota. We focus on basic capabilities and differences between these algorithms. For additional specifications, the interested reader should refer to the Dakota manuals.

The tutorial begins in this README by describing the test problem that will be used throughout. Then, four approaches to sampling are explored. The first is simple Monte Carlo. It introduces the concepts of an *estimator* and *estimator variance*. The next three approaches, Control Variate Monte Carlo (CVMC), Multilevel Monte Carlo (MLMC), and Multilevel-Multifidelity Monte Carlo (MLMF), are ways of exploiting multiple model fidelities or levels to achieve better estimates of statistics at lower overall computational cost.

After completing the tutorial, the reader should understand the basic theory that underlies multilevel and multifidelity sampling approaches and how to configure Dakota to use them.

# Outline

1. [Test Problem Description](#test-problem-description). A description of the simple model that will be used throught the tutorial.
2. Sampling Approaches
    1. [Monte Carlo](./mc). Single-fidelity approach. A good understanding of Monte Carlo sample is essential before moving on to more advanced
       approaches;
    2. [Control Variate Monte Carlo](./cv). Multifidelity Monte Carlo is based on control variate and a single low-fidelity model;
    3. [Multilevel Monte Carlo](./mlmc). MLMC is an extension of MC via linear expansion of the expected value over a prescribed set of models;
    4. [Multilevel-Multifidelity Monte Carlo](./mlmf). MLMF is a combination of MLMC and CV MC as an expansion over a prescribed set of models,
       based on the first model form, for which a control variate, based on the second model form, is used to decrease the variance of the
       level-by-level, decomposition.

# Test Problem Description

In this chapter we define the test problem that we are going to use for
the tutorial. More details on this problem can be found in [\[1\]](#references).
We consider the PDE describing the temperature evolution $`u`$ in a rod
$`\Omega=[0,1]`$ with uncertain initial condition $`u_0`$ and diffusivity
$`\alpha > 0`$

```math
    \frac{ \partial u }{ \partial t} - \alpha \frac{ \partial^2 u }{ \partial x^2 } = 0, \\[2mm]
    u(x,\xi,0) = u_0(x,\xi) \\[2mm]
    u(x,\xi,t)_{\partial \Omega} = 0.
 ```

For this problem we can write the initial condition as a sum of
contributions that depends explicitly on the physical coordinate $`x`$ or
the stochastic coordinate $`\xi`$

```math
     u_0(x,\xi) = \mathcal{G}_1(\xi) \mathcal{F}_1(x) + \mathcal{G}_2(\xi) \mathcal{F}_2(x) \\[2mm]
    \mathcal{F}_1(x) = \sin(\pi x) \\[2mm]


    \mathcal{F}_2(x) = \sin(2 \pi x) + \sin(3 \pi x) + 50 \left( \sin(9 \pi x) + \sin(21 \pi x) \right) \\[2mm]

    \mathcal{G}_1(\xi) = 50 \frac{ |4 \xi_5 - 2| + a_i }{ 1 + a_i }\, \frac{ |4 \xi_6 -2| + a_i }{ 1 + a_i }\,  \frac{ |4 \xi_7 -2| + a_i }{ 1 + a_i },
      \quad \mathrm{with} \quad a_i = -1/2\\[2mm]

    \mathcal{G}_2(\xi) = \frac{7}{2} \left( \sin(\xi_1) + 7 \sin^2(\xi_2) + \frac{1}{10} \xi^4_3 \sin(\xi_1) \right).  \\
```

Two comments are in order here: the problem has a total of 7
(independent) uncertain parameters $`\xi_i \sim \mathcal{U}(-1,1)`$; there
is a prescribed and discrete spectral content in the spatial response
that we can use to define a model form.

The problem can be solved in closed form for the spatial average
temperature on the rod, $`Q`$, after a finite time $`T`$. The numerical
solution of the problem can be obtained by resorting to a Fourier
expansion where each coefficient is obtained via a spectral projection
between the initial solution and the selected trigonometric basis.

We are interested in demonstrating UQ approaches that uses both a
multilevel setting and a multifidelity setting, so we can define the
model forms, based on the spectral content that we use to resolve the
spatial expansion coefficients. In particular, we define the
high-fidelity (HF) model as the one including the full spectral content
of $`u_0`$ (determined by the highest spatial mode in $`\mathcal{F}_2`$),
whereas the low-fidelity (LF) model only uses the first 3 spatial modes,
which corresponds to including only part of the $`\mathcal{F_2}`$
solution. Due to the difference in the spectral content, for each model
we can rely on a different spatial resolution (controlled by equally
spaced point $`N_x`$) to perform the numerical quadrature via a
trapezoidal rule. The properties of the models are reported in the following
table for four possible levels ($`\ell = 0, \dots, 3`$)
per model fidelity.

|Level       | **LF** ($`N_x = 3`$) | **HF** ($`N_x = 21`$) |
|------------|----------------------|-----------------------|
| $`\ell=0`$ | $`5`$  | $`30`$ |
| $`\ell=1`$ | $`15`$ | $`60`$ |
| $`\ell=2`$ | $`30`$ | $`100`$ |
| $`\ell=3`$ | $`60`$ | $`200`$ |


We also note, as demonstrated in [\[1\]](#references), that the two model form do
not converge to the same statistics of the QoI, therefore it is
legitimate to assume them as distinct model form, rather than ’levels’,
as it will be more evident later on. Finally, we note that this problem is already available in 
Dakota and it can be invoked via a direct driver (more details will be provided later). 

# References

1. G. Geraci, M.S. Eldred & G. Iaccarino, A multifidelity control variate
approach for the multilevel Monte Carlo technique. *Center for
Turbulence Research, Annual Research Briefs 2015*, pp. 169–181, 2015.

----
* Return to the [Outline](#outline)
* Continue to the [next section](./mc) of the tutorial

# Sensitivities with Surrogates

In these examples, we demonstrate how you can use a surrogate model to compute the sensitivities.

There two strategies: 

1. PCE on a surrogate 
2. sampling on a surrogate

And there are two surrogate building strategies:

1. Call model a small number of times and then create the surrogate
2. Use existing data to create the surrogate

## PCEs on Surrogates

Building a PCE on a surrogate may seem like an odd choice of methods since the PCE is, itself, a surrogate (of sorts). However, such an approach is useful since the `variance_based_decomp` that comes from a PCE method are analogous to directly computing the integrals. In addition, the PCE method returns much more information about parameter interaction

## Differences between PCE and Sampling methods

The only difference for both building strategies between the PCE methods and the sampling methods are the `method` block. For example, in the "existing data" methods, the sampling method has the following

```dakota
method
	sampling
	  samples = 10000 
	  seed = 54321
	  sample_type lhs
	variance_based_decomp
```

while the PCE methods look as follows (with some options in the comments):

```dakota
method
	polynomial_chaos
	    askey
	    ############# This works for low-dimensions
	    #quadrature_order = 15
     	#non_nested
     	
     	############ This may be useful for either higher dimensions 
     	#            or if higher order PCEs are desired
     	sparse_grid_level = 8
     	nested         
     	
     	variance_based_decomp
```

## Existing Data vs Calling the Model

Both methods are perfectly acceptable to perform global sensitivity. The key advantages of using existing data are:

* Much simpler Dakota input deck
* Easily reuse data from previous study
* No need to `interface` a model
* No risk of lost data

In this example, both the existing data and the model calls were generated from the same LHS seed. As such, they yield identical results:

## Results

As noted above, the exisisting-data method and the method that calls the model use the same LHS settings so their results are identical:

PCE:
```
Ishigami Sobol' indices:
                                  Main             Total
                      2.0346652757e-01  4.4301290034e-01 x
                      3.6065909618e-01  6.6024513704e-01 y
                      2.3321485551e-02  4.1795293820e-01 z
                           Interaction
                      1.7921438046e-02 x y
                      1.1296684984e-01 x z
                      1.7300651793e-01 y z
                      1.0865808488e-01 x y z
```

Sampling

```
Ishigami Sobol' indices:
                                  Main             Total
                          1.985522e-01      4.446065e-01 x
                          3.313369e-01      6.521479e-01 y
                          1.444564e-02      4.183909e-01 z
```

And, just to note: the analytical:

```
                                  Main             Total
                      3.1390519115e-01  5.5758885521e-01 x
                      4.4241114480e-01  4.4241114480e-01 y
                      0.0000000000e-00  2.4368366406e-01 z
                           Interaction
                      0.0000000000e-00 x y
                      2.4377949556e-01 x z
                      0.0000000000e-00 y z
                      0.0000000000e-00 x y z
```



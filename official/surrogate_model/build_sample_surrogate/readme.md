# Build and Sample (LHS) a Surrogate Model.

There are two nearly identical examples. The first builds and samples a surrogate in a single input deck. The second breaks the processes into two parts. The former is more compact while the latter can be easily adapted for building a surrogate on existing data.

In both examples we will build a surrogate of the Rosenbrock function (even though it can be evaluated easily)

## Example 1 Notes

At the top of `Example1.in` is the block that starts

```dakota
environment
	top_method_pointer = 'method_surrogate' # VERY IMPORTANT
```

This is imperative to tell Dakota which method to use first. Then each block is given an `id_[method,model,...]` and are also provided pointers where appropriate. For example, in the `model_real` model block is `interface_pointer = 'interface_real'`

## Example 2 Notes

The components of example 2 are very similar to the respective parts of example 1. IDs and pointers are removed and the original 40 point sample from the "real" model is saved.

In part 1, we output the model values. Note that we also include `output_precision = 16`. While this isn't necessary, it is good practice since we will be immediately processing that data in another dakota file.

In part 2, the `model surrogate` block is identical except with the addition of 

## Surrogate model block

Both examples share the same form of the `model` block for the surrogate. Dakota provides a common interface to all available surrogates. In the `model` block is the line:

```dakota
	surrogate global    
        # polynomial quadratic		
        # neural_network		
        gaussian_process surfpack trend quadratic
        # mars
```

where a few surrogate types are listed but commented out. These can be readily changed to use different surrogate forms

The `metrics` tell Dakota to compute simple metrics of the quality. Additionally, are `press` for Leave-one-out cross validation and `cross_valiation` to perform k-fold (default 10) cross validation. These are commented out because they are rather expensive to compute.


## Cleanup

Run 

    $ rm LHS_[123456789].out LHS_distributions.out LHS_samples.out  
    $ rm fort.*
    $ rm dakota.rst # if you do not need it.
    
to clean up.

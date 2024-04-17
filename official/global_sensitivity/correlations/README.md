# Summary

This page provides eight examples computing four correlations:
- Pearson (denoted 'simple' in the dakota run outputs)
- partial Pearson (denoted 'partial' in the dakota run outputs)
- Spearman (denoted 'simple rank' in the dakota run outputs)
- partial Spearman (denoted 'partial rank' in the dakota run outputs)

### The meaning of the four correlations

All four correlations assume values in the range [-1,1].

For the purpose of the definitions below, assume that we have $n$ scalar input variables $x_i,~i=1,\ldots,n$, and a scalar output variable $y$.
The definitions below can be easily extended for cases where one has more than one output variable.

The Pearson correlation measures the strength and direction of the linear relationship between two variables (input-input, or input-output, or output-output).
For instance, suppose we have $N\text{ samples }(w_j,z_j),~j=1,\ldots,N$, of the pair of variables $w\text{ and }z$ (in our case, both $w\text{ and }z$ can be any of the variables $y,~x_1,\ldots,x_n$).
The Pearson correlation between $w\text{ and }z$ is given by

$\rho(w,z) = \frac{\text{cov}(w,z)}{\sqrt{\text{var}(w)\cdot \text{var}(z)}} = \frac { N\cdot\left(\sum_{j=1}^{N}w_j\cdot z_j\right) - \left(\sum_{j=1}^{N}w_j\right) \cdot \left(\sum_{j=1}^{N}z_j\right) } { \sqrt{ N\cdot\left(\sum_{j=1}^{N}w_j^2\right) - \left(\sum_{j=1}^{N}w_j\right)^2 } \cdot \sqrt{ N\cdot\left(\sum_{j=1}^{N}z_j^2\right) - \left(\sum_{j=1}^{N}z_j\right)^2 } }$.

The partial Pearson correlation measures the strength and direction of the linear relationship between an input variable $x_i$ and an output variable $y$ *after the linear effect of the remaining parameters* $x_1,~x_2,\ldots,~x_{i-1},~x_{i+1},\ldots,~x_n$, *have been taken out from both* $y\text{ and }x_i$.
For instance, In order to compute it for variables $x_i\text{ and }y$, one needs to go through the following three steps:
- compute linear regression models of both $y\text{ and }x_i$:
  - $\tilde{y_i}=a_0+a_1\cdot x_1+a_2\cdot x_2+\ldots+a_{i-1}\cdot x_{i-1}+a_{i+1}\cdot x_{i+1}+\ldots+a_n\cdot x_n$,
  - $\tilde{x_i}=b_0+b_1\cdot x_1+b_2\cdot x_2+\ldots+b_{i-1}\cdot x_{i-1}+b_{i+1}\cdot x_{i+1}+\ldots+b_n\cdot x_n$;
- compute the residuals $r_{y,i}=y-\tilde{y_i}\text{ and }r_{x,i}=x_i-\tilde{x_i}$;
- compute the Pearson correlation between $r_{y,i}\text{ and }r_{x,i}$.

The Spearman correlation measures the strength and direction of the monotonic relationship between two variables (input-input, or input-output, or output-output).
In order to compute it, one has to replace the values in each sample $(x_{1,j},\ldots,x_{n,j},y_j),~j=1,\ldots,N$, by the respective ranks in the corresponding sets of values.
Then one just computes the Pearson correlation for the rank samples.

The partial Spearman correlation measures the strength and direction of the monotonic relationship between an input variable and an output variable *after the linear effect of the remaining ranks of* $x_1,~x_2,\ldots,~x_{i-1},~x_{i+1},\ldots,~x_n$, *have been taken out from the ranks of both* $y\text{ and }x_i$.
In order to compute it, one has to replace the values in each sample $(x_{1,j},\ldots,x_{n,j},y_j),~j=1,\ldots,N$, by the respective ranks in the corresponding sets of values.
Then one just computes the partial Pearson correlation for the rank samples.

### The eight examples

In all eight examples there is an output variable $y$ as a function of four input variables $x_1,~x_2,~x_3,\text{ and }x_4$.
All four input variables are uniform random variables over $[0,1]$.
In cases 7 and 8, the variable $\epsilon$ is an uniform random variable over $[-0.2, 0.2]$.

The eight example cases are as follows:
- Case 1: $y = 10 \cdot x_1 + x_2 + 0.1 \cdot x_3 + 0.01 \cdot x_4$, with uncorrelated input variables
- Case 2: $y = 10 \cdot x_1 + x_2 + 0.1 \cdot x_3 + 0.01 \cdot x_4,\text{ with corr}(x_1,x_4)=0.8$
- Case 3: $y = 10 \cdot x_1 + x_2^2 + x_3^3 + x_4^4$, with uncorrelated input variables
- Case 4: $y = 10 \cdot x_1 + x_2^2 + x_3^3 + x_4^4,\text{ with corr}(x_1,x_4)=0.8$
- Case 5: $y = x_1 + x_2^2 + x_3^3 + x_4^4$, with uncorrelated input variables
- Case 6: $y = x_1 + x_2^2 + x_3^3 + x_4^4,\text{ with corr}(x_1,x_4)=0.8$
- Case 7: $y = 10 \cdot x_1 + x_2 + 0.1 \cdot x_3 + 0.01 \cdot x_4 + \epsilon$, with uncorrelated input variables
- Case 8: $y = 10 \cdot x_1 + x_2 + 0.1 \cdot x_3 + 0.01 \cdot x_4 + \epsilon,\text{ with corr}(x_1,x_4)=0.8$

Each of the eight cases demand two files, as follows:
- Case 1: [correlations1.in](./1/correlations1.in) and [driver1.py](./1/driver1.py)
- Case 2: [correlations2.in](./2/correlations2.in) and [driver2.py](./2/driver2.py)
- Case 3: [correlations3.in](./3/correlations3.in) and [driver3.py](./3/driver3.py)
- Case 4: [correlations4.in](./4/correlations4.in) and [driver4.py](./4/driver4.py)
- Case 5: [correlations5.in](./5/correlations5.in) and [driver5.py](./5/driver5.py)
- Case 6: [correlations6.in](./6/correlations6.in) and [driver6.py](./6/driver6.py)
- Case 7: [correlations7.in](./7/correlations7.in) and [driver7.py](./7/driver7.py)
- Case 8: [correlations8.in](./8/correlations8.in) and [driver8.py](./8/driver8.py)

### Running Dakota

In order to run any of the eight cases, just type

```
dakota -i <dakota case input file>.in <ENTER>
```

### Motivations for the eight example cases

The eight examples can be seen as four pairs of examples:
- first pair (cases 1 and 2): deals with the relation $y = 10 \cdot x_1 + x_2 + 0.1 \cdot x_3 + 0.01 \cdot x_4$, and serves as a reference which all other pairs will be compared against.
- second pair (cases 3 and 4): deals with the relation $y = 10 \cdot x_1 + x_2^2 + x_3^3 + x_4^4$, checking the impact of different functions of $x_2,~x_3,\text{ and }x_4$ on the computed correlations,
when compared to the results of the *first* pair of examples.
- third pair (cases 5 and 6): deals with the relation $y = x_1 + x_2^2 + x_3^3 + x_4^4$, checking the impact of a different scaling factor for $x_1$ on the computed correlations,
when compared to the results of the *second* pair of examples.
- fourth pair (cases 7 and 8): deals with the relation $y = 10 \cdot x_1 + x_2 + 0.1 \cdot x_3 + 0.01 \cdot x_4 + \epsilon$, checking the impact of a noise on the computed correlations,
when compared to the results of the *first* pair of examples.

Inside each pair of examples, the first example has uncorrelated input variables, while the second example has a correlation of 0.8 between variables $x_1\text{ and }x_4$. The aim of the second examples
in each pair is to check the impact of correlation among input variables on the computed correlations.

### Results of all eight example cases

Click [here](./results) to see the results and corresponding comments.

### Suggestions for extra example cases

The user may very easily experiment with different functions on $x_1,~x_2,~x_3,\text{ and }x_4$, other than
the simple power functions used above. For instance, one could try $e^{x},\text{ or sin}(x),\text{ or }1/(1+x)$.

Also, some of the input variables could have different distributions, or be still uniform but over
an interval other than $[0,1]$.

Another possibility is to vary the number of samples. Above we report results using 4,000 samples in all eight example cases.

One can also compute more than one output function in each example, e.g., $y\text{ and }g$, facilitating result comparisons.

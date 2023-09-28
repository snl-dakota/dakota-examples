### Generic comments for all output results of the eight example cases

In the sections below we list the outputs of all eight example cases, and give more specific comments for each of the four pairs of examples.

In all cases, the Pearson and Spearman correlations are presented as a matrix involving all input variables ($x_1,~x_2,~x_3,\text{ and }x_4$) and all output variables (just $y$ in this page).
Since the matrix is symmetric, only the lower portion is presented.
Moreover, one can see that the diagonal terms are always equal to 1.0.
One can also see that almost all computed correlations between $x_i\text{ and }x_j$ are smaller than $0.01,\text{ for }1 \leq i, j \leq 4,~i \neq j$.
The only exceptions are in cases 2, 4, 6, and 8, where the dakota input files specify a correlation of $0.8\text{ between }x_1\text{ and }x_4$.
Indeed, in all such cases the computed correlation between $x_1\text{ and }x_4$ is around 0.788, close to the limit value of 0.8 for an infinite amount of samples (instead of 'just' 4,000 samples).

Also in all cases, the partial Pearson and partial Spearman correlations are presented just for the relationship between $x_1\text{ and }y,\text{ between }x_2\text{ and }y,\text{ between }x_3\text{ and }y$, and between $x_4\text{ and }y$,
a presentation consistent with the definitions given above for both partial correlations.
 
### The output results for case 1 (4,000 samples): $y = 10 \cdot x_1 + x_2 + 0.1 \cdot x_3 + 0.01 \cdot x_4$

```
Simple Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.85428e-04  1.00000e+00 
          x3  4.22780e-03 -2.73130e-03  1.00000e+00 
          x4 -9.94643e-04  4.18049e-03  6.27778e-03  1.00000e+00 
           y  9.94990e-01  9.92893e-02  1.38907e-02  4.83734e-04  1.00000e+00 

Partial Correlation Matrix between input and output:
                        y 
          x1  1.00000e+00 
          x2  1.00000e+00 
          x3  1.00000e+00 
          x4  1.00000e+00 

Simple Rank Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.74868e-04  1.00000e+00 
          x3  4.23410e-03 -2.72918e-03  1.00000e+00 
          x4 -9.91559e-04  4.18432e-03  6.29539e-03  1.00000e+00 
           y  9.95148e-01  9.68243e-02  1.33659e-02  6.01249e-04  1.00000e+00 

Partial Rank Correlation Matrix between input and output:
                        y 
          x1  9.99908e-01 
          x2  9.90461e-01 
          x3  5.71912e-01 
          x4  8.28989e-02 
```

### The output results for case 2 (4,000 samples): $y = 10 \cdot x_1 + x_2 + 0.1 \cdot x_3 + 0.01 \cdot x_4$

```
Simple Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.85428e-04  1.00000e+00 
          x3  4.22780e-03 -2.73130e-03  1.00000e+00 
          x4  7.87657e-01  5.80151e-03  3.07378e-03  1.00000e+00 
           y  9.94998e-01  9.92135e-02  1.38767e-02  7.84684e-01  1.00000e+00 

Partial Correlation Matrix between input and output:
                        y 
          x1  1.00000e+00 
          x2  1.00000e+00 
          x3  1.00000e+00 
          x4  1.00000e+00 

Simple Rank Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.74868e-04  1.00000e+00 
          x3  4.23410e-03 -2.72918e-03  1.00000e+00 
          x4  7.87660e-01  5.80152e-03  3.07740e-03  1.00000e+00 
           y  9.95156e-01  9.67474e-02  1.33585e-02  7.84441e-01  1.00000e+00 

Partial Rank Correlation Matrix between input and output:
                        y 
          x1  9.99757e-01 
          x2  9.90432e-01 
          x3  5.71597e-01 
          x4  2.79561e-03 
```

### Interpreting the output results for cases 1 and 2

It should be noted the 'perfect' unit values of partial correlation for both cases 1 and 2 for all four input variables, while the partial rank correlations loose 'strength' (get away from the 'perfect' unit value)
as the companion scaling factor gets smaller (the companion scaling factors for $x_1,~x_2,~x_3,\text{ and }x_4$ are respectively 10, 1, 0.1, and 0.01).
Indeed (given that all input variables vary on the same range $[0,1]$):
- an increase in the value of $x_1$, for instance, will almost certainly cause an increase on the value of $y$, since the other (also varying) input variables have a smaller impact on $y$,
- an increase in the value of $x_4$, for instance, will not necessarily cause an increase on the value of $y$, since the other (also varying) input variables have a greater impact on $y$.

### The output results for case 3 (4,000 samples): $y = 10 \cdot x_1 + x_2^2 + x_3^3 + x_4^4$

```
Simple Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.85428e-04  1.00000e+00 
          x3  4.22780e-03 -2.73130e-03  1.00000e+00 
          x4 -9.94643e-04  4.18049e-03  6.27778e-03  1.00000e+00 
           y  9.85817e-01  9.78072e-02  9.31333e-02  7.93418e-02  1.00000e+00 

Partial Correlation Matrix between input and output:
                        y 
          x1  9.97792e-01 
          x2  8.30748e-01 
          x3  8.04121e-01 
          x4  7.70746e-01 

Simple Rank Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.74868e-04  1.00000e+00 
          x3  4.23410e-03 -2.72918e-03  1.00000e+00 
          x4 -9.91559e-04  4.18432e-03  6.29539e-03  1.00000e+00 
           y  9.86584e-01  9.42574e-02  8.92704e-02  7.55616e-02  1.00000e+00 

Partial Rank Correlation Matrix between input and output:
                        y 
          x1  9.97576e-01 
          x2  8.07987e-01 
          x3  7.76838e-01 
          x4  7.39635e-01 
```

### The output results for case 4 (4,000 samples): $y = 10 \cdot x_1 + x_2^2 + x_3^3 + x_4^4$

```
Simple Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.85428e-04  1.00000e+00 
          x3  4.22780e-03 -2.73130e-03  1.00000e+00 
          x4  7.87657e-01  5.80151e-03  3.07378e-03  1.00000e+00 
           y  9.89192e-01  9.21286e-02  8.79782e-02  8.07564e-01  1.00000e+00 

Partial Correlation Matrix between input and output:
                        y 
          x1  9.94180e-01 
          x2  8.28905e-01 
          x3  8.04095e-01 
          x4  5.88750e-01 

Simple Rank Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.74868e-04  1.00000e+00 
          x3  4.23410e-03 -2.72918e-03  1.00000e+00 
          x4  7.87660e-01  5.80152e-03  3.07740e-03  1.00000e+00 
           y  9.90211e-01  8.87022e-02  8.41320e-02  8.06141e-01  1.00000e+00 

Partial Rank Correlation Matrix between input and output:
                        y 
          x1  9.94910e-01 
          x2  8.35003e-01 
          x3  8.08179e-01 
          x4  5.80718e-01 
```

### Interpreting the output results for cases 3 and 4

One can see that the partial correlations are not 'perfectly' 1.0 now (contrary to cases 1 and 2),
since the relations between $x_2\text{ and }y,\text{ between }x_3\text{ and }y$, and between $x_4\text{ and }y$, are not linear anymore.
Both partial and partial rank correlations get away from 1.0 as the exponent of the input variable increases,
since all input variables have the same range $[0,1]$.
If the range were, e.g., $[1,10]$, then we would see the partial correlations increase with the exponents of the respective input variables.

### The output results for case 5 (4,000 samples): $y = x_1 + x_2^2 + x_3^3 + x_4^4$

```
Simple Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.85428e-04  1.00000e+00 
          x3  4.22780e-03 -2.73130e-03  1.00000e+00 
          x4 -9.94643e-04  4.18049e-03  6.27778e-03  1.00000e+00 
           y  5.08267e-01  5.02748e-01  4.58681e-01  4.11674e-01  1.00000e+00 

Partial Correlation Matrix between input and output:
                        y 
          x1  8.33011e-01 
          x2  8.30748e-01 
          x3  8.04121e-01 
          x4  7.70746e-01 

Simple Rank Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.74868e-04  1.00000e+00 
          x3  4.23410e-03 -2.72918e-03  1.00000e+00 
          x4 -9.91559e-04  4.18432e-03  6.29539e-03  1.00000e+00 
           y  5.06996e-01  5.03550e-01  4.47630e-01  3.98242e-01  1.00000e+00 

Partial Rank Correlation Matrix between input and output:
                        y 
          x1  8.09449e-01 
          x2  8.08123e-01 
          x3  7.71237e-01 
          x4  7.31805e-01 
```

### The output results for case 6 (4,000 samples): $y = x_1 + x_2^2 + x_3^3 + x_4^4$

```
Simple Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.85428e-04  1.00000e+00 
          x3  4.22780e-03 -2.73130e-03  1.00000e+00 
          x4  7.87657e-01  5.80151e-03  3.07378e-03  1.00000e+00 
           y  7.22389e-01  4.35217e-01  3.98244e-01  7.03024e-01  1.00000e+00 

Partial Correlation Matrix between input and output:
                        y 
          x1  6.85399e-01 
          x2  8.28905e-01 
          x3  8.04095e-01 
          x4  5.88750e-01 

Simple Rank Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.74868e-04  1.00000e+00 
          x3  4.23410e-03 -2.72918e-03  1.00000e+00 
          x4  7.87660e-01  5.80152e-03  3.07740e-03  1.00000e+00 
           y  7.24908e-01  4.34655e-01  3.89300e-01  6.98789e-01  1.00000e+00 

Partial Rank Correlation Matrix between input and output:
                        y 
          x1  6.81379e-01 
          x2  8.16662e-01 
          x3  7.84219e-01 
          x4  5.52851e-01 
```

### Interpreting the output results for cases 5 and 6

Compared to cases 3 and 4, the four correlations between $x_1\text{ and }y$ loose strength, being now comparable to the correlation strenght between $x_2\text{ and }y$,
since now both $x_1\text{ and }x_2$ are multiplied by the same unit scaling factor.
In case 6, $x_1$ even ceases to be the variable with strongest partial correlations with $y$ (compare both partial Pearson and partial Spearman correlations to case 4).

### The output results for case 7 (4,000 samples): $y = 10 \cdot x_1 + x_2 + 0.1 \cdot x_3 + 0.01 \cdot x_4 + \epsilon$

```
Simple Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.85428e-04  1.00000e+00 
          x3  4.22780e-03 -2.73130e-03  1.00000e+00 
          x4 -9.94643e-04  4.18049e-03  6.27778e-03  1.00000e+00 
           y  9.94100e-01  9.99919e-02  1.51026e-02  1.38078e-03  1.00000e+00 

Partial Correlation Matrix between input and output:
                        y 
          x1  9.99191e-01 
          x2  9.28700e-01 
          x3  2.68709e-01 
          x4  4.69504e-02 

Simple Rank Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.74868e-04  1.00000e+00 
          x3  4.23410e-03 -2.72918e-03  1.00000e+00 
          x4 -9.91559e-04  4.18432e-03  6.29539e-03  1.00000e+00 
           y  9.94293e-01  9.74255e-02  1.46293e-02  1.35072e-03  1.00000e+00 

Partial Rank Correlation Matrix between input and output:
                        y 
          x1  9.99122e-01 
          x2  9.19666e-01 
          x3  2.48062e-01 
          x4  4.45978e-02 
```

### The output results for case 8 (4,000 samples): $y = 10 \cdot x_1 + x_2 + 0.1 \cdot x_3 + 0.01 \cdot x_4 + \epsilon$

```
Simple Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.85428e-04  1.00000e+00 
          x3  4.22780e-03 -2.73130e-03  1.00000e+00 
          x4  7.87657e-01  5.80151e-03  3.07378e-03  1.00000e+00 
           y  9.94110e-01  9.99157e-02  1.50876e-02  7.84438e-01  1.00000e+00 

Partial Correlation Matrix between input and output:
                        y 
          x1  9.97869e-01 
          x2  9.28681e-01 
          x3  2.68826e-01 
          x4  3.35564e-02 

Simple Rank Correlation Matrix among all inputs and outputs:
                       x1           x2           x3           x4            y 
          x1  1.00000e+00 
          x2 -1.74868e-04  1.00000e+00 
          x3  4.23410e-03 -2.72918e-03  1.00000e+00 
          x4  7.87660e-01  5.80152e-03  3.07740e-03  1.00000e+00 
           y  9.94304e-01  9.73412e-02  1.46137e-02  7.84179e-01  1.00000e+00 

Partial Rank Correlation Matrix between input and output:
                        y 
          x1  9.97690e-01 
          x2  9.19579e-01 
          x3  2.48046e-01 
          x4  1.67427e-02 
```

### Interpreting the output results for cases 7 and 8

Compared to case 1, the partial correlations in case 7 are not equal to 1.0 anymore,
since the noise $\epsilon$ introduces a random variability that influences the 'perfect' linear relationship between each input variable and $y$,
the influence getting stronger as the companion scaling factor (10, or 1, or 0.1, or 0.01) gets smaller.

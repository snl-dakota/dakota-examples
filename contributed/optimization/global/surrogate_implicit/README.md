# Summary
_Write short description of the problem, one or two sentences._
 
### Run Dakota
    $ dakota -i <dakota-file>.in -o <dakota-file>.out
 
### More about running this example
_Optionally, write additional information in this section._
 
# What problem does this solve?
_Include a paragraph to describe the problem that will be solved by Dakota. If
no math equation is specified, this description should articulate in English the
information a math equation would provide._
 
## Math Equation
_Optional: Include a LaTex formatted math equation describing the problem (see
example below). If no equation will be specified, delete the header above._

_maximize:_ $` \qquad \qquad f = \frac{horsepower} {250} + \frac {warranty} {100,000}`$

_subject to:_ $` \qquad \qquad sigma\_max \leq 0.5 * sigma\_yield `$

$` \qquad \qquad \qquad \qquad warranty \geq 100,000 `$

$` \qquad \qquad \qquad \qquad time\_cycle \leq 60 `$

$` \qquad \qquad \qquad \qquad 1.5 \leq d\_intake \leq 2.164`$

$` \qquad \qquad \qquad \qquad 0.0 \leq flatness \leq 4.0 `$

# What method will we use?
_Include a paragraph about the chosen Dakota method and the reason for 
choosing this particular method over other possibilities, i.e., identify problem
characteristics that led to the selection._
 
## Analysis Driver
_Characterize the analysis driver._

### Inputs

### Outputs
 
# Interpret the results
 
## Screen Output
_Insert image of screen output:_

---

![Screen Output](DAKOTA_Arrow_Name_horiz.jpg)
 
_Explain the relevance of the image._
 
---

_Insert image of other images (plots, etc.):_

![Other images](DAKOTA_Arrow_Name_horiz.jpg)
 
_Explain the relevance of the image._

---
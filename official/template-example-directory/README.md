# Summary
_Write a short description of the problem, one or two sentences. (The
underscores in this and the following sections indicate text
that you should replace. Do not include the underscores unless
you want text to be rendered in italics.)_


### Run Dakota
    $ dakota -i <dakota-file>.in -o <dakota-file>.out

### More about running this example
_Optionally, in this section, write additional information or instructions that 
would be helpful to run the example. You may wish to include notes about how to
get the example to run on different operating systems_
 
# What problem does this solve?
_Include a paragraph to describe the problem that will be solved by Dakota. If
no math equation is specified, this description should articulate in English the
information a math equation would provide. Describe what Dakota will do, not 
just what the analysis driver calculates._
 
## Math Equation
_Optional: Include a LaTex formatted math equation describing the problem (see
example below). If no equation will be specified, delete the header above. Again,
this section should somehow describe what Dakota will do._


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
 
# Additional Input to Dakota

_Optionally describe input that Dakota needs to run the example in addition to
the input file_

## Analysis Driver
_Characterize the analysis driver._

### Inputs

_Inputs to the analysis driver._

### Outputs

_Outputs from the analysis driver_ 

# Interpret the results

## Screen Output

_Describe the screen output for the study in this section. The text in the
codeblock below should be replaced with relevant Dakota screen output. If the
instructions to run Dakota include redirecting output to file, be sure to note
that. If helpful, the screen output can be broken up between multiple 
codeblocks interleaved with descriptions._

```
Replace this text with relevant Dakota screen output
```

---

_You may also wish to include other images, such as plots,  that clarify the
results._

![Result](DAKOTA_Arrow_Name_horiz.jpg)
 
_Explain the relevance of the image._
 

# Summary

Find the most probable point of "failure" using local optimization
over continuous uncertain variables.

### Run Dakota

   $ dakota -i logratio_uq_reliability.in -o logratio_uq_reliability.out
 

# What problem does this solve?

This example quantifies the uncertainty in the “log ratio” response function:

$`\qquad \qquad g(x1, x2) = \frac {x1} {x2}`$

by computing approximate response statistics using reliability
analysis to determine the response cumulative distribution function:

$`\qquad \qquad P[g(x1, x2) \lt z]`$

where x1 and x2 are identically distributed lognormal random variables
with means of 1, standard deviations of 0.5, and correlation
coefficient of 0.3.

# What method will we use?

A Dakota input file showing RIA using FORM (option 7 in limit state
approximations combined with first-order integration) is listed in
Figure 5.10. The user first specifies the local reliability method,
followed by the MPP search approach and integration order. In this
example, we specify mpp search no approx and utilize the default
first-order integration to select FORM. Finally, the user specifies
response levels or probability/ reliability levels to determine if the
problem will be solved using an RIA approach or a PMA approach. In the
example figure of 5.10, we use RIA by specifying a range of response
levels for the problem.


## Analysis Driver

Built-in Dakota driver, log_ratio 

_TODO: Characterize the analysis driver._

### Inputs

### Outputs
 

# Interpret the results
 
## Screen Output

The resulting output for this input is shown in Figure 5.11, with
probability and reliability levels listed for each response level.
Figure 5.12 shows that FORM compares favorably to an exact analytic
solution for this problem. Also note that FORM does have some error in
the calculation of CDF values for this problem, but it is a very small
error (on the order of e-11), much smaller than the error obtained
when using a Mean Value method, which will be discussed next.

![Screen Output](logratio_uq_reliability_cdf.png)


### FORM Results 


If the user specifies local reliability as a method with no additional
specification on how to do the MPP search (for example, by commenting
out mpp search no approx in logratio_uq_reliability.in), then no MPP
search is done: the Mean Value method is used.

![Screen Output](logratio_uq_reliability_mv.png)

The mean value results are shown above and consist of approximate mean
and standard deviation of the response, the importance factors for
each uncertain variable, and approximate probability/reliability
levels for the prescribed response levels that have been inferred from
the approximate mean and standard deviation (see Mean Value section in
Reliability Methods Chapter of Dakota Theory Manual [4]).  It is
evident that the statistics are considerably different from the fully
converged FORM results; however, these rough approximations are also
much less expensive to calculate. The importance factors are a measure
of the sensitivity of the response function(s) to the uncertain input
variables.

![Screen Output](cdf_form.png)



A comparison of the mean value results with the FORM
results is shown in Figure 5.12. The mean value results are not
accurate near the tail values of the CDF, and can differ from the
exact solution by as much as 0.11 in CDF estimates. A comprehensive
comparison of various reliability methods applied to the logratio
problem is provided in [36].

Additional reliability analysis and design results are provided
in Sections 20.10.1-20.10.5




 



_Explain the relevance of the image._
 
---

_Insert image of other images (plots, etc.):_

![Other images](DAKOTA_Arrow_Name_horiz.jpg)
 
_Explain the relevance of the image._

---
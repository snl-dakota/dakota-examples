# Summary

Unmaintained example of linking Dakota to Rsmas simulator implemented
in Fortran

# Description

Demonstrates application of Dakota optimization and parameter study to
a simple Fortran simulation of a Rankine Cycle Space Power System.

Caveat: This example was contributed prior to 2010 and not maintained
since, but is included as may contain useful nuggets of interfacing
information.

This content migrated from top-level Dakota Git repo at
`fd500c77fc94fe3dceab864e1f7235820386a321`

# Contents

* `dakota_rsmas_ga_opt.in`, `dakota_rsmas_grad_opt.in`,
  `dakota_rsmas_pstudy.in`: Dakota input files for global
  optimization, gradient-based optimization, and parameter study,
  respectively.
* `rsmas_driver`: Analysis driver to run the Rsmas simulation
* `rsmas.f`: Fortran simulation code
* `rsmas.in`, `rsmas.template`: Representative input and templated
  input files
* `rsmas.out`: Representative simulation output

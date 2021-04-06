# Summary

(Unmaintained examples of) Dakota interfacing to analysis drivers
through compiled/linked interfaces.

# Description

Examples of using Dakota with tightly-linked simulation interfaces,
such as to MATLAB, Pyomo (via Dakota's AMPL interface), or Scilab, for
variable to response mapping. These embedded interfaces all require
compiling Dakota from source and enabling the linked interface. When
enabled, they facilitate efficient, in-memory communicaiton between
Dakota and the simulation analysis driver.

The ModelCenter example additionally demonstrates plugging Dakota into
ModelCenter as a solver and calling back to ModelCenter for function
evaluations

Caveat: These examples were contributed prior to 2010 and not
maintained since, but are included as they may contain useful nuggets
of interfacing information.

This content migrated from top-level Dakota Git repo at
`fd500c77fc94fe3dceab864e1f7235820386a321`

# Summary

(Unmaintained examples of) Dakota interfacing to analysis drivers
through interprocess communication.

# Description

The examples in this directory each include analysis driver shims to
facilitate communication between Dakota's interface and a separate
process performing the ultimate interface evaluation for variable to
response mapping.

For example, a typical fork or system script interface to a simulator
written in MATLAB might incur large overhead on each function
evaluation while the MATLAB instance starts and license checks
happen. The MATLAB example here instead starts a single MATLAB
instance and then uses named pipes to communicate between Dakota and
it in a much more streamlined manner.

Caveat: These examples were contributed prior to 2010 and not
maintained since, but are included as they may contain useful nuggets
of interfacing information.

This content migrated from top-level Dakota Git repo at
`fd500c77fc94fe3dceab864e1f7235820386a321`

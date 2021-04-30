# Summary
Use an analysis driver written in Windows batch (bat) to run a simulation

# Description

Dakota does not know how to set up, run, or get output from a user's simulation.
The user is responsible for creating a *driver* that carries out those tasks on Dakota's
behalf. In a typical study, Dakota runs the driver one time for each evaluation, which is
a mapping from a single point in input/parameter space to a corresponding point in response/output
space.

The driver has three main responsibilities.

1. **Preprocessing**: Dakota provides parameter values to the driver by writing them to a *parameters file*.
   It communicates the name of the parameters file to the driver by passing it as its first command line argument. 
   In the preprocessing phase, the driver uses values it reads from the parameters file to construct valid
   input for the simulation.
2. **Execution**: The driver runs the user's simulation.
3. **Postprocessing**: In this phase, the driver extracts response information from simulation output and
   writes it to a correctly formatted Dakota results file. Dakota provides the
   name of the results file as the second command line argument to the driver.

Because Dakota does not directly interpret the driver and relies on the operating system
and other tools on the user's system to execute it, the driver can be written in any programming
language. The Microsoft Windows operating system natively supports the "batch" scripting language,
which may be used for this purpose.

This example shows how to use Windows batch to write a simple driver. The driver works in concert with
several convenient Dakota interfacing features, which will also be explained.

# Dakota interface block

The `interface` along with the `variables`, and `responses` blocks in the Dakota input input file can be thought
of as forming a contract between Dakota and the driver. Here we will focus our attention on the `interface` block
in the example Dakota input file `dakota_rosenbrock.in`.

```
interface
    system	
	  analysis_driver = 'simulator_script.bat'
	  parameters_file = 'params.in'
	  results_file    = 'results.out'
      file_save
	  work_directory directory_tag directory_save  named 'workdir'
	  copy_files = 'templatedir/*'
 	  deactivate active_set_vector
```

It specifies several pieces of information and enables several options.

* `system`: Ordinarilly, the `fork` interface type is preferred. However, Dakota's `system` interface is needed when
    running .bat scripts.
* `analysis_driver`: The name of (and optionally the path to) the driver.
* `parameters_file` and `results_file`: The names of the parameters files that Dakota will write and
   results files that Dakota will expect the driver to write.
* `file_save`: By default, Dakota cleans up the parameters files and results files by deleting them
   at the end of each driver execution. The `file_save` keyword directs Dakota to preserve them instead.
* `work_directory`: Dakota will run the driver in a work directory that it creates.
* `directory_tag`: Create a new work directory for each evaluation, "tagging" them with the unique evaluation number.
* `directory_save`: Don't clean up the work directories.
* `copy_files`: Copy files matching the glob into the work directory prior to running the driver. In this example,
   the template directory contains an input template for the simulator.
* `deactivate active_set_vector`: See section 9.7 of the User's Manual for a description of the active set vector.

All of these keywords are described in greater detail in the
[Reference Manual](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/interface.html).

# Driver

The driver is `simulator_script.bat`. It is responsible for setting up input for the simulator, `rosenbrock_bb.py`,
running it, and extracting results from its output to place into the Dakota results file. Dakota runs the driver
in an evaluation-specific, tagged work directory.

The script uses `dprepro`, a Dakota-provided template processing tool, to substitute values from
the parameters file into a template to create valid input for the simulator. `rosenbrock_bb.py`'s input file is `ros.in`.
The `dprepro` tool is documented in section 10.9 of the User's Manual. In this simple example, the template,
`ros.template`, contains the substitution tokens `{x1}` and `{x2}`. They will be replaced by the values of `x1` and `x2`
that Dakota provides. The `dprepro` tool is written in Python. Although Windows can be configured to automatically run
.py files using the Python intepreter, it is often safer to be explicit.

Once the input has been created, the script runs `rosenbrock_bb.py`. Dakota will copy `rosenbrock_bb.py` from `templatedir/`
 to the working directory before launching the driver. The simulator produces one output file named `ros.out`.

Finally, after the simulator has completed runing, the driver extracts response information from `ros.out` and places it
in the results file. Three approaches are illustrated in the driver. In the first, common Unix text processing tools are
used. These are not natively available on Windows and must be installed. In the second, Perl one-liners are used. These of
course require a Perl installation. Finally, Python one-liners are used.

# How to run the example

First, edit `simulator_script.bat` so that the variable `dakota_install` points to your Dakota install. The driver uses
this information to find `dprepro.py`.

Then, run Dakota in the `windows_bat` folder:

`dakota dakota_rosenbrock.in`

# Things to notice

While it is running, Dakota will create several work directories named `workdir.N`. Examine the contents of one of these
and find the Dakota parameters file (`params.in`), simulator input (`ros.in`) and output (`ros.out`) files, and Dakota
results file (`results.out`). Make sure you understand how Dakota, `dprepro`, the driver (including the tools it uses, such as 
Perl or Python), and the simulator created each one.

# Requirements

Bash, Python 3, and (optionally) Perl or Unix text processing tools.

# Contents

* `dakota_rosenbrock.in`: Dakota input file
* `simulator_script.sh`: Driver
* `templatedir/ros.template`: Template input file for `rosenbrock_bb.py`.
* `templatedir/rosenbrock_bb.py`: Simulator that runs the Rosenbrock test problem (Section 20.2 of the User's Manual)

# Further Reading

* Chapter 10 of the User's Manual provides a full description of interfacing in Dakota.
* The `interface` keyword documentation in the [Reference Manual](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/interface.html)
  contains detailed descriptions and more examples.
* Microsoft [documents](https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/windows-commands) commands available
 in batch scripting, although it's often more convenient to search the web for examples!

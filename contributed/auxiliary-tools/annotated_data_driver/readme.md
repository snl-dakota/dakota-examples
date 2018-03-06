# Annotated Data Driver

This is a simple tool to feed back to Dakota, values from a data table. It is useful if you, say, compute a new QoI from the same model evaluations. As long as Dakota only requests the same data as the data file, it will return the values.

Note that Dakota is *deterministic* for most methods including sample **when given a `seed`**. That is one reason it is important to always seed the sample.


The `interface` block of your Dakota input should look something like:

    interface
         fork 
           analysis_driver = 'python annotated_data_driver.py [FLAGS] datafile

And the response block **MUST** have `descriptors` that match the column names of the data. See Command Line Help below for description of the flags

## Data Formats

`annotated_data_driver.py` supports comma-separated data and comment-labeled columns (such as those Dakota returns). It is robust to *some* text in columns such as those Dakota may provide for `interface`

Examples: (the first few lines)

comma separated values

```
ix,x,y,z,fun1,fun2,fun3,fun4,fun5
1,0,0,0,0,0,0,0,0
2,0,0,0.25,0.25,0,0,0.25,0
3,0,0,0.5,0.5,0,0,0.5,0
```

comments with column labels:

```
%   ix      x      y      z   fun1   fun2   fun3   fun4   fun5
    +1     +0     +0     +0     +0     +0     +0     +0     +0
    +2     +0     +0   +0.2   +0.2     +0     +0   +0.2     +0
    +3     +0     +0   +0.5   +0.5     +0     +0   +0.5     +0
```



## Command Line Help

The following is the result of `$ python annotated_data_driver.py --help`

```
usage: annotated_data_driver.py [-h] [-s "param=value"] [-t TOL] [-v]
                                datafile paramsfile resultsfile

Dakota Usage:
-------------
Note that responses and variables MUST have descriptors that match
the data

    ...
    interface
     fork
       analysis_driver = 'python annotated_data_driver.py [FLAGS] datafile'
       asynchronous evaluation_concurrency 10

    ...

    responses
       response_functions = 1
              descriptors = 'function_name' # >>>> REQUIRED <<<<

CLI Usage:
----------

    annotated_data_driver.py [FLAGS] datafile paramsfile resultsfile
                                     \_user_/ \_______Dakota_______/

Note that extra columns are ok but the response must ONLY match a single
row. Use continuous_state variables to set values if needed.

positional arguments:
  datafile              Annotated tabular data file. The delimiter will be
                        automatically deduced and text columns will be removed
                        if possible. Set by the user!
  paramsfile            Dakota params file. To be set by Dakota!
  resultsfile           Dakota results file. To be set by Dakota!

optional arguments:
  -h, --help            show this help message and exit
  -s "param=value", --set "param=value"
                        set additional fixed values with "param=value" format.
                        Alternatively, use Dakota continuous_state variables
  -t TOL, --tol TOL     [1e-6]. Set the tolerance. All columns are normalized
                        to [0,1] (and the same transformation is applied to
                        the params). The difference is found as the root-mean-
                        square from the params.
  -v, --verbose         print result information

Version: 20171025.1
```

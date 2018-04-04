# Matlab Daemon Interface

Dakota does provide a Matlab interface *if* it has been compiled. The generally accepted alternative is to create a bash script that calls Matlab. However both of these methods are extremely slow since it must boot up matlab at one.

This tools solves the problem by instead creating a Matlab listener and a dakota `analysis_driver` to tell matlab to run

## Usage:

This comes in two parts: `send_to_matlab.py` and `dakota_daemon.m`

Dakota calls `send_to_matlab.py` which processes the inputs and creates a file read by `dakota_daemon.m`

### In Dakota

Use something along the lines of the following in the `interface` block:

```dakota
interface
    analysis_driver = 'python send_to_matlab.py'
    fork 
        asynchronous evaluation_concurrency = 20
```

### In Matlab

First, you must create a function that takes the input and returns your value. Input can be passed in one of the following `'mode'`s:

* `'struct'` - Will pass a matlab structre of each parameter specified in  Dakota. For example, parameter `v` will be `params.v`.  WARNING: Names must be valid matlab field names.
* `'array'` - Will pass a vector of parameter values *in the order from Dakota*. See Dakota documentation for ordering
* `'filename'` - Will pass the Dakota parameter filename to the function

For example, a simple function may be 

```matlab
>> myfun = @(X) X(1).^2 + X(1).*X(2);
>> dakota_daemon(myfun,'mode','array')
```

Or, to run the example (which takes struct input),

```matlab
>> dakota_daemon(@matlab_rosen,'mode','struct')
```

### Combined

It does not matter if you start Dakota or Matlab first. They will wait for each other. However, once Dakota has completed, you will need to break the exectution of the matlab program. Use CTRL-C

## Additional Notes:

The directory `DAKOTA_MATLAB_TMP` may remain if the execution was terminated too soon. It is safe to delete this directory.

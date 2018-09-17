# Surrogate from Python

This is a simple wrapper that allows you to build and evaluate a surrogate from within python using Dakota. This has been tested on macOS and Linux. It is not expected to work directly on Windows. Last tested with Dakota 6.8, python 2.7 and 3.6

## Demo:

See `demo.py` for more details. Essentially there are two ways to call the Dakota surrogate. 

* As a function
* As a callable class

To call as a function, the call signature looks like:

```
import dakota_surrogate
surrogate = dakota_surrogate.DakotaSurrogate(X,f)
surrogate(Xp)
```

The class version is:

```
import dakota_surrogate
dakota_surrogate.dakota_surrogate(X,f,Xp)
```

## Tips

On some systems where Dakota is not installed, (e.g. CEE Blades), the following line will set the `dakota` variable:

    >>> import subprocess
    >>> dakota = subprocess.check_output('module load dakota;command which dakota',shell=True).decode('utf8').strip()

## Efficiency Note

This tools does not store any information between runs. On every invocation, it independently runs Dakota to build and then evaluate the surrogate. Therefore, for performance, it is critical to evaluate as many surrogate values as possible at the same time.

Also, unless `bounds` are specified in construction, it is possible that the automatic bound specification could cause very small changes to results between calls. Therefore, if the bounds are known ahead of time, it is best to use them

## Known Issues / Limitations

* Must rebuild upon all invocations -- see "Efficiency Note"
* Only supports uniform inputs. Non-uniform inputs should still work but may not provide the optimal answer.
* Bounds are based on inputs if not specified. This has a few affects:
    1. Multiple calls with the same training data *could* yield different results
    2. A non-uniform distribution of points could skew the bounds. 
* Very limited inputs. Use Dakota directly if more control is needed

# Detect Failure

Dakota has a method to re-run a model realization upon failure. However, it *must* be told the model failed.

From the documentation (v6.6):

> The first step is that Dakota must detect analysis failure. Importantly, Dakota always expects a results file to be written by the analysis driver, even when a failure has occurred. If the file does not exist when the analysis driver exits, a Dakota error results, causing Dakota itself to terminate. The analysis driver communicates an analysis failure to Dakota by writing a results file beginning with the (case-insensitive) word "fail". Any file contents after "fail" are ignored.

The problem is that some codes will fail without the analysis driver knowing there was a failure. This code is run as an `output_filter` in the `interface` block. If it does not detect the correct output file existing, it will write the failure to Dakota.

## Usage

In Dakota:

```dakota
interface
	fork
    	analysis_driver = './failcode'
    	output_filter = 'python detect_failure.py'
    	
    	# ... all of the other normal interface specifiers
    
    # Capture and retry once
    failure_capture
        retry 1
```

## Example

The example problem is simply designed to "fail" once and then work the next time. When it fails, it simply quites.

When it is run, the following will be found in the output:

    Failure captured: retry attempt 1/1 for evaluation 3.



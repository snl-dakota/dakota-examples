# Summary

TODO

# Description

TODO

# Python driver module

TODO

# Dakota input

TODO


# How to run the example
 
 Make sure the Python used to build Dakota is in the environment PATH and
 that the PYTHONPATH includes the directory containing the textbook.py
 driver script.

Run Dakota

    $ dakota -i dakota_textbook_python.in
 
# Requirements

Dakota built with Python support. The downloads available on the Dakota website come with Python enabled.
The major.minor version of Python (e.g. 2.7, 3.8) in your environment must match the one included with Dakota.
The version that comes with Dakota can be checked by examining the contents of the bin folder, which contains a
versioned Python library. We recommend setting up a conda or virtual environment to use with Dakota in order to
satisfy the version requirements.

# Contents

* `dakota_textbook_python.in`: Dakota input file
* `textbook.py`: Combined simulator and analysis driver

# Further reading

* The Textbook function is described in more detail in the 
  [Reference Manual](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/textbook.html).
* More details of the Python linked interface can be found in the [Reference
  Manual](https://dakota.sandia.gov//sites/default/files/docs/latest_release/html-ref/interface-analysis_drivers-python.html)
  and in Section 16.3.2 of the [User's Manual](https://dakota.sandia.gov/content/manuals).
 

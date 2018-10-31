# General Instructions

TODO - Anything that needs to be listed here?

# Contributing Dakota Examples

1. From https://gitlab-ex.sandia.gov/Dakota/dakota-examples, create a fork of
   the Dakota examples repository by clicking the `Fork` button. Clone your
   forked copy to your local workstation.

2. FOR OFFICIALLY-SUPPORTED examples, copy the official/template directory into
    the official directory.
   FOR USER-CONTRIBUTED examples, copy the contributed/template directory into
   the contributed directory.

   Rename new directory to a descriptive example name. Users may access the
   repository directly (not through the GUI or Dakota website). Descriptive
   example names will help users navigate to examples they are interested in.

3. Update the README.md file for your example. See Guidance for README.md
   section below.

4. Update the example.json file  for your example. See Guidance for README.md
   section below.

5. Test your README.md and JSON files.
   ```bash
   python test-examplefiles.py  \
       -r ../official/template-example-directory/README.md \
       -j ../official/template-example-directory/example.json
   ```
   If you get errors, test with the verbose flag on.
   ```bash
   python test-examplefiles.py -v  \
       -r ../official/template-example-directory/README.md \
       -j ../official/template-example-directory/example.json
   ```

6. Push changes to your forked repository.
7. In the GitLab GUI forked repository, create a merge request by clicking 
the `Merge Requests` link on the left sidebar, then clicking the `New merge
request` button in the center of the page, then selecting the proper target and
source branches.

# Updating the README.md File

TODO

# Updating the JSON File
The template, `example.json`, makes simplifying assumptions about typical
example metadata required for offically-supported and user-contributed examples.
Below is the JSON specification with valid fields, whether they are REQUIRED or
OPTIONAL, and a short description or example value. The following sections will
provide guidance for customizing your JSON file. 

## Valid JSON Fields

```javascript
{
    "name": "title of example",
    "example_id": "(REQUIRED) unique id",
    "parent_id": "(OPTIONAL) example_id of parent to link related examples",
    "maintainer": {
        "name": "(REQUIRED only for user-contributed examples) John Doe",
        "email": "jdoe@sandia.gov"
    },
    "doc_links": [
        {"name": "(OPTIONAL) user-friendly name",
         "url": "URL link"
        },
        {"name": "Theory Manual Article ",
         "url": "https://example-b.url"
        }
    ],
    "analysis_type": "(REQUIRED) Optimization",
    "analysis_type": ["Optimization", "Calibration"],
    "goal": ["(OPTIONAL)", "Bound", "Correlations"],
    "method": "(REQUIRED) SQP"
}
```


## Hints for Updating JSON Files

1. Valid JSON syntax:
   * Enclose field/value pairs in braces.
   * Fields and values are strings, separated by a colon, `:`.
   * Field/value pairs are separated by commas, `,`, except the last
     field/value pair.

   ```javascript
   {
        "item1": "value1",
  	    "item_last": "value_last_NO_COMMA"
   }
     ```

2. List values (one line).
   Note, there is no comma after the last item.

   ```javascript
   {
        ...
        "list_name_one_line": ["Optimization", "Calibration"],
	    ...
   }
   ```
   
3. List values (many lines).
   Note, there is no comma after the last item.

   ```javascript
   {
	    "list_name_one_line": [
	        "Optimization",
	        ...
	        "Calibration"
	    ],
   }
   ```


## Guidance for Customizing the Dakota Example JSON File

* Field `"name"`: This should be a short descriptive name for your example.

* Field `"example_id"`: This field will be used to link related examples.
   This allows us to change the organization of the examples repository without
   updating all the json files.

* Field `"parent_id"`: If your example is the main example having related
   examples, this field is not necessary. Delete this line from your JSON file.

* Field `"maintainer"`: This field is not required for officially-supported
   Dakota examples but **_IS REQUIRED for user-contributed examples_**. The
   official Dakota JSON template will not have this field listed.

* Field `"doc_links"`: This field is not required for officially-supported
   Dakota examples. The entire section between ellipses should be deleted
   from your JSON file:

   ```javascript
   {
       ...
       "doc_links": [
           {"name": "(OPTIONAL) user-friendly name",
            "url": "URL link"
           },
           {"name": "Theory Manual Article ",
            "url": "https://example-b.url"
           }
       ],
       ...
   }
   ```
   
*  Field `"analysis_type"` can be a list or a single value. It is a
   **_REQUIRED_** field. The template JSON files by default specify a single
   value. See (Hints for Updating JSON Files, #2, #3 for help specifying a
   list. Valid `analysis_type` values are listed below:

   - "Sensitivity Analysis"
   - "Optimization"
   - "Uncertainty Quantification"
   - "Calibration"
   - "Advanced"

* Field `"goal"` can be a list or a single value. It is an **_OPTIONAL_**
  field. Delete the following line if you do not specify a goal.

   ```javascript
   {
       ...
       "goal": ["Bound", "Correlations"],
       ...
   }
   ```

  A single-value field can be specified as `"goal": "Bound",` or as
  `"goal": ["Bound"],`.

  Valid general and constraint `goal` values are listed below:
   - "Bound"
   - "Bound and Linear"
   - "Bound and Non-linear"
   - "Linear"
   - "Non-linear"
   - "Unconstrained"
   - "Analysis of Variance"
   - "Correlations"
   - "Principal Components"
   -"Sobol Indices"

*  Field `"method"` can be a list or a single value. It is a
   **_REQUIRED_** field. The template JSON files by default specify a single
   value. See (Hints for Updating JSON Files, #2, #3 for help specifying a
   list. Valid `method` values are listed below:

   - "Bayesian"
   - "Conjugate Gradient"
   - "DACE"
   - "Divided Rectangles"
   - "Epistemic"
   - "Feasible Directions"
   - "Genetic Algorithms"
   - "Hybrid Optimization"
   - "Least Squares"
   - "Mixed Aleatory-Epistemic UQ"
   - "Newton"
   - "Optimization Under Uncertainty"
   - "Other"
   - "Parameter Study"
   - "Pattern Search"
   - "Reliability"
   - "Sampling"
   - "SQP"
   - "Stochastic"
   - "Stochastic Expansion"
   - "Surrogate-Based Optimization"
   - "Surrogate-Based Optimization Under Uncertainty"
   - "Surrogate-Based UQ"




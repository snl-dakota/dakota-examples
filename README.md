# Dakota Examples Repository

A collection of official and user contributed [Dakota][] examples and
auxiliary tools.

[Dakota]:https://dakota.sandia.gov/


## How to use this repository

We recommend you access this repository using the latest Dakota GUI. You may
also go to diretctly to the GitLab repository and browse the file directories.


### File System

The repository is located on the Sandia SON GitLab server at
https://gitlab-ex.sandia.gov/dakota/dakota-examples. It may be cloned to your
local machine or downloaded as a zipfile.

It is divided into two examples subdirectories, official and contributed. In
addition, it provides several convenient utilities:
- test-examplefiles.py: to test for and fix JSON or example file errors before
  committing

### Dakota GUI

The Dakota GUI is a convenient and powerful way to view and find examples. It
includes an advanced search interface to quickly search for examples by analysis
type, method, and goal. Download the Dakota GUI from
https://dakota.sandia.gov/download.html.


# Contributing Dakota Examples

## First time setup

1. From https://gitlab-ex.sandia.gov/Dakota/dakota-examples, create a fork of
   the Dakota examples repository by clicking the `Fork` button.

2. Clone your forked copy to your local workstation, replacing:
   - \<forked Git URL\> with the repository URL from the forked repository,
     e.g., git@gitlab-ex.sandia.gov:\<username\>/dakota-examples.git
   - \<my_local_dakota_repo_fork\> with a valid name for your local repository.

      ```bash
      git clone <forked Git URL> <my_local_dakota_repo_fork>
      ```
3. Add an upstream remote:
      ```bash
      git remote add upstream git@gitlab-ex.sandia.gov:dakota/dakota-examples.git
      ```
   Your remotes should look like the following. The URL of the upstream remote
   should have the URL of your forked repository.
      ```
      $ git remote -v
      origin	git@gitlab-ex.sandia.gov:dmvigi/dakota-examples.git (fetch)
      origin	git@gitlab-ex.sandia.gov:dmvigi/dakota-examples.git (push)
      upstream	git@gitlab-ex.sandia.gov:<namespace>/dakota-examples.git (fetch)
      upstream	git@gitlab-ex.sandia.gov:<namespace>/dakota-examples.git (push)
      ```

   *NOTE: you will not be able to push to the Dakota repository.*


## Adding a new example

### A brief description of our workflow

1. On the local repo you created in [First time setup](#first-time-setup), step #2`, create and
   checkout a feature branch.
2. Make changes to the files.
3. Commit your changes to the branch.
4. Push your branch to the remote fork you created in [First time setup](#first-time-setup), step 1`.
5. In GitLab, issue a merge request from your fork to the Dakota examples
   repository.


### Using the workflow to create a new Dakota example

1. Update your forked repository:
      ```bash
      git pull origin master
      git pull upstream master
      ```

2. Create a Git branch, replacing <new-dakota-example> with a valid branch name.
      ```bash
      git branch <new-dakota-example>
      git checkout <new-dakota-example>
      ```

3. FOR OFFICIALLY-SUPPORTED examples, copy the official/template directory into
   the official directory.
   FOR USER-CONTRIBUTED examples, copy the contributed/template directory into
   the contributed directory.

   Rename new directory to a descriptive example name. Users may access the
   repository directly (not through the GUI or Dakota website). Descriptive
   example names will help users navigate to examples they are interested in.

4. In your new directory, update the README.md file for your example. See
   Guidance for README.md section below.

5. In your new directory, update the example.json file  for your example. See
   Guidance for README.md section below.

6. Test your README.md and JSON files.
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
   
7. Add and commit your files in <new_directory>. Push changes to your fork.
      ```bash
      git add <new_directory>
      git commit
      git push origin <new-dakota-example>
      ```
8. In the GitLab GUI, issue a merge request and clean up forked repository.
   - Navigate to your forked repository, and issue a Merge request:
     You may see a `New merge request` button at the top of the main window.
     Or on the left sidebar, click the `Merge request` link.
   - Select your feature branch as the source branch and the Dakota examples
     repository master branch as the target branch.
   - Submit the merge request. You should then see a `Merge` button to
     merge your branch to the forked master branch. Optionally, click the box to
     remove the source branch to delete your feature branch onece the merge
     request is approved.
   - Once the merge request is approved, if you clicked the box in the step
     above, you will see a button to remove the source branch. Click the button
     to remove your feature branch. Repeat step #1 above to sync your local
     fork.


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
    ...
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

   "Sensitivity Analysis"
   "Optimization"
   "Uncertainty Quantification"
   "Calibration"
   "Advanced"

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
   "Bound"
   "Bound and Linear"
   "Bound and Non-linear"
   "Linear"
   "Non-linear"
   "Unconstrained"
   "Analysis of Variance"
   "Correlations"
   "Principal Components"
   "Sobol Indices"

*  Field `"method"` can be a list or a single value. It is a
   **_REQUIRED_** field. The template JSON files by default specify a single
   value. See (Hints for Updating JSON Files, #2, #3 for help specifying a
   list. Valid `method` values are listed below:

   "Bayesian"
   "Conjugate Gradient"
   "DACE"
   "Divided Rectangles"
   "Epistemic"
   "Feasible Directions"
   "Genetic Algorithms"
   "Hybrid Optimization"
   "Least Squares"
   "Mixed Aleatory-Epistemic UQ"
   "Newton"
   "Optimization Under Uncertainty"
   "Other"
   "Parameter Study"
   "Pattern Search"
   "Reliability"
   "Sampling"
   "SQP"
   "Stochastic"
   "Stochastic Expansion"
   "Surrogate-Based Optimization"
   "Surrogate-Based Optimization Under Uncertainty"
   "Surrogate-Based UQ"




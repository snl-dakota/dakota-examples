# Summary

This example demonstrates how to submit a Dakota job to a remote machine with a job queue, using the Dakota GUI (more specifically, using the Next-Gen Workflow tool within Dakota GUI).

# Description

There are generally two types of remote machines that you can submit Dakota jobs to: non-queued machines and queued machines. As the name implies, queued machines have job queues. On a queued machine, you must submit your job into the queue and wait your turn to use the high-performance resources:

![alt text](img/JobSubmissionDiagram.png "Example remote job submission")

For the example of submitting a Dakota job to a remote queued machine, you will be creating at least two workflows, as pictured above. The first workflow will run locally on your machine, and its primary responsibility will be uploading files and starting the remote process for NGW, using a **remoteNestedWorkflow** node.

The secondary workflow sent off by the remoteNestedWorkflow node will arrive at a staging area called **the login node.** This is not the appropriate place to perform the job, especially if the job requires heavy-duty computation. This secondary workflow sitting on the login node must itself be smart enough to submit work into a **job queue.** The work submitted to the job queue will then wait in line with other jobs waiting to use that machine.

Once it is your job's turn, the actual work will be performed, after which the results can be transferred back to your local machine for review.

This overall task is complicated by the fact that queue submission is typically script-based, which means that the job itself must be governed by a series of shell scripts (instead of an NGW workflow), so you must be moderately comfortable reading and writing scripts to do queued job submission. However, we have developed a special node called **dakotaQueueSubmit**,  designed to make this step easier.

To summarize, the basic approach for a queued remote machine is as follows:

1. Create a workflow that will be run locally on your machine, and will include a **remoteNestedWorkflow** node, which sends a second workflow to the queued machine's login node. The remoteNestedWorkflow node will include configuration for how to connect to the remote machine login node (the machine name, credentials, etc.)
2. Create a second workflow that will be run on the login node of the queued machine, and will include a **dakotaQueueSubmit** node. The dakotaQueueSubmit will prepare scripts that will be executed once in the job queue.
3. Review the scripts that the dakotaQueueSubmit node governs and validate that they are appropriately written for your environment.

# Contents

- `cantilever` - the simulation model for the cantilever beam physics problem.
- `cantilever.template` - the templatized input for the cantilever beam.
- `CPS.in` - the Dakota study to be run remotely.
- `LocalWorkflow.iwf` - the first of three workflows, which must be run locally on your machine and is responsible for sending the job to the remote machine.
- `LoginNodeWorkflow.iwf` - the second of three workflows, which will run on the login node. This workflow is responsible for submitting Dakota into the job queue.
- `WorkflowDriver.iwf` - the third, innermost workflow, which acts as Dakota's analysis driver. This analysis driver represents the standard Cantilever beam simulation model used for many Dakota examples. This workflow is not directly called by either LoginNodeWorkflow.iwf or LoginNodeWorkflow.iwf, but is called by Dakota.

# Some notes before we get started

- A presupposition of this workflow is that the **server/headless version of Next-Gen Workflow is already installed and available on the remote machine.** Talk to your system administrator to ensure that NGW has already been installed on whatever machine you will be submitting your workflow to.
- Login credentials for the remote machine must have already been previously configured. For example, you will not recieve an opportunity to type in your password once the workflow has begun executing. Refer to "Window > Preferences > Connection & Login Preferences" to set your login credentials.

# How to run the example

## Step 1. Configure LocalWorkflow.iwf

After importing this example into the GUI, double-click LocalWorkflow.iwf. You will be presented with a workflow that looks like this:

![alt text](img/LocalWorkflow.png "LocalWorkflow.iwf")

Note that the connection lines between the file nodes and the remoteNestedWorkflow node are green. Green lines denote that the File Transfer Behavior of the connection is set to "Copy file to target," since the file must be moved from the local machine to the remote machine.

(If you would like to inspect the file transfer behavior, simply click on the connection line and see what the "File Transfer Behavior" property is set to in the Settings view for the connection line.)

Now, click on the remoteNestedWorkflow node, and adjust its properties in the Settings view:

- Verify that the "fileName" property is set to "RemoteWorkflow.iwf."
- Set the "hostname" property to the name of the remote machine you will be connecting and sending files to.
- Set the "username" property to your username on the remote machine.
- Set the "remotePath" property to the remote destination which you would like to act as your remote directory.
- Set the "wflib" property to the installation location of headless NGW on the remote machine.

## Step 2. Configure LoginNodeWorkflow.iwf

Now, double-click RemoteWorkflow.iwf. You will be presented with a workflow that looks like this:

![alt text](img/LoginNodeWorkflow.png "LoginNodeWorkflow.iwf")

Click on the "dakotaQueueSubmit" node to edit its properties in the Settings view:

- Your job submission account ID number should be provided in the "account" field. Talk to your system administrator if you need a job submission account ID number.
- Check the "continueAfterSubmit" checkbox if you want the workflow to return immediately after completing the job submission (i.e. it will not wait for Dakota to finish executing the job). This is useful during the period when you are first setting up your remote job submission workflow, and will most likely have to do a bit of troubleshooting before your workflow is running smoothly.
- Set the number of hours and minutes to provision for your job in the "job.hours" and "job.minutes" fields.
- Set the required number of nodes and processors you need in the "num.nodes" and "num.processors" field.
- Set the type of queue ("batch" is the default for Slurm).

## Step 3. Adjust the dakotaQueueSubmit node scripts (if necessary)

Most of these fields correspond to *tokens* in the shell scripts that the dakotaQueueSubmit node is responsible for executing.

For example, let's look at a portion of the "submit-dakota.sh" script, which submits our Dakota job into a Slurm queue using the "sbatch" command:

    sbatch -N ${num.nodes} \
           --partition=${queue} \
           --time=${job.hours}:${job.minutes}:0 \
	       -A ${account} \
           runDakotaRemote.sh \
           2>dart.id.err | tee dart.id.out

Values that you provide in the properties of the dakotaQueueSubmit node are replaced by their corresponding tokens in the script.

If you need to edit any of these scripts, you may supply your own variations by using the properties in the "Script Substitution" section of the dakotaQueueSubmit node.

1. The "submitScript" is responsible for submitting the job into the job scheduler (in our example script, the job scheduler is Slurm, and the command used to submit is "sbatch"). This script is NOT directly responsible for running Dakota (see the "runDakotaScript" script below).
2. The "statusScript" is responsible for checking whether the job has completed or not.
3. The "checkjobScript" is responsible for checking the status of the job in the queue.
4. The "cancelScript" is responsible for stopping the job in the queue if the user stops Next-Gen Workflow.
5. Finally, the "runDakotaScript" is responsible for loading and executing Dakota.

## Step 4. Configure WorkflowDriver.iwf

Now, double-click WorkflowDriver.iwf. You will be presented with a workflow that looks like this:

![alt text](img/WorkflowDriver.png "WorkflowDriver.iwf")

Click on the dprepro node, and in the Settings view, set the "dpreproPath" property to the installation location of Dakota on the remote machine.

## Step 5. Run

Once you have configured your workflow files, you are ready to run the workflow! With LocalWorkflow.iwf open in the editor, click one of the two green play buttons in the toolbar ribbon along the top of the GUI to start the first workflow.

## Step 6. Remote file retrieval

By way of demonstration, we have included "jobId" as an example value that is returned from LoginNodeWorkflow back to LocalWorkflow, using output ports and responses. You can configure an additional number of output ports to send additional information back to your local machine. For example, remote files may be sent back using the "Grab Output File" feature on the remoteNestedWorkflow node. 

To send remote files back to the local machine after the remoteNestedWorkflow has completed execution, right-click the remoteNestedWorkflow node in your LocalWorkflow workflow file, and choose "Grab Output File" from the context menu. You will be presented with the following dialog:

![alt text](img/JobSubmission_NGW_FileRetrieval1.png "'Grab Output File' dialog")

This dialog will allow you to specify the name of the file as well as the name of the remote file (relative to the working directory of remoteNestedWorkflow).

![alt text](img/JobSubmission_NGW_FileRetrieval2.png "Attaching nodes to output ports")

After setting output ports on your remoteNestedWorkflow node, you can do whatever you wish with the returned files.

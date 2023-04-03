# Summary

This example demonstrates how to submit a Dakota job to a remote, non-queued machine using the Dakota GUI (more specifically, using the Next-Gen Workflow tool within Dakota GUI).

# Description

There are generally two types of remote machines that you can submit Dakota jobs to: non-queued machines and queued machines. As the name implies, non-queued machines have no job queues. They are high-performance machines that you can send Dakota jobs to and run the jobs right away.

![alt text](img/JobSubmissionDiagram.png "Example remote job submission")

For a non-queued remote machine, the high-level approach is as follows:

1. Create a workflow that will be run locally on your machine, and will include a **remoteNestedWorkflow** node, which sends a second workflow to the remote machine. The remoteNestedWorkflow node will include configuration for how to connect to the remote machine (the machine name, credentials, etc.)

2. Create a second workflow that will be run on the remote machine. This workflow should perform whatever computation steps are core to your simulation. (In the diagram above, the remote workflow is running Dakota with an NGW analysis driver, so this results in a third workflow, which must also be sent to the remote machine, but this third workflow is not a prerequisite for a functioning remote workflow.)

3. Finally, run the first workflow on your local machine.

For data collection, you should augment the second workflow to send data back to the first.

# Contents

- `cantilever` - the simulation model for the cantilever beam physics problem.
- `cantilever.template` - the templatized input for the cantilever beam.
- `CPS.in` - the Dakota study to be run remotely.
- `LocalWorkflow.iwf` - the first of three workflows, which must be run locally on your machine and is responsible for sending the job to the remote machine.
- `RemoteWorkflow.iwf` - the second of three workflows, which will run on the remote machine. This workflow is responsible for starting Dakota and monitoring Dakota's progress.
- `WorkflowDriver.iwf` - the third, innermost workflow, which acts as Dakota's analysis driver. This analysis driver represents the standard Cantilever beam simulation model used for many Dakota examples.

# How to run the example

## Step 1. Configure LocalWorkflow.iwf

After importing this example into the GUI, double-click LocalWorkflow.iwf. You will be presented with a workflow that looks like this:

![alt text](img/JobSubmission_NGW_Example1_1.png "LocalWorkflow.iwf")

Note that the connections between the file nodes and the remoteNestedWorkflow node are green. Green lines denote that the File Transfer Behavior of the connection is set to "Copy file to target," since the file must be moved from the local machine to the remote machine.

To change the file transfer behavior, simply click on the connection line and see what the "File Transfer Behavior" property is set to in the Settings view for the connection line.

Now, click on the remoteNestedWorkflow node, and adjust its properties in the Settings view:

- Verify that the "fileName" property is set to "RemoteWorkflow.iwf."
- Set the "hostname" property to the name of the remote machine you will be connecting and sending files to.
- Set the "username" property to your username on the remote machine.
- Set the "remotePath" property to the remote destination which you would like to act as your remote directory.
- Set the "wflib" property to the installation location of headless NGW on the remote machine.

## Step 2. Configure RemoteWorkflow.iwf

Now, double-click RemoteWorkflow.iwf. You will be presented with a workflow that looks like this:

![alt text](img/JobSubmission_NGW_Example1_2.png "RemoteWorkflow.iwf")

Click on the dakota node, and in the Settings view, set the "dakotaPath" property to the installation location of Dakota on the remote machine.

## Step 3. Configure WorkflowDriver.iwf

Now, double-click WorkflowDriver.iwf. You will be presented with a workflow that looks like this:

![alt text](img/JobSubmission_NGW_Example1_3.png "WorkflowDriver.iwf")

Click on the dprepro node, and in the Settings view, set the "dpreproPath" property to the installation location of Dakota on the remote machine.

## Step 4. Run

Once you have configured your workflow files, you are ready to run the workflow! With LocalWorkflow.iwf open in the editor, click one of the two green play buttons in the toolbar ribbon along the top of the GUI to start the first workflow.

## Step 5. Remote file retrieval

To send remote files back to the local machine after the remoteNestedWorkflow has completed execuion, you will need to create output ports for each file or folder you want to bring back.

Right-click the remoteNestedWorkflow node and choose "Grab Output File" from the context menu. You will be presented with the following dialog:

![alt text](img/JobSubmission_NGW_FileRetrieval1.png "'Grab Output File' dialog")

This dialog will allow you to specify the name of the file as well as the name of the remote file (relative to the working directory of remoteNestedWorkflow).

![alt text](img/JobSubmission_NGW_FileRetrieval2.png "Attaching nodes to output ports")

After setting output ports on your remoteNestedWorkflow node, you can do whatever you wish with the returned files.

# Troubleshooting Notes

- A presupposition of this workflow is that the server/headless version of Next-Gen Workflow is already installed and available on the remote machine. Talk to your system administrator to ensure that NGW has already been installed on whatever machine you will be submitting your workflow to.
- Login credentials for the remote machine must have already been previously configured. For example, you will not recieve an opportunity to type in your password once the workflow has begun executing. Refer to Window > Preferences > Connection & Login Preferences to set your login credentials.
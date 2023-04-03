#!/bin/bash

if [[ -z "$jobid" ]]; then
  jobid=$(cat dart.id)
fi

checkFilename=slurm-$jobid.out
resultFilename="job.props"

function printResult(){
    if [ $# -eq 0 ] ; then
        return
    fi

    if [ -e $resultFilename ] ; then
        rm $resultFilename
    fi

    line="job.results.status=$1"
    echo "$line" > $resultFilename
    echo $1
}

successString="Dakota Run Finished."
failedString="ERROR"

if [ -e $checkFilename ] ; then
    if (grep -q "$successString" $checkFilename) then
        printResult "Successful"
    else
        if (grep -q "$failedString" $checkFilename) then
            printResult "Failed"
        else
            printResult "Undefined"
        fi
    fi
else
    printResult "Undefined"
fi

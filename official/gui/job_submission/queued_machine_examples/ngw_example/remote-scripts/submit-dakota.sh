#!/bin/bash

cd ${remote.dir}
source /etc/bashrc

echo submitting to the ${queue} queue
sbatch -N ${num.nodes} \
       --partition=${queue} \
       --time=${job.hours}:${job.minutes}:0 \
	   -A ${account} \
       runDakotaRemote.sh \
       2>dart.id.err | tee dart.id.out

exitcode=$?

#
# see if we have the job id in the file, regardless of any exit code from the job submission script
#
AWK=/usr/bin/awk
jobid=$(${AWK} '/^Submitted/ { print $NF; }' dart.id.out)
  
if [[ -n $jobid ]]; then
  
  # we found a job id, so we can put into the expected file
  printf "%s\n" $jobid > dart.id
fi

exit ${exitcode}

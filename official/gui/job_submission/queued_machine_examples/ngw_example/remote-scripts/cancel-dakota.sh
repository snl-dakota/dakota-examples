
if [[ -z "$jobid" ]]; then
  jobid=$(cat dart.id)
fi

scancel $jobid


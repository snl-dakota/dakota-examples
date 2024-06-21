#!/bin/bash

params=$1
results=$2

eval_id=$(grep eval_id $params | awk '{print $1}')
hostname > host-${eval_id}.txt
flux run -n 14 --label-io --output=eval-${eval_id}.out --error=eval-${eval_id}.err ./text_book_par $params temp-$results 
mv temp-$results $results


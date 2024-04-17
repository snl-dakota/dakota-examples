#!/bin/bash

params=$1
results=$2

eval_id=$(grep eval_id $params | awk '{print $1}')
hostname > host-${eval_id}.txt
srun --account=XXXXX --time=00:01:00 --partition=short,batch -N1 -n 14 ./text_book_par $params $results &> text_book-${eval_id}.log
sleep 2

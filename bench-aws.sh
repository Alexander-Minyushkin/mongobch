#!/bin/sh
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 connection_string" >&2
  exit 1
fi

con=$1

#db_host=$(echo $con | awk -F/ '{print $3}' | awk -F@ '{print $2}')

#ping $db_host 

post_num=100000
log_file=logs/aws_atlas_bench_June_01.log

./mongobch.py --connection $con --threads 5 --utt 0.01 --initial_post_num $post_num --label aws-$post_num-5 | tee $log_file
./mongobch.py --connection $con --threads 10 --utt 0.01 --label aws-$post_num-10 | tee -a $log_file
./mongobch.py --connection $con --threads 20 --utt 0.01 --label aws-$post_num-20 | tee -a $log_file
./mongobch.py --connection $con --threads 40 --utt 0.01 --label aws-$post_num-40 | tee -a $log_file


post_num=200000

./mongobch.py --connection $con --threads 5 --utt 0.01 --initial_post_num $post_num --label aws-$post_num-5 | tee -a $log_file
./mongobch.py --connection $con --threads 10 --utt 0.01 --label aws-$post_num-10 | tee -a $log_file
./mongobch.py --connection $con --threads 20 --utt 0.01 --label aws-$post_num-20 | tee -a $log_file
./mongobch.py --connection $con --threads 40 --utt 0.01 --label aws-$post_num-40 | tee -a $log_file


post_num=300000

./mongobch.py --connection $con --threads 5 --utt 0.01 --initial_post_num $post_num --label aws-$post_num-5 | tee -a $log_file
./mongobch.py --connection $con --threads 10 --utt 0.01 --label aws-$post_num-10 | tee -a $log_file
./mongobch.py --connection $con --threads 20 --utt 0.01 --label aws-$post_num-20 | tee -a $log_file
./mongobch.py --connection $con --threads 40 --utt 0.01 --label aws-$post_num-40 | tee -a $log_file

post_num=400000

./mongobch.py --connection $con --threads 5 --utt 0.01 --initial_post_num $post_num --label aws-$post_num-5 | tee -a $log_file
./mongobch.py --connection $con --threads 10 --utt 0.01 --label aws-$post_num-10 | tee -a $log_file
./mongobch.py --connection $con --threads 20 --utt 0.01 --label aws-$post_num-20 | tee -a $log_file
./mongobch.py --connection $con --threads 40 --utt 0.01 --label aws-$post_num-40 | tee -a $log_file

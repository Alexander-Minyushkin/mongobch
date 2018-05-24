#!/bin/sh
if [ "$#" -ne 1 ]; then
  echo "Usage: $0 connection_string" >&2
  exit 1
fi

con=$1

#db_host=$(echo $con | awk -F/ '{print $3}' | awk -F@ '{print $2}')

#ping $db_host 

log_file=logs/aws_atlas_bench.log

./mongobch.py --connection $con --threads 5 --utt 0.01 --initial_post_num 400000 --label aws-400000-5 | tee $log_file
./mongobch.py --connection $con --threads 10 --utt 0.01 --label aws-400000-10 | tee -a $log_file
./mongobch.py --connection $con --threads 20 --utt 0.01 --label aws-400000-20 | tee -a $log_file
./mongobch.py --connection $con --threads 40 --utt 0.01 --label aws-400000-40 | tee -a $log_file
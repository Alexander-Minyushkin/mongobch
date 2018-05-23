
#db_host=$(echo $con | awk -F/ '{print $3}' | awk -F@ '{print $2}')

#ping $db_host 

log_file=logs/aws_atlas_bench.log

python3 mongobch.py --connection $con --threads 5 --utt 0.01 --initial_post_num 1000000 --label aws-1000000-5 > $log_file
python3 mongobch.py --connection $con --threads 10 --utt 0.01 --label aws-1000000-10 >> $log_file
python3 mongobch.py --connection $con --threads 20 --utt 0.01 --label aws-1000000-20 >> $log_file
python3 mongobch.py --connection $con --threads 40 --utt 0.01 --label aws-1000000-40 >> $log_file

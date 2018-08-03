start mongod --dbpath "C:\Program Files\MongoDB\data\db" --cpu --logpath logs/win_local_mongo.log

ping 127.0.0.1

REM mongoimport --type json --db test --collection posts --file dump/1c_1M.json > logs/win_local_import.log & type logs/win_local_import.log

python mongobch.py --connection mongodb://localhost:27017/ --threads 5 --utt 0.01 --initial_post_num 400000 --label windows-400000-5---- --repeat 3 > logs/win_local_bench_400K.log
python mongobch.py --connection mongodb://localhost:27017/ --threads 10 --utt 0.01 --label windows-400000-10---- --repeat 3 >> logs/win_local_bench_400K.log
python mongobch.py --connection mongodb://localhost:27017/ --threads 20 --utt 0.01 --label windows-400000-20---- --repeat 3 >> logs/win_local_bench_400K.log
python mongobch.py --connection mongodb://localhost:27017/ --threads 40 --utt 0.01 --label windows-400000-40---- --repeat 3 >> logs/win_local_bench_400K.log


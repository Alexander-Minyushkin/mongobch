# mongobch
MongoDB benchmark

Simulate implementation of database for social network which allow client to write and read posts, comment, upvote.

Goal is to measure MongoDB performance on different Cloud providers.

## Start
Clone or download sources.
Run `mongobch.py` with options:

```
python mongobch.py --help
Usage: mongobch.py [OPTIONS]



Options:
  --threads INTEGER           Number of threads.
  --utt FLOAT                 User Think Time in seconds.
  --connection TEXT           Connection string.
  --db_name TEXT              Database name.
  --initial_post_num INTEGER  Initial amount of comments to add to DB.
  --ramp_up_sec FLOAT         Ramp up time in seconds.
  --wc_w INTEGER              Write concern "w" Option.
  --wc_j TEXT                 Write concern "j" Option.
  --wc_to INTEGER             Write concern "wtimeout" value.
  --label TEXT                Any text to distinguish test runs.
  --help                      Show this message and exit.

```

For example:
```
python mongobch.py --connection mongodb://localhost:27017/ --threads 5 --utt 0.01 --initial_post_num 1000000 --label windows-1000000-5
```
This command will connect to locally started MongoDB, create 1 million posts at the beginnning, start 5 threads with interval 0.01 sec. between calls.
At the end of the log string label `windows-1000000-5` will be printed.

Output will look like this:
```
Benchmark started.
Connection established
Initial posts added. 362.41374373435974
{'db': 'test_perf', 'collections': 1, 'views': 0, 'objects': 1000000, 'avgObjSize': 1086.0, 'dataSize': 1086000000.0, 'storageSize': 1073594368.0, 'numExtents': 0, 'indexes': 1, 'indexSize': 9617408.0, 'fsUsedSize': 168740970496.0, 'fsTotalSize': 494586032128.0, 'ok': 1.0}
2018-05-16 11:50:10.110057, 0.0, started, Thread-0, windows-1000000-5
2018-05-16 11:50:10.127570, 0.0, started, Thread-1, windows-1000000-5
2018-05-16 11:50:10.130070, 0.0, started, Thread-2, windows-1000000-5
2018-05-16 11:50:10.135573, 0.0, started, Thread-3, windows-1000000-5
2018-05-16 11:50:10.138575, 0.0, started, Thread-4, windows-1000000-5
2018-05-16 11:50:10.125067, 0.07699275016784668, read, Thread-0, windows-1000000-5

2018-05-16 11:50:10.212565, 0.0010006427764892578, read, Thread-0, windows-1000000-5

2018-05-16 11:50:10.224073, 0.0010001659393310547, upvote, Thread-0, windows-1000000-5
```

## Reports
Once you get logs from benchmark you can generate nice reports using R. Take a look at folder `/report`
Plot example
![Response time](/report/resp_time.png)
# mongobch
MongoDB benchmark

Simulate implementation of database for social network which allow client to write and read posts, comment, upvote.

Goal is to measure MongoDB performance on different Cloud providers.

## Start

```
# Setup for Amazon Linux AMI 2018.03.0 (HVM)

sudo yum update -y
sudo yum install git -y
sudo yum install python36 -y

git clone https://github.com/Alexander-Minyushkin/mongobch.git
cd mongobch/
sudo python3 -m pip install -r requirements.txt
```

On any system you need to clone or download sources, install python3.6.
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
  --repeat INTEGER            How many times to repeat scenarios.  
  --label TEXT                Any text to distinguish test runs.
  --help                      Show this message and exit.

```

For example:
```
python mongobch.py --connection mongodb://localhost:27017/ --threads 5 --utt 0.01 --initial_post_num 1000000 --label windows-1000000-5----
```
This command will connect to locally started MongoDB, create 1 million posts at the beginnning, start 5 threads with interval 0.01 sec. between calls.
At the end of the log string label `windows-1000000-5----` will be printed. It is easier to split later using '-' as separator. 
Later, when you add new conditions to benchmark, you can add this information in the label `windows-1000000-5-NewCondition---` and your previosly written parsers will continue to work.

Output will look like this:
```
Benchmark started.
Connection established
Adding initial posts 
Initial posts added, 170.52163410186768
{'db': 'test_perf', 'collections': 1, 'views': 0, 'objects': 400000, 'avgObjSize': 1086.0, 'dataSize': 434400000, 'storageSize': 63455232, 'numExtents': 0, 'indexes': 1, 'indexSize': 3764224, 'fileSize': 0, 'nsSizeMB': 0, 'ok': 1}
2018-05-25 11:49:28.213340, 0.0, started, Thread-0, aws-400000-5

2018-05-25 11:49:28.224761, 0.0, started, Thread-1, aws-400000-5

2018-05-25 11:49:28.237346, 0.0, started, Thread-2, aws-400000-5
```

## Reports
Once you get logs from benchmark you can generate nice reports using R. Take a look at folder `/report`

Plot example, shows that response time depends on number of threads (Windows, local)
![Response time](/report/resp_time.png)
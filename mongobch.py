#!/usr/bin/python3

import click

from socialNetwork import SN_OneCollection
from workloadProfile import UserWorkload, randomText

import threading
import time
from datetime import datetime
from random import randint

@click.command()
@click.option('--threads', default=1, help='Number of threads.')
@click.option('--utt', default=1.0, help='User Think Time in seconds.')
@click.option('--connection', default="", help='Connection string.')
@click.option('--db_name', default="test_perf", help='Database name.')
@click.option('--initial_post_num', default=0, help='Initial amount of comments to add to DB.')
@click.option('--ramp_up_sec', default=0., help='Ramp up time in seconds.')
@click.option('--wc_w', default=1, help='Write concern "w" Option.')
@click.option('--wc_j', default=True, help='Write concern "j" Option.')
@click.option('--wc_to', default=10000, help='Write concern "wtimeout" value.')
@click.option('--label', default="default-label", help='Any text to distinguish test runs.')
def run_perf_test(threads, utt, connection, db_name, initial_post_num, ramp_up_sec, wc_w, wc_j, wc_to, label):
    """
    """

    click.echo("Benchmark started.")

    sn = SN_OneCollection(connection, db_name)
    sn.WriteConcern = { "w": "majority", "j": True, "wtimeout": 1000 }

    click.echo("Connection established")    

    if initial_post_num > 0:
        click.echo(f"Adding initial posts ")
        start = time.time()
        sn.generate_data(initial_post_num)
        elapsed = time.time() - start 

        click.echo(f"Initial posts added, {elapsed}")

    sn.prepare()
    
    print(sn.db.command("dbstats"))

    arr_threads = []
    for i in range(threads):
        sn_ = SN_OneCollection(connection, db_name)
        sn.WriteConcern = { "w": wc_w, "j": wc_j, "wtimeout": wc_to }

        arr_threads.append(UserWorkload(name = f"Thread-{i}", sn = sn_, user_think_time_sec=utt, label = label))
        arr_threads[-1].start()
        if threads > 1:
            time.sleep(ramp_up_sec/(threads - 1))

    for th in arr_threads:
        th.join()

    print(sn.db.command("dbstats"))

if __name__ == '__main__':
    run_perf_test()
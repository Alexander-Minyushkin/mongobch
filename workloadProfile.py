

from socialNetwork import SN_OneCollection, SocialNetwork, randomText

import threading
import time
from datetime import datetime
import bson

from random import sample
import unittest

class SN_Dummy(SocialNetwork):

    post_num = 0
    comment_num = 0
    upvote_num = 0
    read_num = 0

    def post(self, score =0, text=""):
        self.post_num += 1

    def comment(self, text=""):
        self.comment_num += 1

    def upvote(self):
        self.upvote_num += 1

    def read(self):
        self.read_num += 1   

class Test_SN_Dummy(unittest.TestCase):        

    def test_dummy(self):
        sn_dummy = SN_Dummy()

        sn_dummy.post()
        sn_dummy.comment()
        sn_dummy.upvote()
        sn_dummy.read()

        self.assertEqual(sn_dummy.post_num   , 1)
        self.assertEqual(sn_dummy.comment_num, 1)
        self.assertEqual(sn_dummy.upvote_num , 1)
        self.assertEqual(sn_dummy.read_num   , 1)


class UserWorkload(threading.Thread):
    """
    This class imitates user activity in social network. 
    Most operations a reads, fewer upvotes, even more fewer comments, least ones are posts.
    """

    def __init__(self, name, sn, user_think_time_sec=10, label="Any-text-to-distinguish-test-runs", repeat =1):
        threading.Thread.__init__(self, name=name)

        self.user_think_time_sec = user_think_time_sec

        clicks = ["read"]*100 + ["upvote"]*50 + ["comment"]*10 + ["post"]*1
        self.clicks_order = sample(clicks, len(clicks))
        self.click_id = 0

        self.sn = sn

        self.label = label

        self.repeat = repeat

    def run(self):

        timestamp = str(datetime.now())
        print(f'{timestamp}, 0.0, started, 0, {self.getName()}, {self.label}\n')
        
        thread_start = time.time()
        for _ in range(self.repeat):
            for action in self.clicks_order:
                
                rt = randomText()
                timestamp = str(datetime.now())
                info = 0
                elapsed = 0

                start = time.time()            
                if action == "read" : 
                    doc = self.sn.read()
                    elapsed = time.time() - start
                    if doc is not None:
                        info = len(bson.BSON.encode(doc))                    
                elif action == "upvote" : 
                    start = time.time()
                    self.sn.upvote()
                    elapsed = time.time() - start
                elif action == "comment" : 
                    start = time.time()
                    self.sn.comment(text = rt)
                    elapsed = time.time() - start
                elif action == "post" : 
                    start = time.time()
                    self.sn.post(text = rt)  
                    elapsed = time.time() - start                    

                print(f'{timestamp}, {elapsed}, {action}, {info}, {self.getName()}, {self.label}\n') ## \n added at the end to ensure thread-safe prints

                time.sleep(self.user_think_time_sec)
        
        timestamp = str(datetime.now())
        elapsed = time.time() - thread_start
        print(f'{timestamp}, {elapsed}, finished, 0, {self.getName()}, {self.label}\n')           

class Test_UserWorkload(unittest.TestCase): 

    def test_UserWorkload(self):
        sn_dummy = SN_Dummy()
        mythread = UserWorkload(name = "Test_UserWorkload Thread", sn = sn_dummy, user_think_time_sec=0.01) 
        mythread.start()           
        mythread.join()

        self.assertEqual(sn_dummy.post_num   , 1)
        self.assertEqual(sn_dummy.comment_num, 10)
        self.assertEqual(sn_dummy.upvote_num , 50)
        self.assertEqual(sn_dummy.read_num   , 100)

    def test_UserWorkload_with_Repeat(self):
        sn_dummy = SN_Dummy()
        mythread = UserWorkload(name = "Test_UserWorkload Thread", sn = sn_dummy, user_think_time_sec=0.01, repeat = 2) 
        mythread.start()           
        mythread.join()

        self.assertEqual(sn_dummy.post_num   , 1 * 2)
        self.assertEqual(sn_dummy.comment_num, 10 * 2)
        self.assertEqual(sn_dummy.upvote_num , 50 * 2)
        self.assertEqual(sn_dummy.read_num   , 100 * 2)        

        


if __name__ == '__main__':
    pass

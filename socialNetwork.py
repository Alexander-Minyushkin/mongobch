


import pymongo
from pymongo import MongoClient, DESCENDING

import pprint

from random import sample, choices, randint
from math import sqrt, ceil
import string
import unittest

def randomText(n=1024):
    return "".join(choices(string.ascii_lowercase +"      ", k=n))

class SocialNetwork:
    """
    Simulate user activity on somekind of social network.
    Provides interface to post, comment, upvote and read.

    """

    @staticmethod
    def init_db(db_client):
        pass

    @staticmethod
    def clean_db(db_client):
        pass
    
    def sort_favorites(self, count = 100):
        """
        We do not need to choose wisely what to read, upvote etc. 
        Instead we simulate viral nature of social network when users apply most attention to small subset of popular topics.
        But from time to time we need to resort them, to simulate new topics arrival.
        """
        pass

    def post(self, score, text):
        raise NotImplementedError

    def generate_data(self, num):
        """
        To be used for generation of big data volumes
        """
        raise NotImplementedError

    def comment(self, text):
        raise NotImplementedError

    def upvote(self):
        raise NotImplementedError

    def read(self):
        raise NotImplementedError

class SN_OneCollection(SocialNetwork):
    """
    Simplest implementation of SocialNetwork:
    1. All data (posts and comments) are in one collection
    2. No indexes
    3. Write Concern can be reset (https://docs.mongodb.com/manual/reference/write-concern/)    
    """

    favorites_id = []  ## This is list of most popular posts which will be read, commented and upvoted further

    def __init__(self, connection_string, db_name):
        self.db = MongoClient(connection_string)[db_name]
        self._WriteConcern = { "w": 1, "j": True, "wtimeout": 10000 }
    
    def sort_favorites(self, count = 1000):
        SN_OneCollection.favorites_id = []

        for doc in self.db.posts.find({}, {"_id": 1}).sort("score", DESCENDING).limit(count):
            SN_OneCollection.favorites_id.append(doc)

    def prepare(self):    
        self.sort_favorites()
        # index creation to go here    

    @property
    def WriteConcern(self):
        return self._WriteConcern

    @WriteConcern.setter
    def WriteConcern(self, wc):
        self._WriteConcern = wc

    def get_doc_id_for_update(self):
        if len(SN_OneCollection.favorites_id) == 0 :
            self.sort_favorites()

        id = sample(SN_OneCollection.favorites_id, 1)[0]
        
        return id


    def post(self, score = 0, text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."):
        self.db.posts.insert_one({
            "content": text,
            "score": score,
            "comments": [],
            })

    def _inflate_to(self, M, max_string_len=len(randomText())):
        """
        Make full join of posts to posts and (not very) randomly combine content.
        This will create more different 'words' for future experiments with indexes and text search.
        """

        N = ceil(sqrt(M))
            
        limit = {"$limit": N}
        
        lookup = {
            "$lookup":{
                "from": "posts",
                "localField": "score",
                "foreignField": "score",
                "as": "joined"
            }
        }

        unwinding = {
            "$unwind":
            {
            "path": "$joined"
            }

        }
        
        split = randint(0, max_string_len-1)

        project = {
                '$project': {
                    '_id':0,
                    'score': 1,
                    'comments': 1,
                    'content': { '$concat': [ { '$substr': [ '$content', 0, split ] }, 
                                            { '$substr': [ '$joined.content' , split,  max_string_len-split] }] 
                            }
                }
        }
        
        self.db.posts.aggregate([limit, lookup, unwinding, project, {'$limit': M}, { '$out' : "posts" }])

    def generate_data(self, num):
        """
        Used for initial data generation.
        """
        
        self.db.posts.insert_many([{
            "content": randomText(),
            "score": 1, # this need to be constant for self._inflate_to() to work properly
            "comments": [],
            } for _ in range(min(100, num))]) ## Insert up to 100 initial posts

        ## Inflate exponentially until required number of posts
        while(self.db.command("collstats", "posts")['count'] < num):            
            self._inflate_to(num)

        self.sort_favorites()

            

    def comment(self, text = "What is it? Twitter for ants?"):
        doc_id = self.get_doc_id_for_update() 

        self.db.posts.update_one( doc_id, {"$push":{"comments": text}})

    def upvote(self):
        doc_id = self.get_doc_id_for_update() 

        self.db.posts.update_one( doc_id, {"$inc":{"score":1}})
        #raise NotImplementedError

    def read(self):
        doc_id = self.get_doc_id_for_update()        
        
        return self.db.posts.find_one(doc_id)

class Test_SN_OneCollection(unittest.TestCase):

    connection_string = "mongodb://localhost:27017/"

    @classmethod
    def tearDownClass(cls):
        sn = SN_OneCollection(cls.connection_string, "test")
        sn.db.posts.drop()

    def test_post(self):
        sn = SN_OneCollection(self.connection_string, "test")

        sn.post()

        count_before = sn.db.command("collstats", "posts")['count'] 
        sn.post()
        count_after = sn.db.command("collstats", "posts")['count'] 

        self.assertEqual( count_after - count_before, 1)


    def test_generate_data(self):
        sn = SN_OneCollection(self.connection_string, "test")
        
        sn.db.posts.drop()
        sn.generate_data(1111) # Important - number should not be equal to batch_size
        count_after = sn.db.command("collstats", "posts")['count'] 

        self.assertEqual( count_after, 1111)


    def test_read(self):
        sn = SN_OneCollection(self.connection_string, "test")

        sn.post()

        self.assertTrue( len(sn.read()) > 0)


    def test_upvote(self):
        sn = SN_OneCollection(self.connection_string, "test")

        sn.post()

        pipeline = [
            {
                "$group": {
                    "_id": "total",
                    "score_count": { "$sum": "$score" }       
                }
            }
        ]
        count_before = list(sn.db.posts.aggregate(pipeline))[0]['score_count']
        sn.upvote()
        count_after = list(sn.db.posts.aggregate(pipeline))[0]['score_count']

        self.assertEqual( count_after - count_before, 1)   

    def test_comment(self):
        sn = SN_OneCollection(self.connection_string, "test")

        sn.post()

        pipeline = [
            {
                "$group": {
                    "_id": "total",
                    "comments_count": { "$sum": { "$size": "$comments" } }       
                }
            }
        ]
        count_before = list(sn.db.posts.aggregate(pipeline))[0]['comments_count']
        sn.comment()
        count_after = list(sn.db.posts.aggregate(pipeline))[0]['comments_count']

        self.assertEqual( count_after - count_before, 1)  

    def test_WriteConcernReset(self):
        sn = SN_OneCollection(self.connection_string, "test")

        wc = sn.WriteConcern

        wc_new = {}

        wc_new["j"] = not wc["j"]
        wc_new["w"] = 1 - wc["w"]
        wc_new["wtimeout"] = wc["wtimeout"] + 1

        sn.WriteConcern = wc_new

        self.assertNotEqual(wc["j"], sn.WriteConcern["j"])
        self.assertNotEqual(wc["w"], sn.WriteConcern["w"])
        self.assertNotEqual(wc["wtimeout"], sn.WriteConcern["wtimeout"])





# to run unit tests:
# python -m unittest socialNetwork.py

if __name__ == "__main__":

    #unittest.main()

    #connection_string = "mongodb://localhost:27017/"
    #sn = SN_OneCollection(connection_string, "test")
    #sn.comment()

    pass
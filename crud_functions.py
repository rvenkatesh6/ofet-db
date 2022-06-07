import pandas as pd
import numpy as np
from pymongo import MongoClient
import json
from bson.objectid import ObjectId
import functools


def connect_mongo(uri, db): #this does not take the collection as an arg, since DPP-DTT and P3HT, etc. may be in separate collections
    """ A util for making a connection to mongo """

    conn = MongoClient(uri)
    
    return conn[db]

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.nan):
            return None
        return super(NpEncoder, self).default(obj)


def read_mongo_docs(uri, db, collection, query={}, proj={}):
    """ Read from Mongo and Store into DataFrame, and return all the documents as a dict """

    # Connect to MongoDB
    mydb = connect_mongo(uri=uri, db=db)
    col = mydb[collection]
    # Make a query to the specific DB and Collection
    cursor = col.find(query, proj)

    # Expand the cursor
    docs =  list(cursor)

    return docs

#### INSERTS ####
def csv_convert(fname, template="literature"):
    """ Inputs a file, output a json formatted dict"""
    if template=="literature":

        mydict = {}

        return mydict

    return mydict 

def insert_mongo(uri, db, collection):
    """ Input is a dict, function inserts into database"""
    return


def row_to_json(a):
    
    """Takes a Series object as an input, with columns in dot notation according to 
    ofetdb schema, converts to a json formatted dict. Must use Excel literature/expt template with dot notation"""

    output = {}
    for key, value in a.iteritems():
        if pd.isnull(value) == False: #Only add key:value if not empty in the json
            path = key.split('.')
            target = functools.reduce(lambda d, k: d.setdefault(k, {}), path[:-1], output)
            target[path[-1]] = value
    return output
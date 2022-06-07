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

def get_persson_dataset_dict(sample_row):
    """ Input is a 1-D df object, which is one row; column info is preserved from
    Persson et al (2016) with column names modified"""
     
    sample_dict = {
        "_id": ObjectId(sample_row._id),
        "solution": {
            "solvent": 
                {
                "name": sample_row.solvent_name,
                "boiling_point_C": sample_row.solvent_bp_C
                },
            "polymer": {
                "semiconductor":
                    {
                        "name": "P3HT",
                        "Mn_kDa": sample_row.Mn_kDa,
                        "Mw_kDa": sample_row.Mw_kDa,
                        "PDI": sample_row.PDI,
                        "RR": sample_row.RR
                    }
            },
            "concentration_mg_ml": sample_row.solution_concentration_mg_ml,
            "treatment": {
                "age": {
                    "time_hr": sample_row.age_time_hr,
                    "temp_C": sample_row.age_temp_c
                },
                "poorsolvent":{
                    "name": sample_row.poor_solvent_name,
                    "vfrac": 1-sample_row.solvent1_VF
                }
            },
            "hansen_radius": sample_row.hansen_radius
        },
        
        "film": {
            "thickness_nm": sample_row.film_thickness_nm
        },

        "ofet": {
            "mobility_cm2_Vs": sample_row.mobility_cm2_Vs,
            "regime": sample_row.mobility_regime,
            "environment": sample_row.mobility_environment,
            "Vds_V": sample_row.Vds_V
        },   
        
        "substrate": {
            "gate_material": "Si",
            "dielectric_material": "SiO2",
            "electrode_config": sample_row.electrode_config,
            "electrode_material": sample_row.electrode_material,
            "channel_length_um": sample_row.channel_length_um,
            "channel_width_mm": sample_row.channel_width_mm,
            "surface_modification": sample_row.substrate_surface_treatment
        },
        
        "coating_process": {
            "deposition_method": sample_row.deposition_method,
            "spin_rate_rpm": sample_row.spin_rate_rpm,
            "spin_time_s": sample_row.spin_time_s,
            "coating_speed_mm_s": sample_row.dip_rate_mm_min/60,
            "coating_environment": sample_row.process_environment,
            "annealing": {
                "time_hr": sample_row.anneal_time_hr,
                "temp_C": sample_row.anneal_temp_c
            }
        },
        
        "literature": {
            "author": sample_row.Author,
            "year": sample_row.Year,
            "DOI": sample_row.DOI
        }        
        
        
    }
    
    return sample_dict


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
# %%
import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np
import plotly.express as px

uri = "mongodb+srv://aliu319:LO9UfXxBfDEPPfcQ@aliu319-gt.t7rt0.mongodb.net/test?retryWrites=true&w=majority"
db = "ofet-db"
collection = "devices"

def _connect_mongo(uri, db):
    """ A util for making a connection to mongo """

    conn = MongoClient(uri)
    return conn[db]

def read_mongo(uri, db, collection, query={}, proj={}):
    """ Read from Mongo and Store into DataFrame """

    # Connect to MongoDB
    db = _connect_mongo(uri=uri, db=db)

    # Make a query to the specific DB and Collection
    cursor = db[collection].find(query, proj)

    # Expand the cursor and construct the DataFrame
    docs =  list(cursor)
    df_flat = pd.json_normalize(docs)
    # Delete the _id
    # if no_id:
        # del df['_id']

    return df_flat

# %%

q1 = {}
proj = {
    "_id": False, 
    "ofet.mobility_cm2_Vs": True, 
    "solution.concentration_mg_ml": True, 
    "solution.solvent.solvent_name": True,
    "substrate.surface_modification": True,
    "solution.polymer": True,
    "coating_process.deposition_method": True
}   

df_1 = read_mongo(uri, db, collection, q1, proj)
print(df_1)

# q2 = '''
#     SELECT polymer_name, mw_kda, COUNT(*) FROM device, solution, polymer
#     WHERE device.solution_id = solution.solution_id
#     AND solution.polymer_id = polymer.polymer_id
#     GROUP BY polymer_name, mw_kda;
#     '''        

# df_2 = read_select_query(q2)

# # q3 = '''
# #     SELECT polymer_name, solvent.solvent_name, boiling_point_c, min(concentration_mgml)	
# #         AS min_concentration, max(concentration_mgml) AS max_concentration, count(*) AS num_expts
# #     FROM device, solution, solvent, polymer
# #     WHERE device.solution_id = solution.solution_id AND
# #     solution.solvent_name = solvent.solvent_name AND
# #     solution.polymer_id = polymer.polymer_id
# #     GROUP BY solvent.solvent_name, polymer_name
# #     ORDER BY polymer_name
# #     '''     

# # df_3 = read_select_query(q3)

# def q3_mod(polymer_name):
#     query = '''
#     SELECT solvent.solvent_name, boiling_point_c, min(concentration_mgml)	
#         AS min_concentration, max(concentration_mgml) AS max_concentration, count(*) AS num_expts
#     FROM device, solution, solvent, polymer
#     WHERE device.solution_id = solution.solution_id AND
#     solution.solvent_name = solvent.solvent_name AND
#     solution.polymer_id = polymer.polymer_id AND
#     polymer.polymer_name = '%s'
#     GROUP BY solvent.solvent_name, polymer_name
#     ORDER BY polymer_name
#     ''' % polymer_name

#     df_3 = read_select_query(query)

#     return df_3

# q4 = '''
#     SELECT polymer_name, mobility_cm2_vs, deposition_method 
#     FROM device, solution, polymer, coating_process
#     WHERE device.coating_id = coating_process.coating_id AND 
#     device.solution_id = solution.solution_id AND 
#     solution.polymer_id = polymer.polymer_id;
#     '''

# df_4 = read_select_query(q4)

# print("Success")

# # cur = conn.cursor()


# # conn.commit()
# # print("Operation successful")
# # conn.close()
# # %%
# fig4 = px.box(df_4, 
#     x="deposition_method", 
#     y="mobility_cm2_vs", 
#     color="polymer_name", 
#     points="all",
#     log_y=True
#     )
# fig4.show()
# %%

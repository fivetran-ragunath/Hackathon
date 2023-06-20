from fields import *  
import sys 

source_data = json.load(open("postman_collection.json"))
for key,value in source_data.items():
    if key == 'item':
        entire_json = value  
with open("output.clj", "w") as f:
    sys.stdout = f 
    for row in entire_json:
        for key,value in row.items():
            if key == 'response' and value != []:
                test = testing(row)
                test.iter_every_entity()
                test.entity_source()
                test.extract_path()
                # test.incremental_sync()          
                test.field()
                test.surrogation()
                test.dynamic_field()
                test.flatten_field()
                test.relate()
                test.foreign_relation()
                test.breakout_table() 
    
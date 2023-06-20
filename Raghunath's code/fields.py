import json  
import pandas as pd 

def flatten(keys,values):
    final_col = final.columns
    print('(flatten-fields\n(fields')
    for key,value in values.items(): 
        if value == {}:
            print('\t',key,'\t\t(json)') 
        else:
            print('\t',key)
    for col in final_col:
        is_list = final[col].apply(lambda x: isinstance(x, list)).all()
        if is_list == False and len(col.split('.')) > 1 and col.split('.')[-1] == keys :  
            keys = col.replace('.','/')
    print('):from',keys,')')

def breakout_fields(parent,col):
    data = pd.json_normalize(parent[str(col)][0]) 
    data_col = data.columns  
    print('(fields') 
    for col in data_col:
        is_list = data[col].apply(lambda x: isinstance(x, list)).all()
        if is_list == False and len(col.split('.')) == 1 and col != 'id':
            print(col)
        elif is_list == False and len(col.split('.')) == 1 and col == 'id':
            print(col,'\t\t:id')
        elif is_list == False and len(col.split('.')) > 1 :
            print(col.lower().replace('.','_'),'\t:<=\t"'+col+'"')
    print(')')

def breakout_relation(parent,col):
    data = pd.json_normalize(parent[str(col)][0]) 
    data_col = data.columns
    for col in data_col:
        is_list = data[col].apply(lambda x: isinstance(x, list)).all()
        if is_list == False and len(col.split('.')) == 1 and len(col) > 2 and col[-2:] == 'id' and col[-3:] != '_id' and col[-3:] != '_Id' or col[-2:] == 'Id':
            print('\t(links-to '+col[:-2].upper(),':prop '+'"'+col+'")')
        elif is_list == False and len(col.split('.')) == 1 and len(col) > 3 and col[-3:] == '_id' or col[-3:] == '_Id':
            print('\t(links-to '+col[:-3].upper(),':prop '+'"'+col+'")')
        elif is_list == False and len(col.split('.')) == 2 and col.split('.')[1] == 'id':
            print('\t(links-to '+col.split('.')[0].upper(),':prop '+'"'+col.split('.')[0]+'_'+col.split('.')[1]+'")')  
    print('))')

class testing():

    def __init__(self,entire_json):
        self.entire_json = entire_json 

    def iter_every_entity(self): 
        global request_json
        global response_json
        global raw_output
        global target
        for key,value in self.entire_json.items():
            if key == 'request':
                request_json = value
            elif key == 'response' and value != []:
                response_json = value[0]
                for keys,values in response_json.items():
                    if keys == 'body' and values != None :
                        raw = values
                        raw_output = json.loads(values) 
                    elif keys == 'body' and values == None : 
                        raw_output = {"oops!!! got empty response to this entity in postman collection example!" : "info"}
            else : 
                response_json = None
            
        path_list = ['items','result','results','item','items','value','values','data','segments','sessions','elementBlocks','contacts','people','organizations','fields','keywords','articles','documents','privateDocuments','next_states','customDataFieldDefintions','modules','learner_resources','user','group_manager','dashboard_lists','dashboards','events','indexes','orgs','host_list','embedded_graphs','accounts','courseAssignments','Resources']
        data = pd.json_normalize(response_json)
        path_lists = data['originalRequest.url.path'][0]
        # if type(raw_output) == dict and raw_output != {}:
        #     for key,value in raw_output.items():
        #         if key in path_list and value != [] and type(value) == list :
        #             target = value[0]
        #         elif key in path_lists and value != [] and type(value) == list:
        #             target = value[0]
        #         elif key not in path_list or key != path_lists and value != {} and type(value) == dict :
        #             target = raw_output
        # print(raw_output)
        array_count = 0  
        global target
        if type(raw_output) == list and raw_output != []:
            target = raw_output[0]
        elif type(raw_output) == dict and raw_output != {} :
            for key,value in raw_output.items() : 
                if isinstance(value, list):
                    array_count = array_count + 1
                    if array_count == 1 :
                        target_data = value[0]
                    elif array_count == 0 or array_count > 1:
                        target_data = raw_output 
        if type(raw_output) == dict and raw_output != {} and array_count == 1 :
            target = target_data
        elif type(raw_output) == dict and raw_output != {} and array_count == 0 or array_count > 1:
            target = raw_output 
   
    def entity_source(self):   
        print('\n(entity '+list(self.entire_json.items())[0][1].upper(),'\n\t(api-docs-url "docs_link")')
        entity_url = ''
        data = pd.json_normalize(self.entire_json) 
        data_cols = data.columns 
        method = data['request.method'][0]
        split_url = str(data['request.url.raw'][0]).split('/') 
        for url in split_url[split_url.index(data['request.url.path'][0][0]):]: 
            entity_url = entity_url + url + '/'
        print('\t(source(http/'+method.lower(),':url "/'+entity_url[:-1]+'"')
        encoded_body_request = pd.json_normalize(response_json)
        encoded_columns = encoded_body_request.columns
        if 'request.body.raw' in data_cols and not {}:
            print('\t(body-param-format "application/json")\n\t(body-params',data['request.body.raw'][0].replace(':',''),')')
        elif 'originalRequest.body.urlencoded' in encoded_columns :
            print('\t(body-param-format "application/x-www-form-urlencoded")\n\t(body-params')
            encoded_data = encoded_body_request['originalRequest.body.urlencoded'][0]
            encoded_key = ''
            encoded_value = ''
            for i in encoded_data :
                for key,value in i.items():
                    if key == 'key':
                        encoded_key = value
                    elif key == 'value':
                        encoded_value = value
                        print('\t\t\t"'+encoded_key+'"','"'+encoded_value+'"')
            print(')')
        print(')')

    def extract_path(self): 
        path_list = ['items','result','results','item','value','values','data','versions']
        data = pd.json_normalize(response_json)
        path_lists = data['originalRequest.url.path'][0]
        extract_path = ''
        if type(raw_output) == dict and raw_output != {}:
            for key,value in raw_output.items():
                if key in path_list or key in path_lists:
                    extract_path = key
        elif type(raw_output) == list and raw_output != []:
            extract_path = ''
        print('(extract-path "'+extract_path+'"))')

    def field(self):
        global final
        final = pd.json_normalize(target) 
        final_col = final.columns 
        end = True
        print('(fields')
        for col in final_col:
            is_list = final[col].apply(lambda x: isinstance(x, list)).all()
            if is_list == False and len(col.split('.')) == 1 and col != 'id':
                print('\t',col)
            elif is_list == False and len(col.split('.')) == 1 and col == 'id':
                print('\t',col,'\t\t:id')
            elif is_list == True and  final[str(col)][0] == [] and len(col.split('.')) == 1:
                print('\t',col,'\t\t(json)')
            elif is_list == True and  final[str(col)][0] == [] and len(col.split('.')) > 1:
                print('\t',col.replace('.','_'),'\t:<=\t\t"'+col+'"','\t\t(json)')
            elif is_list == False and  col == {} and len(col.split('.')) == 1:
                print('\t',col,'\t\t(json)')
            elif is_list == False and col == {} and len(col.split('.')) > 1:
                print('\t',col.replace('.','_'),'\t"'+col+'"','\t\t(json)')
        print(')')

    def surrogation(self):
        final = pd.json_normalize(target)
        final_col = final.columns
        for col in final_col:
            if col != 'id' and col != 'name' and col[-5:] == 'number' and len(col.split('.')) < 1:
                print('(dynamic-fields(fivetran-id))')

    def dynamic_field(self):
        final = pd.json_normalize(target)
        final_col = final.columns
        global dynamical 
        dynamical = 0
        for col in final_col:
            is_list = final[col].apply(lambda x: isinstance(x, list)).all()
            if is_list == False and len(col.split('.')) > 1:
                dynamical = dynamical + 1
        if dynamical != 0:
            print('(dynamic-fields')
    
    def flatten_field(self):
        ending = True
        final = pd.json_normalize(target)
        final_col = final.columns
        for key,value in target.items():
            if type(value) == dict and value != {}:
                flatten(key,value)
                for key_1,value_1 in value.items():
                    if type(value_1) == dict and value_1 != {}:
                        flatten(key_1,value_1)
                        for key_2,value_2 in value_1.items():
                            if type(value_2) == dict and value_2 != {}:
                                flatten(key_2,value_2)
                                for key_3,value_3 in value_2.items():
                                    if type(value_3) == dict and value_3 != {}:
                                        flatten(key_3,value_3) 
        if dynamical != 0:
            print(')') 
        for col in final_col:
            is_list = final[col].apply(lambda x: isinstance(x, list)).all()  
            if is_list == True and final[str(col)][0] != []:
                ending = False
            if len(col) > 2 and col[-2:] == 'id':
                ending = False
        if ending == True :
            print(')') 
    
    def incremental_sync(self):
        final = pd.json_normalize(response_json)
        final_col = final.columns
        query_start = ['fr','st','mo','si','up']
        query_end = ['to','nd']
        query_sort = ['or','so']
        query_params = ''
        count = 0
        start_param = ''
        end_param = ''
        if 'originalRequest.url.query' in final_col:
            query_params = final['originalRequest.url.query']
            for i in range(len(query_params[0])):
                for key,value in query_params[0][i].items():
                    if value[:2] in query_start:
                        start_param = value
                        count = count + 1
                    elif value[-2:] in query_end:
                        end_param = value
                        count = count + 1 
            if count == 1:
                print('(sync-plan\n(change-capture-cursor\n\t\t(subset/by-time (query-params "'+start_param+'" "$FROM")\n\t\t(format "epoch-sec"))))')
            elif count == 2:
                print('(sync-plan\n(change-capture-cursor\n\t\t(subset/by-time (query-params "'+start_param+'" "$FROM" "'+end_param+'" "$TO")\n\t\t(format "epoch-sec"))))')  
            
    def relate(self):
        final = pd.json_normalize(target)
        final_col = final.columns
        global relation 
        relation = False
        for col in final_col:
            is_list = final[col].apply(lambda x: isinstance(x, list)).all()
            if is_list == False  and len(col) > 2 and col[-2:] == 'id' and col[-3:] != '_id' or col[-2:] == 'Id':
                relation = True
            elif is_list == True and final[str(col)][0] != []:
                relation = True
        if relation == True:
            print('(relate')

    def foreign_relation(self):
        final = pd.json_normalize(target)
        final_col = final.columns
        for col in final_col:
            is_list = final[col].apply(lambda x: isinstance(x, list)).all()
            if is_list == False and len(col.split('.')) == 1 and len(col) > 2 and col[-2:] == 'id' and col[-3:] != '_id' and col[-3:] != '_Id' or col[-2:] == 'Id':
                print('(links-to '+col[:-2].upper(),':prop '+'"'+col+'")')
            elif is_list == False and len(col.split('.')) == 1 and len(col) > 3 and col[-3:] == '_id' or col[-3:] == '_Id':
                print('(links-to '+col[:-3].upper(),':prop '+'"'+col+'")')
            elif is_list == False and len(col.split('.')) == 2 and col.split('.')[1] == 'id':
                print('(links-to '+col.split('.')[0].upper(),':prop '+'"'+col.split('.')[0]+'_'+col.split('.')[1]+'")')
            elif is_list == True and len(col.split('.')) < 2 and final[str(col)][0] != [] and type(final[str(col)][0][0]) == dict:
                print('(contains-list-of',list(response_json.items())[0][1].upper()+'_'+col.upper().replace('.','_'),':inside-prop '+'"'+col.replace('.','/')+'")')
            elif is_list == True and len(col.split('.')) >= 2 and final[str(col)][0] != [] and type(final[str(col)][0][0]) == dict:
                print('(contains-list-of',list(response_json.items())[0][1].upper()+'_'+col.upper().split('.')[-1],':inside-prop '+'"'+col.replace('.','/')+'")')
            elif is_list == True and final[str(col)][0] != [] and type(final[str(col)][0][0]) == str:
                print('(contains-list-of',list(response_json.items())[0][1].upper()+'_'+col.upper().split('.')[-1],':inside-prop '+'"'+col.replace('.','/')+'" :as',col.lower().split('.')[-1],')')
        if relation == True:
            print('))') 

    def breakout_table(self):  
        first_breakout = pd.json_normalize(target) 
        first_breakout_cols = first_breakout.columns
        for col in first_breakout_cols: 
            is_list = first_breakout[col].apply(lambda x: isinstance(x, list)).all()
            if is_list == True and first_breakout[str(col)][0] != [] and type(first_breakout[str(col)][0][0]) == dict:
                print('\n(entity '+list(self.entire_json.items())[0][1].upper()+'_'+col.upper().split('.')[-1],'\n\t(api-docs-url "docs_link")')                    #first_breakout_table
                breakout_fields(first_breakout,col)  
                print('(relate\n\t (includes',list(self.entire_json.items())[0][1].upper(),':prop "id" )')
                breakout_relation(first_breakout,col)
                second_breakout = pd.json_normalize(first_breakout[str(col)][0]) 
                second_breakout_col = second_breakout.columns 
                for cols in second_breakout_col:
                    is_list = second_breakout[cols].apply(lambda x: isinstance(x, list)).all()
                    if is_list == True and second_breakout[str(cols)][0] != [] and type(second_breakout[str(cols)][0][0]) == dict:
                        print('\n(entity '+list(self.entire_json.items())[0][1].upper()+'_'+col.upper().split('.')[-1] + '_' + cols.upper().split('.')[-1],'\n\t(api-docs-url "docs_link")')  #second_breakout_table
                        breakout_fields(second_breakout,cols)  
                        print('(relate\n\t (includes',list(self.entire_json.items())[0][1].upper()+'_'+col.upper(),':prop "'+list(self.entire_json.items())[0][1]+'_id" ) \n\t (includes',list(self.entire_json.items())[0][1].upper()+'_'+col.upper(),':prop "id" )')
                        breakout_relation(second_breakout,cols)
                        third_breakout = pd.json_normalize(second_breakout[str(cols)][0])
                        third_breakout_col = third_breakout.columns
                        for column in third_breakout_col:
                            is_list = third_breakout[column].apply(lambda x: isinstance(x, list)).all()
                            if is_list == True and third_breakout[str(column)][0] != [] and type(third_breakout[str(column)][0][0]) == dict:
                                print('\n(entity '+list(self.entire_json.items())[0][1].upper()+'_'+column.upper().split('.')[-1] + '_' + column.upper().split('.')[-1],'\n\t(api-docs-url "docs_link")')  #third_breakout_table
                                breakout_fields(third_breakout,column)  
                                print('(relate\n\t (includes',list(self.entire_json.items())[0][1].upper()+'_'+col.upper()+'_'+cols.upper(),':prop "'+list(self.entire_json.items())[0][1].upper()+'_id" )\n\t (includes',list(self.entire_json.items())[0][1].upper()+'_'+col.upper()+'_'+cols.upper(),':prop "'+cols.upper()+'_id" ) \n\t (includes',list(self.entire_json.items())[0][1].upper()+'_'+col.upper()+'_'+cols.upper(),':prop "id" )')
                                breakout_relation(third_breakout,column)
                            elif is_list == True and third_breakout[str(column)][0] != [] and type(third_breakout[str(column)][0][0]) != dict and type(third_breakout[str(column)][0][0]) == str:
                                print('\n(entity '+list(self.entire_json.items())[0][1].upper()+'_'+column.upper().split('.')[-1],'\n\t(api-docs-url "docs_link")')
                                print('(fields\n\t',column.lower().split('.')[-1],'\n\t index \t\t :id \t\t :index)')
                                print('(relate\n\t (includes',cols.upper(),':prop "'+list(self.entire_json.items())[0][1]+'_id" ) \n\t (includes',cols.upper(),':prop "id" )')
                                if column.lower().split('.')[-1][-2:] == 'id':
                                    print('(links-to',column.upper().split('.')[:-2],':prop "id")')
                                elif column.lower().split('.')[-1][-3:] == '_id' or column.lower().split('.')[-1][-3:] == 'ids':
                                    print('(links-to',column.upper().split('.')[:-3],':prop "id")')
                                elif column.lower().split('.')[-1][-4:] == '_ids':
                                    print('(links-to',column.upper().split('.')[:-4],':prop "id")')
                                else:
                                    print(')')
                    elif is_list == True and second_breakout[str(cols)][0] != [] and type(second_breakout[str(cols)][0][0]) != dict and type(second_breakout[str(cols)][0][0]) == str:
                        print('\n(entity '+list(self.entire_json.items())[0][1].upper()+'_'+col.upper().split('.')[-1],'\n\t(api-docs-url "docs_link")')
                        print('(fields\n\t',col.lower().split('.')[-1],'\n\t index \t\t :id \t\t :index)')
                        print('(relate\n\t (includes',col.upper(),':prop "'+list(self.entire_json.items())[0][1]+'_id" ) \n\t (includes',col.upper(),':prop "id" )')
                        if cols.lower().split('.')[-1][-2:] == 'id':
                            print('(links-to',cols.upper().split('.')[:-2],':prop "id")')
                        elif cols.lower().split('.')[-1][-3:] == '_id' or cols.lower().split('.')[-1][-3:] == 'ids':
                            print('(links-to',cols.upper().split('.')[:-3],':prop "id")')
                        elif cols.lower().split('.')[-1][-4:] == '_ids':
                            print('(links-to',cols.upper().split('.')[:-4],':prop "id")')
                        else:
                            print(')')
            elif is_list == True and first_breakout[str(col)][0] != [] and type(first_breakout[str(col)][0][0]) != dict:
                print('\n(entity '+list(self.entire_json.items())[0][1].upper()+'_'+col.upper().split('.')[-1],'\n\t(api-docs-url "docs_link")')
                print('(fields\n\t',col.lower().split('.')[-1],'\n\t index \t\t :id \t\t :index)')
                print('(relate\n\t(needs',list(self.entire_json.items())[0][1].upper(),':prop "id" ))')
                if col.lower().split('.')[-1][-2:] == 'id':
                    print('(links-to',col.upper().split('.')[:-2],':prop "id")')
                elif col.lower().split('.')[-1][-3:] == '_id' or col.lower().split('.')[-1][-3:] == 'ids':
                    print('(links-to',col.upper().split('.')[:-3],':prop "id")')
                elif col.lower().split('.')[-1][-4:] == '_ids':
                    print('(links-to',col.upper().split('.')[:-4],':prop "id")')
                else:
                    print(')')

# import sys 
# source_data = json.load(open("postman_collection.json"))
# for key,value in source_data.items():
#     if key == 'item':
#         entire_json = value  
# with open("output.clj", "w") as f:
#     sys.stdout = f 
#     for row in entire_json:
#         for key,value in row.items():
#             if key == 'response' and value != []:
#                 test = testing(row)
#                 test.iter_every_entity()
#                 test.entity_source()
#                 test.extract_path()
#                 # test.incremental_sync()          
#                 test.field()
#                 test.surrogation()
#                 test.dynamic_field()
#                 test.flatten_field()
#                 test.relate()
#                 test.foreign_relation()
#                 test.breakout_table() 

 
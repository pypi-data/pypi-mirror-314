import easy_db 
from ..utils import path_maker
from ..debug import Debug

class DB:
    def __init__(self,tables={},name = 'database',relative_path='.',debug_mode = True,debug_relative_path = '.',path=None) -> None:
        '''
            tables={'table_name':{id:0}}
        '''
        if path==None:
            self.path = path_maker([],relative_path=relative_path)+f'/{name}.db'
        else:
            self.path =path
        self.db = easy_db.DataBase(self.path, create_if_none=True)
        self.init_tables(tables)
        self.debug = Debug(debug_mode=debug_mode,relative_path=debug_relative_path)

    def init_tables(self,tables):
        # self.db.
        if tables:
            table_names = set(self.db.table_names())
            for table_name in tables:
                if table_name not in table_names:
                    self.db.create_table(table_name, self.convert_value_to_type(tables[table_name].copy()))
                else:
                    key_columns = set(self.db.columns_and_types(tablename = table_name).keys())
                    base_key_columns = set(tables[table_name].keys())
                    for new_col_name in base_key_columns - key_columns:
                        self.db.add_column(table_name,new_col_name,type(tables[table_name][new_col_name]).__name__)
            # table_names = set(sorted(self.db.table_names()))
            # for i in list(table_names -set(tables.keys())):
            #     print(i)
            #     self.db.drop_table(i)
    
    def do(self,table,keys_values=None,condition=None,delete=False):
        '''
            condition:                 must be str
            keys_values :              must be dict or list
            return all data:           keys_values=None,condition=None
            return data by condition : condition= sql str condition
            insert data:               dict or list and condition= None
            update data:               keys_values= dict data and condition= sql str condition

        
        '''
        if not delete:
            if type(keys_values)==type(None):
                if type(condition)==type(None):return self.db.pull(table,fresh=True)
                else:return self.db.pull_where(table,condition)

            else:
                if type(condition)==type(None):
                    if isinstance(keys_values,list):
                        self.db.append(table,keys_values)
                    elif isinstance(keys_values,dict):
                        self.db.append(table,[keys_values])

                else:
                    res = self.db.pull_where(table,condition)
                    if len(res) > 0:
                        col,val = condition.split('=')
                        col=col.strip(' ')
                        val=val.strip(' ')
                        val = val.replace('"','').replace("'",'')
                        for i in keys_values:
                            self.db.update(table, col,val, i, keys_values[i])
                    else:
                        if isinstance(keys_values,list):
                            self.db.append(table,keys_values)
                        elif isinstance(keys_values,dict):
                            self.db.append(table,[keys_values])
        else:
            if type(condition)==type(None):
                self.db.clear_table(table)
            else:
                self.db.execute(f'DELETE FROM `{table}` WHERE {condition}')


    def convert_value_to_type(self,dict_data):
        for i in dict_data:
            dict_data[i] = type(dict_data[i])
        return dict_data

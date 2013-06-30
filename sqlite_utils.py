# -*- coding: utf-8 -*-
# %%06e04634dc02a21685ae0bf1dca0dadbeff3eb0758082e61fcd2304ae19ba69e7afda013125c5f1d3138487a150f61a0118734169f4c28e12ecbf82c7b0f3873%%

#
# Standard imports
#
import sys
import os
import platform
import sqlite3


def get_conf(conf):

    def san(splitted):
        if splitted[-1] == '\n':
            return splitted[:-1]
        return splitted

    with open(conf) as f:
        elements = {line.split("=")[0]: san(line.split("=")[1])
                    for line in f.readlines()}
                    
    #for x, y in elements.items():
    #    print(x, y)
    return elements

if os.path.isfile('.sqlite_conf'):
    elements = get_conf('.sqlite_conf')
else:
    elements = {}
    

class SQLiteConn(object):

    #def __convert(self, element):
    #
    #    # Python    SQLite
    #
    #    # None      NULL
    #    # int       INTEGER
    #    # float     REAL
    #    # str       TEXT
    #    # bytes     BLOB
    #
    #    # SQLite    Python
    #
    #    # NULL      None
    #    # INTEGER   int
    #    # REAL      float
    #    # TEXT      depends on text_factory, str by default
    #    # BLOB      bytes
    #    
    #    s2p = {'NULL': None, 'INTEGER': int, 'REAL': float, 'TEXT': str, 'BLOB': bytes}
    #    p2s = {None: 'NULL', int: 'INTEGER', float: 'REAL', str: 'TEXT', bytes: 'BLOB'}
    #    
    #    if element in s2p:
    #        return s2p[element]
    #    elif element in p2s:
    #        return p2s[element]
            
    def __init__(self, name=elements.get('dbname', ':memory:')):
    
        self.CREATE_TABLE_TEMPLATE = """CREATE TABLE IF NOT EXISTS {0} ({1})"""
        self.SELECT_TEMPLATE = """SELECT {1} FROM {0}"""
        self.INSERT_TEMPLATE = """INSERT INTO {0} ({1}) VALUES ({2})"""
        self.REMOVE_ALL_TEMPLATE = """DELETE FROM {0}"""
        self.UPDATE_TEMPLATE = """UPDATE {0} SET {1} WHERE {2}"""
        
        self.__tr = {
            'value_format': lambda type: {True: "'{}'", False: "{}"}[type == 'TEXT'],
            'insert_columns': lambda model: ", ".join(sorted(model['columns'])),
            'insert_plholders': lambda model: ", ".join(["?" for x in model['columns']]),
            'select_columns': lambda model: ", ".join(sorted(model['columns'])),
            'create_table_columns': lambda model: ", ".join(
                [
                    "{} {}".format(c, model['columns'][c]) 
                    for c in sorted(model['columns'])
                ]
            ),
            'update_columns': lambda values: ", ".join(
                ["{0} = ?".format(column) for column in sorted(values['columns'])]
            ),
            'update_where': lambda values: ", ".join(
                ["{0} = ?".format(column) for column in sorted(values['where'])]
            ),
        }
        
        self.conn = sqlite3.connect(name)
        self.conn.row_factory = sqlite3.Row
        
    def __generate_update(self, values):
    
        name = values['table']
        columns = self.__tr['update_columns']
        where = self.__tr['update_where']
        
        return self.UPDATE_TEMPLATE.format(name, columns(values), where(values))
        
    def __generate_remove_all(self, model):
    
        name = model['table']
    
        return self.REMOVE_ALL_TEMPLATE.format(name)
        
    def __generate_insert(self, model):
    
        name = model['table']
        columns = self.__tr['insert_columns']
        plholders = self.__tr['insert_plholders']
    
        return self.INSERT_TEMPLATE.format(name, columns(model), plholders(model))
        
    def __generate_select(self, model):
        
        name = model['table']
        columns = self.__tr['select_columns']
        
        return self.SELECT_TEMPLATE.format(name, columns(model))
        
    def __generate_create_table(self, model):
    
        name = model['table']
        columns = self.__tr['create_table_columns']
        
        return self.CREATE_TABLE_TEMPLATE.format(name, columns(model))
        
    def update(self, values, only_sql=False):
        
        sql = self.__generate_update(values)
        
        if only_sql:
            return sql
            
        else:
            cvalues = values['columns']
            wvalues = values['where']
            values = [cvalues[col] for col in sorted(cvalues)] + \
                     [wvalues[col] for col in sorted(wvalues)]
            
            c = self.conn.cursor()
            c.execute(sql, values)
            self.conn.commit()
            c.close()
            
        return self
        
    def remove_all(self, model, only_sql=False):
        
        sql = self.__generate_remove_all(model)
        
        if only_sql:
            return sql
            
        else:
            c = self.conn.cursor()
            c.execute(sql)
            self.conn.commit()
            c.close()
            
        return self
        
    def insert(self, model, values, only_sql=False):
        
        sql = self.__generate_insert(model)
        
        if only_sql:
            return sql
            
        else:
            cvalues = values['columns']
            values = [cvalues[col] for col in sorted(cvalues)]
            
            c = self.conn.cursor()
            c.execute(sql, values)
            self.conn.commit()
            c.close()
            
        return self
        
    def select(self, model, only_sql=False):
        
        sql = self.__generate_select(model)
        
        if only_sql:
            return sql
            
        else:
            c = self.conn.cursor()
            c.execute(sql)
            return c
        
    def create_table(self, model, only_sql=False):
    
        sql = self.__generate_create_table(model)
        
        if only_sql:
            return sql
            
        else:
            c = self.conn.cursor()
            c.execute(sql)
            c.close()
            return self
        
    def close(self):
        self.conn.close()

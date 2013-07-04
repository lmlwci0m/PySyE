#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# %%06e04634dc02a21685ae0bf1dca0dadbeff3eb0758082e61fcd2304ae19ba69e7afda013125c5f1d3138487a150f61a0118734169f4c28e12ecbf82c7b0f3873%%

SCRIPT_DEBUG_MODE = False

#
# Standard imports
#
import sys
import os
import platform
import argparse
import json

#
# Custom modules imports
#
from scripts_commons import get_conf, DEFAULT_LOCATOR_SOURCE, DEFAULT_ENC, check_os, main, writable
import sqlite_utils
import htmlgen

class RowIterator(object):
    def __init__(self, row, data_elems):
        self.row = row
        self.data_elems = data_elems
        self.keys = self.data_elems['export']['columns']

    def __iter__(self):
        self.index = 0
        return self
        
    def __next__(self):
        if self.index >= len(self.keys):
            raise StopIteration
        retval = self.row[self.keys[self.index]]
        self.index += 1
        return str(retval)
        
class CursorIterator(object):
    def __init__(self, cursor, data_elems):
        self.cursor = cursor
        self.data_elems = data_elems
        self.keys = self.data_elems['export']['columns']
        
    def __iter__(self):
        return self
        
    def __next__(self):
        row = self.cursor.fetchone()
        if row is None:
            raise StopIteration
        retval = {}
        for column in self.keys:
            retval[column] = row[column]
        
        return RowIterator(retval, self.data_elems)

def init(datafile, datainfo):
    conn = sqlite_utils.SQLiteConn(datafile)
    with open(datainfo) as f:
        data_elems = json.load(f)
    
    conn.create_table(data_elems['model'])
    
    conn.close()
    
    
def add(datafile, datainfo):
    conn = sqlite_utils.SQLiteConn(datafile)
    with open(datainfo) as f:
        data_elems = json.load(f)
    
    for values in data_elems['insert']:
    
        conn.insert(data_elems['model'], values)
    
    conn.close()
    
    
def change(datafile, datainfo):
    conn = sqlite_utils.SQLiteConn(datafile)
    with open(datainfo) as f:
        data_elems = json.load(f)
    
    conn.close()
    
    
def remove(datafile, datainfo):
    conn = sqlite_utils.SQLiteConn(datafile)
    with open(datainfo) as f:
        data_elems = json.load(f)
        
    conn.remove_all(data_elems['model'])
    
    conn.close()
    
    
def show(datafile, datainfo):
    conn = sqlite_utils.SQLiteConn(datafile)
    with open(datainfo) as f:
        data_elems = json.load(f)
        
    c = conn.select(data_elems['model'])
    
    for column in data_elems['model']['order']:
        print("{:20}".format(column), end=" | ")
    print()
    for row in c:
        
        for column in data_elems['model']['order']:
            print("{:20}".format(row[column]), end=" | ")
        print()
        
    c.close()
    conn.close()
    
    
def update(datafile, datainfo):
    
    conn = sqlite_utils.SQLiteConn(datafile)
    with open(datainfo) as f:
        data_elems = json.load(f)
        
    for values in data_elems['update']:
        conn.update(values)
        
    conn.close()
    
    
def export(datafile, datainfo):

    conn = sqlite_utils.SQLiteConn(datafile)
    with open(datainfo) as f:
        data_elems = json.load(f)
        
    c = conn.select(data_elems['model'])
    
    htmlgen.SimpleTemplate(
        elements=['Esport table: {}'.format(data_elems['export']['table'])],
        table=data_elems['export']['table'], 
        cols=data_elems['export']['columns'],
        body=CursorIterator(c, data_elems)
    ).create_page(
        data_elems['export']['template'], 
        '{}.html'.format(data_elems['export']['table'])
    )
    
    c.close()
    conn.close()

DATA_CONF = '.data_conf'

    
#
# Script execution
#
def execute(script_name, script_dir, cur_dir, paths):
    """
    usage: command [[datafile] datainfo]
    
    datafile and datainfo autowired from .data_conf
    """

    elements = {}
    datafile = None
    defaultmodel = None
    
    conf = os.path.join(script_dir, DATA_CONF)
    
    if os.path.isfile(conf):
        elements = get_conf(conf)
        datafile = elements.get('dbname', None)
        defaultmodel = elements.get('defaultmodel', None)

    parser = argparse.ArgumentParser()
    parser.add_argument("command", 
                        help="Data command to execute", 
                        type=str)
                        
    if len(sys.argv) > 3 or not datafile:
        parser.add_argument("datafile", 
                            help="Db name to operate in", 
                            type=str)
    
    if not defaultmodel or len(sys.argv) > 2:
        parser.add_argument("datainfo", 
                            help="General data info for command(model and values)", 
                            type=str)
        
                        
    args = parser.parse_args()
    if not defaultmodel or len(sys.argv) > 2:
        defaultmodel = args.datainfo
        
    if len(sys.argv) > 3 or not datafile:
        datafile = args.datafile
        
    
    commands = {
        'init': init,
        'add': add,
        'change': change,
        'remove': remove,
        'show': show,
        'update': update,
        'export': export,
    }
    
    commands[args.command](datafile, defaultmodel)


if __name__ == '__main__':

    main(execute, SCRIPT_DEBUG_MODE)

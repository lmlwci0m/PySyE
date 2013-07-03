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
import datetime

now = datetime.date.today

#
# Custom modules imports
#
from scripts_commons import get_conf, DEFAULT_LOCATOR_SOURCE, DEFAULT_ENC, check_os, main, writable
import sqlite_utils
import htmlgen


def add(datafile, datainfo):
    conn = sqlite_utils.SQLiteConn(datafile)
    with open(datainfo) as f:
        data_elems = json.load(f)
        
    cols = insert_data(data_elems)
    
    submodel = {    
        "model": data_elems['model'],
        "insert": [
            {
                "table": data_elems['model']['table'],
                "columns": cols
            }
        ]
    }
    
    for values in submodel['insert']:
    
        conn.insert(submodel['model'], values)
    
    conn.close()
    
    
def insert_data(model):
    cols = {}
    
    #for x in model['model']['order']:
    #    if "INTEGER PRIMARY KEY" in model['model']['columns'][x]:
    #        cols[x] = None
    #    else:
    #        cols[x] = input("[{}]: ".format(x))
            
    for x in model['model']['order']:
        cols[x] = input("[{}]: ".format(x))
        
    if "ID" in model['model']['columns']:
        cols["ID"] = None
            
    return cols
    
DATA_CONF = '.data_conf'
    
#
# Script execution
#
def execute(script_name, script_dir, cur_dir, paths):

    elements = {}
    datafile = None
    defaultmodel = None
    if os.path.isfile(DATA_CONF):
        elements = get_conf(DATA_CONF)
        datafile = elements.get('dbname', None)
        defaultmodel = elements.get('defaultmodel', None)

    parser = argparse.ArgumentParser()
                        
    if len(sys.argv) > 2 or not datafile:
        parser.add_argument("datafile", 
                            help="Db name to operate in", 
                            type=str)
    
    if not defaultmodel or len(sys.argv) > 1:
        parser.add_argument("datainfo", 
                            help="General data info for command(model and values)", 
                            type=str)
        
                        
    args = parser.parse_args()
    if not defaultmodel or len(sys.argv) > 1:
        defaultmodel = args.datainfo
        
    if len(sys.argv) > 2 or not datafile:
        datafile = args.datafile
    
    add(datafile, defaultmodel)


if __name__ == '__main__':

    main(execute, SCRIPT_DEBUG_MODE)

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

#
# Custom modules imports
#
from scripts_commons import get_conf, DEFAULT_LOCATOR_SOURCE, DEFAULT_ENC, check_os, main, writable
import sqlite_utils

model = {
    'table': 'TASKS',
    'columns': {
        'date': 'TEXT',
        'title': 'TEXT',
        'subject': 'TEXT',
        'description': 'TEXT',
    },
}

values = {
    'table': 'TASKS',
    'columns': {
        'date': '01-01-13',
        'title': 'Title',
        'subject': 'Subject',
        'description': 'Description',
    },
}

#
# Script execution
#
def execute(script_name, script_dir, cur_dir, paths):

    conn = sqlite_utils.SQLiteConn()
    
    print(conn.create_table(model, True))
    conn.create_table(model)
    
    print(conn.select(model, True))
    c = conn.select(model)
    for row in c:
        for key in sorted(model['columns']):
            print(row[key], end=" ")
        print()
    c.close()
    
    print(conn.insert(model, values, True))
    conn.insert(model, values)
    
    #print(conn.remove_all(model, True))
    #conn.remove_all(model)
    
    conn.close()

if __name__ == '__main__':

    main(execute, SCRIPT_DEBUG_MODE)

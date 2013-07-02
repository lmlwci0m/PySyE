#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Manually added
# %%06e04634dc02a21685ae0bf1dca0dadbeff3eb0758082e61fcd2304ae19ba69e7afda013125c5f1d3138487a150f61a0118734169f4c28e12ecbf82c7b0f3873%%
#
# PySyE project: check.py - script for source control of python modules and scripts.
#
# the best way to integrate this code to the system is to add source directory to the
# PATH environment variable.

SCRIPT_DEBUG_MODE = False

#
# Standard imports
#
import sys
import os
import platform
import argparse
import re

#
# Custom modules imports
#
from hashing import do_hash
import scripts_commons
from scripts_commons import get_conf, DEFAULT_LOCATOR_SOURCE, DEFAULT_ENC, check_os, main, writable
       
       
def check_file(filepath, hash_digest, pattern, full_check=True):
    
    if (full_check):
        print("Verifying {0:s}...".format(filepath), end="")
    
    if not os.path.isfile(filepath):
        print("{0:s} not exists.".format(filepath))
        
    else:
        
        with open(filepath) as fr:
            results = re.search(pattern, fr.read())
            check_ok = results and results.group('code') == hash_digest
            if full_check:
                if check_ok:
                    print("Done")
                else:    
                    print("No match")
            else:
                if check_ok:
                    print(filepath)
                    
                    
CHECK_CONF = '.check_conf'
                    
        
def execute(script_name, script_dir, cur_dir, paths):
    """
    usage: check.py path [-l locator]
    
    -l autowired from .check_conf
    """
    
    if len(sys.argv) < 2:
        print("{0:s}: No arguments specified".format(script_name))
        exit(0)
        
    elements = {}
    
    if os.path.isfile(CHECK_CONF):
        elements = get_conf(CHECK_CONF)
        
    parser = argparse.ArgumentParser()
    parser.add_argument("target", 
                        help="Python file path", 
                        type=str)
    parser.add_argument("-l", "--locator", 
                        help="Common identifier", 
                        type=str)
    args = parser.parse_args()
        
    if 'locator' in elements or args.locator:
        if args.locator:
            locator_source = bytes(args.locator, DEFAULT_ENC)
        else:
            locator_source = bytes(elements['locator'], DEFAULT_ENC)
    else:
        locator_source = DEFAULT_LOCATOR_SOURCE
        
    filepath = args.target
    hash_digest = do_hash(locator_source)
    pattern = re.compile("\%\%(?P<code>.{128})\%\%") #c = re.compile("\%\%.{128}\%\%")
    
    if not os.path.exists(filepath):
        print("{0:s} not exists.".format(filepath))
        exit(0)
    
    if os.path.isdir(filepath):
        for f in os.listdir(filepath):
            if ".py" == os.path.splitext(f)[-1]:
                check_file(os.path.join(filepath, f), hash_digest, pattern, False)
    else:
        check_file(filepath, hash_digest, pattern)


if __name__ == '__main__':

    main(execute, SCRIPT_DEBUG_MODE)

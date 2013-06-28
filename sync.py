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
import shutil

#
# Custom modules imports
#
from scripts_commons import get_conf, DEFAULT_LOCATOR_SOURCE, DEFAULT_ENC, check_os, main, writable
        
SYNC_CONF = '.sync_conf'

IGNORE_LIST = ['.DS_Store', '__pycache__']

        
def sync(src, dst, ignore_list, create_dir=False):
    
    status = {'ignored': [], 'notp': [], 'processed': []}
    
    if create_dir and not os.path.isdir(dst):
        os.mkdir(dst)
        #print("Directory {} created.".format(dst))

    src_contents = os.listdir(src)
    dst_contents = os.listdir(dst)
    
    for ignored in [os.path.join(src, content) 
                    for content in src_contents 
                    if content in ignore_list]:
        #print(" * Ignored     {}".format(ignored))
        status['ignored'].append(ignored)
    
    for notp in [os.path.join(dst, content) 
                 for content in dst_contents 
                 if content not in src_contents]:
        #print(" * Not by sync {}".format(notp))
        status['notp'].append(notp)
    
    processed = []
    for content in src_contents:
        if content not in ignore_list and not os.path.isdir(content):
            processed.append(shutil.copy2(os.path.join(src, content), os.path.join(dst, content)))
        
    for content in processed:
        #print("File {} copied.".format(content))
        status['processed'].append(content)
        
    processed_dirs = [
        (sync(os.path.join(src, content_dir), os.path.join(dst, content_dir),
             ignore_list,
             create_dir=True), os.path.join(dst, content_dir))
        for content_dir in src_contents
        if content_dir not in ignore_list and os.path.isdir(content_dir)
    ]
    
    for dir_status, content_dir in processed_dirs:
        #print("Directory {} copied.".format(content_dir))
        status['processed'].append(content_dir)
        status['processed'] += dir_status['processed']
        status['ignored'] += dir_status['ignored']
        status['notp'] += dir_status['notp']

    return status
    
    
def sync_check(src, dst, ignore_list, create_dir=False):

    src_contents = os.listdir(src)
    if os.path.exists(dst):
        dst_contents = os.listdir(dst)
    else:
        dst_contents = []
            
    for ignored in [os.path.join(src, content) 
                    for content in src_contents 
                    if content in ignore_list]:
        print(" * Ignored     {}".format(ignored))
    
    for notp in [os.path.join(dst, content) 
                 for content in dst_contents 
                 if content not in src_contents]:
        print(" * Not by sync {}".format(notp))
        
    processed_dirs = [
        sync_check(os.path.join(src, content_dir), os.path.join(dst, content_dir),
        ignore_list,
        create_dir=True)
        for content_dir in src_contents
        if content_dir not in ignore_list and os.path.isdir(content_dir)
    ]

    return dst
    

def assert_dir(path):
    if not os.path.isdir(path):
        print("{} not a directory. Exiting.".format(path))
        exit(0)
    
    
def sync_init(src, dst):
    
    assert_dir(src)
    assert_dir(dst)
    
    status = sync(src, dst, IGNORE_LIST)
    
    print("\nResults of synchronization:")
    print("Source:      {}".format(src))
    print("Destination: {}\n".format(dst))   
    
    for x in status['processed']:
        print(" * Synchronized        {}".format(x.split(dst)[1]))
        
    print()
        
    for x in status['ignored']:
        if os.path.isdir(x):
            print(" * Ignored       [dir] {}".format(x.split(src)[1]))
        else:
            print(" * Ignored             {}".format(x.split(src)[1]))
        
    print()
        
    for x in status['notp']:
        if os.path.isdir(x):
            print(" * Not in source [dir] {}".format(x.split(dst)[1]))
        else:
            print(" * Not in source       {}".format(x.split(dst)[1]))
        
    print()
        
    
def sync_init_options(src, dst):
    
    assert_dir(src)
    assert_dir(dst)
        
    sync_check(src, dst, IGNORE_LIST)
    
    if input("Proceed with synchronize?") in ['y', 'yes', 'ok']:
    
        sync(src, dst, IGNORE_LIST)

#
# Script execution
#
def execute(script_name, script_dir, cur_dir, paths):

    if len(sys.argv) == 1:
        
        if os.path.isfile(SYNC_CONF):
        
            elements = get_conf(SYNC_CONF)
                          
            src = cur_dir
            dst = elements['sync']
                
            sync_init(src, dst)
                
        else:
        
            print("No configuration found here.")
        
    else:
    
        parser = argparse.ArgumentParser()
        parser.add_argument("source", help="Directory path", type=str)
        parser.add_argument("destination", help="Directory path", type=str)
        args = parser.parse_args()

        src = args.source
        dst = args.destination
        
        sync_init_options(src, dst)
    

if __name__ == '__main__':

    main(execute, SCRIPT_DEBUG_MODE)

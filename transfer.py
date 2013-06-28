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
        
#
# Script execution
#
def execute(script_name, script_dir, cur_dir, paths):

    parser = argparse.ArgumentParser()
    parser.add_argument("source", 
                        help="Directory path", 
                        type=str)
    parser.add_argument("destination", 
                        help="Directory path", 
                        type=str)
    args = parser.parse_args()

    src = cur_dir
    name = os.path.basename(src)
    dst = os.path.join(args.destination, name)
    
    print("""Source: {}
    All files and subdirectory will be synced from this directory.
    """.format(src))
    print("Destination: {}".format(dst))
    
    #def ignore_no_py(dir, elements):
    #    print('Working in %s' % dir)
    #    return [x for x in elements if not ".py" == os.path.splitext(x)[-1] and 
    #    not os.path.isdir(os.path.join(dir, x))]   
        
    #shutil.copytree(src, dst, ignore=ignore_no_py)
    


if __name__ == '__main__':

    main(execute, SCRIPT_DEBUG_MODE)

#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Manually added
# %%06e04634dc02a21685ae0bf1dca0dadbeff3eb0758082e61fcd2304ae19ba69e7afda013125c5f1d3138487a150f61a0118734169f4c28e12ecbf82c7b0f3873%%
#
# PySyE project: new.py - script for generation of python modules and scripts.
#
# the best way to integrate this code to the system is to add source directory to the
# PATH environment variable.

SCRIPT_DEBUG_MODE = False

#
# Standard modules imports
#
import sys
import os
import platform
import argparse
import inspect


#
# Custom modules imports
#
from hashing import do_hash
import scripts_commons
from scripts_commons import get_conf, DEFAULT_LOCATOR_SOURCE, DEFAULT_ENC, check_os, main, writable
from templating import TemplateManager

NEW_CONF = '.new_conf'

        
def execute(script_name, script_dir, cur_dir, paths):
    """
    
    select locator
    select destination
    select type
    
    """
    
    temp_manager = TemplateManager()
    elements = {}
    
    if os.path.isfile(NEW_CONF):
        elements = get_conf(NEW_CONF)
    
    if len(sys.argv) < 2:
        print("{0:s}: No arguments specified".format(script_name))
        exit(0)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("destination", 
                        help="Python file path", 
                        type=str)
    parser.add_argument("-t", "--type", 
                        help="Type of python file", 
                        choices=temp_manager.choices())
    parser.add_argument("-l", "--locator", 
                        help="Common identifier", 
                        type=str)
    args = parser.parse_args()
    
    if 'template' in elements or args.type:
        if args.type:
            selected_template = args.type
        else:
            selected_template = elements['template']
    else:
        selected_template = temp_manager.APP
    
    if 'locator' in elements or args.locator:
        if args.locator:
            locator_source = bytes(args.locator, DEFAULT_ENC)
        else:
            locator_source = bytes(elements['locator'], DEFAULT_ENC)
    else:
        locator_source = DEFAULT_LOCATOR_SOURCE
    
    filepath = args.destination

    print("Creating {0:s} as python main...".format(filepath), end="")

    if not writable(filepath):
        print("Writing {0:s} aborted.".format(filepath))
        exit(0)
                                      
    template_path = temp_manager.get_path(selected_template)

    with open(os.path.join(script_dir, template_path), "r") as fr:
        with open(filepath, "w") as fw:
        
            if selected_template == temp_manager.MODULE:
                get_conf_func = "".join(inspect.getsourcelines(get_conf)[0])
                fw.write(fr.read().format(do_hash(locator_source), get_conf_func))
            else:
                fw.write(fr.read().format(do_hash(locator_source)))
    
    if selected_template == temp_manager.MODULE:
        os.chmod(filepath, scripts_commons.FileUtils().get_644())
    else:
        os.chmod(filepath, scripts_commons.FileUtils().get_755())
    
        
    print("Done")


if __name__ == '__main__':

    main(execute, SCRIPT_DEBUG_MODE)

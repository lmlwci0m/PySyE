#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Manually added
# %%06e04634dc02a21685ae0bf1dca0dadbeff3eb0758082e61fcd2304ae19ba69e7afda013125c5f1d3138487a150f61a0118734169f4c28e12ecbf82c7b0f3873%%
#
# Crynet project: scripts_commons.py - module for scripts common configuration.

import sys
import os
import platform
from functools import partial
import stat

color_orange = 255, 209, 41
color_green_blue = 33, 88, 103
color_cyan = 219, 238, 243


class FileUtils(object):

    def __init__(self):
        
        self.owner_r = stat.S_IREAD
        self.owner_w = stat.S_IWRITE
        self.owner_x = stat.S_IEXEC
        self.group_r = stat.S_IRGRP
        self.group_w = stat.S_IWGRP
        self.group_x = stat.S_IXGRP
        self.other_r = stat.S_IROTH
        self.other_w = stat.S_IWOTH
        self.other_x = stat.S_IXOTH
        
        self.owner_all = self.owner_r | self.owner_w | self.owner_x
        self.group_no_write = self.group_r | self.group_x
        self.other_no_write = self.other_r | self.other_x
        
    def get_755(self):
        return self.owner_all | self.group_no_write | self.other_no_write
        
    def get_644(self):
        return self.owner_r | self.owner_w | self.group_r | self.other_r
    

#
# aggregator identifier - use this for matching modules from the same source
#
DEFAULT_LOCATOR_SOURCE = b'crynet' # base for hashing

DEFAULT_ENC = 'utf-8'

def check_os():
    """Check platform."""
    
    if os.name == 'nt' or platform.system() == 'Windows':
        return 'nt'
    elif os.name == 'mac' or platform.system() == 'Darwin':
        return 'mac'
    elif os.name == 'posix' or platform.system() == 'Linux':
        return 'posix'
        
        
def writable(filepath):

    choose_check = ['y', 'yes', 'n', 'no']
    
    do_write = True
    
    if os.path.exists(filepath):
        
        prompt = partial(input, "\n{0:s} already exists. Overwrite(y/n)?".format(filepath))
        
        choose = prompt()
        while not choose in choose_check:
            choose = prompt()
            
        do_write = choose in choose_check[0:2]
        
    return do_write
        
        
def is_null(element):
    if not element:
        print("{} is null".format(repr(element)))
        
        
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
        
        
def main(execute, debug_mode):
    """Script initialization."""

    script_name = os.path.basename(sys.argv[0])
    script_dir = os.path.dirname(sys.argv[0])
    cur_dir = os.getcwd()
    paths = os.environ['PATH'].split(os.pathsep)
    
    if debug_mode:
        print("################## START PRINTING PATH ENV VAR ##################")
        print(os.environ['PATH'])
        print("################### END PRINTING PATH ENV VAR ###################")
    
    if script_dir not in paths:
        print("{0:s} is not set to your PATH environment variable.".format(script_dir))
    elif debug_mode:
        print("{0:s} is correctly set to your enviroment variable.".format(script_dir))
    
    print("Executing {0:s} from {1:s}".format(script_name, script_dir))
    print("Working dir is {0:s}".format(cur_dir))
    
    execute(script_name, script_dir, cur_dir, paths)

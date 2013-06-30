#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Manually added
# %%06e04634dc02a21685ae0bf1dca0dadbeff3eb0758082e61fcd2304ae19ba69e7afda013125c5f1d3138487a150f61a0118734169f4c28e12ecbf82c7b0f3873%%
#
# PySyE project: templating.py - module for templates facility.

import os


class TemplateManager(object):

    def __init__(self, template_location='templates'):
        self.APP = 'app'
        self.SCRIPT = 'script'
        self.MODULE = 'module'
        self.templates = {
            self.APP: 'app_template.py',
            self.SCRIPT: 'script_template.py',
            self.MODULE: 'module_template.py',
        }
        self.location = template_location
        
    def choices(self):
        return list(self.templates.keys())
        
    def get_path(self, temp_name):
        return os.path.join(self.location, self.templates[temp_name])

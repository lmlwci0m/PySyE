# -*- coding: utf-8 -*-
# %%06e04634dc02a21685ae0bf1dca0dadbeff3eb0758082e61fcd2304ae19ba69e7afda013125c5f1d3138487a150f61a0118734169f4c28e12ecbf82c7b0f3873%%

#
# Standard imports
#
import sys
import os
import platform
import re
from functools import partial

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


DEFAULT_ENCODING = "utf-8"

def iterable(obj):
    import collections

    if isinstance(obj, collections.Iterable):
        return True
    else:
        return False


def pre_repl(self, parent, match):
    """
    self : SimpleTemplate object
    parent : [file object]
    match : Match object
    """

    string = match.group()[2:-1] # Rule: ${var} -> var
    
    if ":" in string:
    
        tag_inc, tag_var = string.split(":")
    
        #
        # include external file: RECURSION into parent file
        #
        filename = tag_var + ".html"
       
        if "(" in tag_inc and ")" in tag_inc:
        
            #
            # Managing loops
            #
        
            loop_var = self[tag_inc[2:-1]]
            
            if type(loop_var) == list or iterable(loop_var):
            
                #
                # __item__ is used for list loops
                # __item__[name] is used for dictionaries
                #
            
                if "__item__" in self:
                    self.stack.append(self["__item__"])
            
                for x in loop_var:
                    
                    self["__item__"] = x
                    
                    if type(x) == dict:
                    
                        for key in x:
                            if "__stack__item__{}".format(key) not in self:
                                self["__stack__item__{}".format(key)] = []
                            if "__item__{}".format(key) in self:
                                self["__stack__item__{}".format(key)].append(self["__item__{}".format(key)])
                            self["__item__{}".format(key)] = x[key]
                    
                    self.create_page(filename, output=None, parent=parent)
                    
                    if type(x) == dict:
                    
                        for key in x:
                            if len(self["__stack__item__{}".format(key)]) > 0:
                                self["__item__{}".format(key)] = self["__stack__item__{}".format(key)].pop()
                        
                if len(self.stack) > 0:
                    self["__item__"] = self.stack.pop()
                
            else:
                
                if "__item__" in self:
                    self.stack.append(self["__item__"])
            
                self["__item__"] = str(loop_var)
                self.create_page(filename, output=None, parent=parent)
            
                if len(self.stack) > 0:
                    self["__item__"] = self.stack.pop()
            
        else:
        
            self.create_page(filename, output=None, parent=parent)

    elif string in self:
        #
        # normal string subtitution value
        #
        return self[string]

    return ""
    

class SimpleTemplate(dict):
    """
    e = SimpleTemplate(
        title="Pippo", 
        body='Pluto', 
        header='Template generator', 
        par="This is a test",
        secpar="This is a second test",
        font="tahoma",
        fontsize="11px"
        )
    
    e.create_page(input="base_template.html", output="test.html")
    """

    pattern_matcher = None
    include_patter_matcher = None
    stack = []

    def __get_pattern_matcher(self):
        if self.pattern_matcher is None: #    "\$\{(?:f(\(\w+\))?:)?\w+\}" "\$\{    (f   (\(\w+\))?   :)?    \w+\}"
            self.pattern_matcher = re.compile("\$\{(?:f(?:\(\w+\))?:)?\w+\}")
        return self.pattern_matcher
        
    def __get_include_pattern_matcher(self):
        if self.include_patter_matcher is None: # "\$\{f:(\(\w+\))?\w+\}"
            self.include_patter_matcher = re.compile("\$\{f(?:\(\w+\))?:\w+\}") 
        return self.include_patter_matcher
        
    def __process_template_loop(self, pattern, repl, t, output_file):
        """Managing read/write cycles.
        
        pm: tags pattern
        repl: replacement function 
        t: input template file object
        dest: output file object
        """
        
        include_pattern = self.__get_include_pattern_matcher()
        
        #
        # substitution with repl as rule
        # 
        #
        do_replace = partial(pattern.sub, repl)
        
        #
        # Aliasing for output writing
        #
        do_write = output_file.write
        
        #
        # Process template file line by line
        #
        line = t.readline()
        while line != '':
            
            #
            # For each line
            #
            
            # 
            # Check include tag elements
            #
            # line:  **${*}**${f:*}**${*}**${*}**${f:*}**${*}**
            #        \______/\____/\____________/\____/\______/
            #
            # split  elems[0]         elems[1]         elems[2]
            #               \         /      \         /
            # findall       includes[0]      includes[1]
            #
            elems, includes = include_pattern.split(line), include_pattern.findall(line)
            
            #print("Line elements: {} {}".format(elems, includes))
            
            if len(elems) > 1:
            
                # Include tags found: split and process sequentially
                # due to missing process of file tag's previous sections
            
                for x in range(len(elems)):
                
                    do_write(do_replace(elems[x]))
                    
                    if x < len(elems) - 1:
                    
                        do_write(do_replace(includes[x]))
                        
            else:
            
                # 
                # No file tags: process entire line
                #
                
                do_write(do_replace(line)) # TODO: ERROR ERROR ERROR
            
            line = t.readline() # Next line
            
    def __process_template(self, input, pattern, output_file):
        """Template reading and transformation initialization."""
    
        with open(input, "r", encoding=DEFAULT_ENCODING) as t:
            repl = partial(pre_repl, self, output_file)
            self.__process_template_loop(pattern, repl, t, output_file)
                    
    def create_page(self, input, output, parent=None):
        """Make transformation from input to output.
    
        Using recursion in order to write template transformations.
        
        input: tamplate fila name
        output: output of tree tranformation. Used only on root
        parent: file object reference for no-root nodes
        """
    
        pattern = self.__get_pattern_matcher()
    
        if parent == None:
        
            # Start of template tree: new file creation
        
            #
            # Template nodes must be in the same directory!!!
            #
            self.template_dir = os.path.dirname(input)
        
            with open(output, "w", encoding=DEFAULT_ENCODING) as output_file:
                self.__process_template(input, pattern, output_file)
            
        else:
        
            # Go deep into the tree: use existing open file
            
            self.__process_template(os.path.join(self.template_dir, input), 
                                    pattern, parent)
            

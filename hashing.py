#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# Manually added
# %%06e04634dc02a21685ae0bf1dca0dadbeff3eb0758082e61fcd2304ae19ba69e7afda013125c5f1d3138487a150f61a0118734169f4c28e12ecbf82c7b0f3873%%
#
# PySyE project: hashing.py - module for hashing facility.

import hashlib
from functools import partial, reduce
import random


DEFAULT_HASH_FUNC = hashlib.sha512
DEFAULT_HASH_LOOP = 50
DEFAULT_RANDOM_SEED = 80


def hash_iteration_old(source):
    h = DEFAULT_HASH_FUNC()
    h.update(source)
    return h.digest()
    

def hash_iteration(source):
    h = DEFAULT_HASH_FUNC()
    if type(source) == bytes:
        h.update(source)
    else:
        h.update(source.digest())
    return h
    

#
# Not actually used
#
def shuffle(source_str):
    """Shuffle a string."""

    random.seed(DEFAULT_RANDOM_SEED)
    element = list(source_str)
    random.shuffle(element)
    return "".join(element)
    
    
def dodigest(h):
    return h.hexdigest()
    
    
do_hash = partial(reduce, 
                  lambda x, y: y(x), 
                  [hash_iteration] * DEFAULT_HASH_LOOP + [dodigest])




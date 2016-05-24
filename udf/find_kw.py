#!/usr/bin/env python
from deepdive import *
import ddlib

@tsv_extractor
@returns(lambda
        author  = "text",
        body    = "text",
        kw      = "text",
        index   = "int",
        is_kw   = "int",
    :[])
def find_kw(
        author       = "text",
        body         = "text",
    ):
    
    uni_true = ddlib.load_dictionary("/home/denimalpaca/Documents/CS/293n/input/uni_kws.txt", dict_id="uni_true")
    uni_false = ddlib.load_dictionary("/home/denimalpaca/Documents/CS/293n/input/non_kws.txt", dict_id="uni_false")
    
    i = 0
    for word in body:
        i += 1
        if word in uni_true:
            yield [author, body, word, i-1, 1]
        if word in uni_false:
            yield [author, body, word, i-1, -1]

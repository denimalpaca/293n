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
    
    ddlib.load_dictionary("uni_kws.txt", dict_id="uni_true")
    ddlib.load_dictionary("non_kws.txt", dict_id="uni_false")

    for i, word in body:
        if word in uni_true:
            yield [author, body, word, i, 1]
        if word in uni_false:
            yield [author, body, word, i, -1]

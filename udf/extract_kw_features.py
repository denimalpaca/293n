#!/usr/bin/env python
from deepdive import *
import ddlib

@tsv_extractor
@returns(lambda
        author  = "text",
        keyword = "text",
        feature = "text",
    :[])

def extract(
        author      = "text",
        keyword     = "text",
        index       = "int",
        is_kw       = "bool",
        tokens      = "text[]",
        lemmas      = "text[]",
        pos_tags    = "text[]",
        ner_tags    = "text[]",
        dep_tokens  = "int[]",
        dep_types   = "text[]",
    ):
    # Create a DDLIB sentence object, which is just a list of DDLIB Word objects
    sent = []
    for i,t in enumerate(tokens):
        sent.append(ddlib.Word(
            begin_char_offset=None,
            end_char_offset=None,
            word=t,
            lemma=lemmas[i],
            pos=pos_tags[i],
            ner=ner_tags[i],
            dep_par=dep_tokens[i] - 1,
            dep_label=dep_types[i]))

    # Create DDLIB Span object from keyword index
    kw_span = ddlib.Span(begin_word_id=index, length=1)

    # Generate generic features for keyword mention
    for feature in ddlib.get_generic_features_mentions(sent, kw_span):
        yield [author, keyword, feature]

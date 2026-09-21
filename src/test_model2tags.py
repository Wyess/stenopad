#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

import pytest
from model2tags import model2tags

TEST_CASES = [
    ("ner8", "@model_ner8"),
    ("ner8", "@model_ner"),
    ("ner8", "@head_ner8"),
    ("ner8", "@head_ner"),
    ("ner8", "@tail_ner8"),
    ("ner8", "@tail_ner"),

    #("ne8", []),
    #("nel8", []),
    #("uswl4", []),
    #("e8cl1", []),
    ("oswl4",  "@head_oswl4"),
    ("oswl4",  "@tail_oswl4"),
    ("swl4swr4", "@head_swl4"),
    ("swl4swr4", "@tail_swr4"),
    #("e8f", []),
    #("ne8f", []),
    #("e8cl1", []),
    #("e8nw4", []),
]

@pytest.mark.parametrize("model, tag", TEST_CASES)
def test_model2tags(model, tag):
    assert tag in model2tags(model)

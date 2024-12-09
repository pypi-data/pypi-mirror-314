import pytest

import numpy as np
import pandas as pd
from epitope_aligner import map, stretch, utils

@pytest.fixture(params=[0,1], ids=["0index","1index"])
def index(request):
    return request.param

@pytest.fixture(params=[True, False], ids=["endin","endout"])
def includeend(request):
    return request.param

@pytest.fixture
def sequence():
    return utils.random_seq(100)

@pytest.fixture
def epitopes(sequence, index, includeend):
    return utils.random_epitopes(
        sequence,
        n=100,
        epitope_lengths=(5,15),
        index=index,
        includeend=includeend
    )

def test_seq_len(epitopes, includeend):
    seq_lengths = epitopes.seq.apply(len)
    lengths = epitopes.length
    intervals = epitopes.end - epitopes.start + includeend
    assert all([sl==l==i for sl,l,i in zip(seq_lengths, lengths, intervals)])


def test_random_epitopes(sequence, epitopes, index):
    floating_epitopes = map.float_epitopes(
        table=epitopes,
        parent_seq=None,
        start_col="start",
        index=index
    )
    scores = ([map._score_epitope_alignment(epi, sequence)[0] for epi in floating_epitopes])
    assert sum(scores) == len(scores)

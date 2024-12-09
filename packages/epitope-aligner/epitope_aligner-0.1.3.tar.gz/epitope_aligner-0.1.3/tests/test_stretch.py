
import pytest
import numpy as np
import pandas as pd
from epitope_aligner import map, stretch, utils

# missing first residue?
# how to get length
# check residues with indexes


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

def test_stretch_size(epitopes, index):
    stretched_epitopes = stretch.stretch(epitopes)
    total_stretch_size = sum(stretched_epitopes.groupby(["seq", "start"]).size())
    assert sum(epitopes.length) == total_stretch_size


def test_stretch_custom_cols(epitopes):
    """Add test that start_col argument works"""
    EPITOPES = epitopes.copy()
    EPITOPES = EPITOPES.rename(columns = {
        "start": "START",
        "length": "LENGTH",
        "seq": "SEQ"
    })
    stretched_epitopes = stretch.stretch(
        epitopes=EPITOPES,
        length_col= "LENGTH",
        start_col= "START",
        seq_col= "SEQ"
    )
    total_stretch_size = sum(stretched_epitopes.groupby(["SEQ", "START"]).size())
    assert sum(epitopes.length) == total_stretch_size


def test_position_name_assertion(epitopes, sequence, index, ):
    stretched_epitopes = stretch.stretch(epitopes)
    positional_count = stretched_epitopes.groupby("position").size()
    with pytest.raises(AssertionError):
        stretch.add_empty_positions(
            positional_count,
            parent_seq_length=len(sequence),
            index=index,
            empty_value=0,
            position_name="missing name"
        )


def test_3group_grid_fail(sequence, epitopes, index):
    epitopes['allele'] = np.random.choice(["x","y","z"], epitopes.shape[0])
    stretched_epitopes = stretch.stretch(epitopes)
    allele_position_count = stretched_epitopes.groupby(["allele", "position", "length"]).size()
    with pytest.raises(AssertionError):
        grid = stretch.make_grid(
            allele_position_count,
            index=index,
            parent_seq_length=len(sequence),
            empty_value=0
        )


@pytest.fixture
def grid(sequence, epitopes, index):
    epitopes['allele'] = np.random.choice(["x","y","z"], epitopes.shape[0])
    stretched_epitopes = stretch.stretch(epitopes)
    allele_position_count = stretched_epitopes.groupby(["allele", "position"]).size()
    grid = stretch.make_grid(
        allele_position_count,
        index=index,
        parent_seq_length=len(sequence),
        empty_value=0
    )
    return grid


def test_grid_sum(epitopes, grid):
    epitope_sum = epitopes.groupby('allele').length.sum()
    epitope_sum.sort_index(inplace=True)
    grid_sum = grid.sum(axis=1)
    grid_sum.sort_index(inplace=True)
    assert all(epitope_sum == grid_sum)


def test_grid_pos_sum(sequence, epitopes, index):
    epitopes['allele'] = np.random.choice(["x","y","z"], epitopes.shape[0])
    stretched_epitopes = stretch.stretch(epitopes)
    allele_position_count = stretched_epitopes.groupby(["allele", "position"]).size()
    position_sum = allele_position_count.groupby('position').sum()
    pos_sums = []
    for i in range(index, len(sequence)+index):
        i
        pos_sums.append(position_sum[position_sum.index == i].sum())
    grid = stretch.make_grid(
        allele_position_count,
        index=index,
        parent_seq_length=len(sequence),
        empty_value=0
    )
    assert all(grid.sum(axis=0) == pos_sums)


def test_grid_width(sequence, grid):
    assert grid.shape[1] == len(sequence)


@pytest.fixture
def iedb_epitopes():
    sequence = "abcdefghi"
    iedb_epitopes = pd.DataFrame({
        'start': [1.0,2,2,6],
        'end': [3,4,4,8],
        'seq': ['abc','bcd','bcd','fgh'],
        'mhc_allele': ["x","x","y","z"]
    })
    iedb_epitopes['length'] = iedb_epitopes.seq.apply(len)
    return sequence,iedb_epitopes


def test_iedb_epitope_grid(iedb_epitopes):
    sequence, iedb_epitopes = iedb_epitopes
    stretched_epitopes = stretch.stretch(iedb_epitopes)
    allele_position_count = stretched_epitopes.groupby(["mhc_allele", "position"]).size()
    grid = stretch.make_grid(
        allele_position_count,
        index=1,
        parent_seq_length=len(sequence),
        empty_value=0
    )
    grid.sort_index(inplace=True)
    expected = np.array([
        [1,2,2,1,0,0,0,0,0],
        [0,1,1,1,0,0,0,0,0],
        [0,0,0,0,0,1,1,1,0]
    ])
    assert all(grid == expected)

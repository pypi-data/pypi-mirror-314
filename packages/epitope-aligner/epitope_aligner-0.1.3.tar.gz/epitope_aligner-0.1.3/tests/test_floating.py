from epitope_aligner import map, utils
import pandas as pd
import pytest

def test_align_float_peptide():
    assert map._align_float(
        start=2,
        seq="CDEF",
        parent_seq="ABC--DE-FG",
        index=0
    ) == "C--DE-F"

def test_float_peptides():
    sequence = "abcdefghi"
    epitopes = pd.DataFrame(
        {
            'START': [1.0,2,3,4,6],
            'END': [4,5,6,7,9],
            'SEQ': ['abc','bcd','cde','def','fgh']
        }
    )
    floating_peptides = map.float_epitopes(epitopes, parent_seq=sequence, index=1, start_col="START", seq_col="SEQ")
    assert floating_peptides == ['abc', '-bcd', '--cde', '---def', '-----fgh']


def test_float_peptides_none_parent():
    sequence = "abcdefghi"
    epitopes = pd.DataFrame(
        {
            'START': [1.0,2,3,4,6],
            'END': [4,5,6,7,9],
            'SEQ': ['abc','bcd','cde','def','fgh']
        }
    )
    floating_peptides = map.float_epitopes(epitopes, parent_seq=None, index=1, start_col="START", seq_col="SEQ")
    assert floating_peptides == ['abc', '-bcd', '--cde', '---def', '-----fgh']


def test_score_1_toupper():
    sequence = "ABCDEFGHI"
    epitopes = pd.DataFrame(
        {
            'START': [1.0,2,3,4,6],
            'END': [4,5,6,7,9],
            'SEQ': ['abc','xcd','cxe','dex','xxh']
        }
    )
    floating_peptides = map.float_epitopes(
        epitopes,
        parent_seq=sequence,
        index=1,
        start_col="START",
        seq_col="SEQ"
    )
    epitopes['floating_peptides'] = floating_peptides
    score_matches = map.score_epitope_alignments(
        table=epitopes,
        parent_seq=sequence,
        seq_col="floating_peptides"
    )
    scores = score_matches.score.tolist()
    true_scores = [1, 2/3, 2/3, 2/3, 1/3]
    assert scores == pytest.approx(true_scores)


def test_score_1_noupper():
    sequence = "ABCDEFGHI"
    epitopes = pd.DataFrame(
        {
            'START': [1.0,2,3,4,6],
            'END': [4,5,6,7,9],
            'SEQ': ['abc','xcd','cxe','dex','xxh']
        }
    )
    floating_peptides = map.float_epitopes(
        epitopes,
        parent_seq=sequence,
        index=1,
        start_col="START",
        seq_col="SEQ"
    )
    epitopes['floating_peptides'] = floating_peptides
    score_matches = map.score_epitope_alignments(
        table=epitopes,
        parent_seq=sequence,
        seq_col="floating_peptides",
        toupper=False
    )
    scores = score_matches.score.tolist()
    true_scores = [0, 0, 0, 0, 0]
    assert scores == pytest.approx(true_scores)

def test_score_length_assertion():
    seq = "ABC"
    epi = "-BCD"
    with pytest.raises(AssertionError):
        map._score_epitope_alignment(epi, seq)

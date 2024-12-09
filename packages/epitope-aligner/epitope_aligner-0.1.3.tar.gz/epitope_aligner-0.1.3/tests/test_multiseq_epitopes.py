from epitope_aligner import map, utils
import pandas as pd
import pytest

@pytest.fixture(params=[0, 1], ids=['0index','1index'])
def index(request):
    return request.param


@pytest.fixture(params=[True, False], ids=["endin", "endout"])
def includeend(request):
    return request.param


@pytest.fixture(params=[1,2,3])
def seqlist(request):
    seqlist = []
    for i in range(request.param):
        seq = utils.random_seq(100)
        seqlist.append(seq)
    return seqlist


@pytest.fixture
def epitopes(seqlist, index, includeend):
    epilist = []
    for i,seq in enumerate(seqlist):
        epi = utils.random_epitopes(
            sequence=seq,
            n=100,
            epitope_lengths=(5, 15),
            index=index,
            includeend=includeend
        )
        epi['parent'] = f"seq{i}"
        epilist.append(epi)
    epilist = pd.concat(epilist)
    epilist = epilist.reset_index(drop=True)
    return epilist


@pytest.fixture
def aligned_seq(seqlist):
    aligned_seq = []
    for seq in seqlist:
        al_seq = utils.random_gaps(
            seq,
            gap_prob=0.2,
            gap_size_interval=(1,5)
        )
        aligned_seq.append(al_seq)
    if len(aligned_seq) == 1:
        aligned_seq = aligned_seq[0]
    else:
        keys = [f"seq{i}" for i in range(len(aligned_seq))]
        aligned_seq = dict(zip(keys, aligned_seq))
    return aligned_seq


@pytest.fixture
def sequence(seqlist):
    if len(seqlist) == 1:
        sequence = seqlist[0]
    else:
        keys = [f"seq{i}" for i in range(len(seqlist))]
        sequence = dict(zip(keys, seqlist))
    return sequence


def test_float_random_peptides(epitopes, sequence, index):
    epitopes['float'] = map.float_epitopes(
        table=epitopes,
        parent_seq=sequence,
        start_col="start",
        index=index,
        parent_col="parent"
    )
    scores_matches = map.score_epitope_alignments(
        table=epitopes,
        parent_seq=sequence,
        seq_col="float",
        parent_col="parent"
    )
    perfect_score = scores_matches.score == 1
    all_match = scores_matches.matches.apply(lambda x: sum(x) == len(x))
    assert all(perfect_score) and all(all_match)


def test_align_float(epitopes, aligned_seq, index, includeend):
    epitopes['newstart'] = map.align_coords(
        table=epitopes,
        aligned_parent_seq=aligned_seq,
        coord_col="start",
        parent_col="parent",
        index=index
    )
    epitopes['newend'] = map.align_coords(
        table=epitopes,
        aligned_parent_seq=aligned_seq,
        coord_col="end",
        parent_col="parent",
        index=index
    )
    epitopes['float'] = map.float_epitopes(
        table=epitopes,
        parent_seq=aligned_seq,
        start_col="newstart",
        parent_col="parent",
        index=index
    )
    trimmed_epitope_floats = epitopes.float.str.replace("^-*", "", regex=True)
    pss = map.ParentSeqSerialiser(parent_seq_object=aligned_seq)

    aligned_seq_epitope_slices = epitopes.apply(
        lambda x: pss.get_parent_seq(x['parent'])[x.newstart-index:x.newend-index+includeend], axis=1
    )
    aligned_seq_epitope_slices = aligned_seq_epitope_slices.str.replace(
        "-*$", "", regex=True
    )
    assert all(trimmed_epitope_floats == aligned_seq_epitope_slices)


def test_score_matches_length(epitopes, sequence, index):
    epitopes['float'] = map.float_epitopes(
        table=epitopes,
        parent_seq=sequence,
        start_col="start",
        index=index,
        parent_col="parent"
    )
    scores_matches = map.score_epitope_alignments(
        table=epitopes,
        parent_seq=sequence,
        seq_col="float",
        parent_col="parent"
    )
    match_lengths = scores_matches.matches.apply(len)
    assert all(epitopes.length == match_lengths)


def test_floating_seqrecord(epitopes, index, sequence):
    floating_seqs = map.float_epitopes(
        table=epitopes,
        parent_seq=sequence,
        index=index,
        start_col="start",
        id_col="seq",
        parent_col="parent"
    )
    seqrecord_ids = [r.id for r in floating_seqs]
    assert all(seqrecord_ids == epitopes.seq)


def test_locate_peptide(epitopes, sequence, index, includeend):
    floating_epitopes = map.float_epitopes(
        table=epitopes,
        parent_seq=sequence,
        start_col="start",
        index=index,
        parent_col="parent"
    )
    located_pos = [map.locate_epitope(floater, index, includeend) for floater in floating_epitopes]
    epitopes['located_start'] = [pos[0] for pos in located_pos]
    epitopes['located_end'] = [pos[1] for pos in located_pos]
    starts_match = epitopes['start'] == epitopes['located_start']
    ends_match = epitopes['end'] == epitopes['located_end']
    assert all(starts_match & ends_match)


def test_apply_locate_peptide(epitopes, sequence, index, includeend):
    epitopes['float'] = map.float_epitopes(
        table=epitopes,
        parent_seq=sequence,
        start_col="start",
        index=index,
        parent_col="parent"
    )
    located_pos = epitopes.float.apply(
        map.locate_epitope,
        index=index,
        includeend=includeend,
    )
    epitopes['located_start']=pd.DataFrame(located_pos.tolist())[0]
    epitopes['located_end']=pd.DataFrame(located_pos.tolist())[1]
    starts_match = epitopes['start'] == epitopes['located_start']
    ends_match = epitopes['end'] == epitopes['located_end']
    print(epitopes[~starts_match | ~ends_match].values)
    assert all(starts_match & ends_match)


def test_align_coordinate(epitopes, aligned_seq, index, includeend):
    epitopes['newstart'] = map.align_coords(
        table=epitopes,
        aligned_parent_seq=aligned_seq,
        coord_col="start",
        parent_col="parent",
        index=index
    )
    epitopes['newend'] = map.align_coords(
        table=epitopes,
        aligned_parent_seq=aligned_seq,
        coord_col="end",
        parent_col="parent",
        index=index
    )
    pps = map.ParentSeqSerialiser(aligned_seq)
    epitopes['aligned_seq'] = epitopes.apply(lambda x: pps.get_parent_seq(x.parent)[x.newstart-index:x.newend-index+includeend], axis=1)
    assert all(epitopes.seq == epitopes.aligned_seq.str.replace("-",""))


def test_align_last_coordinate(aligned_seq, sequence, index):
    if isinstance(sequence, str):
        sequence = {'seq0': sequence}
    if isinstance(aligned_seq, str):
        aligned_seq = {'seq0': aligned_seq}
    last_coordinates = [len(seq)+index for seq in sequence.values()]
    last_characters = [seq[-1] for seq in sequence.values()]
    epi = pd.DataFrame({
        "last_character": last_characters,
        "end": last_coordinates,
        'parent_seq': sequence.keys()
    })
    epi['new_end'] = map.align_coords(
        table=epi,
        aligned_parent_seq=aligned_seq,
        coord_col="end",
        index=index,
        parent_col='parent_seq'
    )
    pss = map.ParentSeqSerialiser(parent_seq_object=aligned_seq)
    epi['new_end_character'] = epi.apply(lambda x: pss.get_parent_seq(x.parent_seq)[x.new_end-1-index], axis=1)
    assert all(epi.new_end_character == epi.last_character)


def test_align_past_end_coordinate_fail(aligned_seq, sequence, index):
    if isinstance(sequence, str):
        sequence = {'seq0': sequence}
    if isinstance(aligned_seq, str):
        aligned_seq = {'seq0': aligned_seq}
    last_coordinates = [2*len(seq)+index for seq in sequence.values()]
    last_characters = [seq[-1] for seq in sequence.values()]
    epi = pd.DataFrame({
        "last_character": last_characters,
        "end": last_coordinates,
        'parent_seq': sequence.keys()
    })
    with pytest.raises(Exception):
        epi['new_end'] = map.align_coords(
            table=epi,
            aligned_parent_seq=aligned_seq,
            coord_col="end",
            index=index,
            parent_col='parent_seq'
        )


def test_unalign_coordinate(epitopes, aligned_seq, index, includeend, sequence):
    epitopes['newstart'] = map.align_coords(
        table=epitopes,
        aligned_parent_seq=aligned_seq,
        coord_col="start",
        parent_col="parent",
        index=index
    )
    epitopes['newend'] = map.align_coords(
        table=epitopes,
        aligned_parent_seq=aligned_seq,
        coord_col="end",
        parent_col="parent",
        index=index
    )
    epitopes['oldstart'] = map.unalign_coords(
        table=epitopes,
        aligned_parent_seq=aligned_seq,
        coord_col="newstart",
        parent_col="parent",
        index=index,
        gap="-"
    )
    epitopes['oldend'] = map.unalign_coords(
        table=epitopes,
        aligned_parent_seq=aligned_seq,
        coord_col="newend",
        parent_col="parent",
        index=index,
        gap="-"
    )
    pps = map.ParentSeqSerialiser(sequence)
    epitopes['unaligned_seq'] = epitopes.apply(lambda x: pps.get_parent_seq(x.parent)[x.oldstart-index:x.oldend-index+includeend], axis=1)
    assert all(epitopes.seq == epitopes.unaligned_seq)

from typing import Literal
import re
import logging
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord


def _align_float(
    start: int, seq: str, parent_seq: str, index: int, gap: str = "-"
) -> str:
    """Match spacing between epitope and parent sequence

    If the epitope spans an insertion in the parent sequence,
    indicated by gaps, these gaps will be added to the floating
    epitope. E.g. 'LOPS' in 'ABCD--FGHIJKL--OP--STUVWXYZ'
    becomes 'L--OP--S'.

    Note, this does not add gaps the start of the epitope.
    Instead this function is called by _float_peptide() before
    adding gaps to the start of the epitope.

    Args:
        start (int): The start position of the epitope
        seq (str): The epitope sequence to float
        parent_seq (str): The parent sequence the epitope is derived from
        index (int): Counting index, i.e. do the position counts start at
            0 or 1?
        gap (str, optional): The gap character. Defaults to "-".

    Returns:
        str: The "floating" sequence
    """
    if isinstance(start, float):
        start = int(start)
    if index == 1:
        start = start - 1
    i = 0
    floating_peptide = []
    for aa in parent_seq[start:]:
        if aa == gap:
            floating_peptide.append(gap)
        else:
            floating_peptide.append(seq[i])
            i += 1
        if i >= len(seq):
            break
    floating_peptide = "".join(floating_peptide)
    return floating_peptide


def _float_epitope(start, seq, parent_seq, index):
    """Add gaps to epitope sequence so it aligns with its parent sequence.


    Args:
        start (int): The start position of the epitope
        seq (str): The epitope sequence to float
        parent_seq (str): The parent sequence the epitope is derived from
        index (int): Counting index, i.e. do the position counts start at
            0 or 1?

    Returns:
        str: The "floating" sequence
    """
    if parent_seq is not None:
        seq = _align_float(start=start, seq=seq, parent_seq=parent_seq, index=index)
    if index == 1:
        start = start - 1
    start = int(start)
    floating_peptide = "-" * start + seq
    return floating_peptide


def float_epitopes(
    table,
    parent_seq: str | dict,
    index,
    start_col: str,
    seq_col="seq",
    parent_col=None,
    id_col=None,
):
    """Add gaps to sequences so they align to their parent

    Args:
        table (pd.DataFrame): Dataframe of epitopes with sequences and their
            start position as columns.
        parent_seq (str|dict): A single parent sequence sting to use for all
            epitopes or a dictionary of multiple epitopes, or "parent_seq_column".
            See epitope_aligner.map.ParentSeqSerialiser for details.
        index (int): Counting index, i.e. do the positions start at 0 or 1?
        start_col (str): Name of the column with start positions.
        seq_col (str, optional): Name of column with sequences. Defaults to
            "seq".
        parent_col (str, optional): If provided, this column is used for parent
            information. Defaults to None.
        id_col (str, optional): If provided, this column is used as the id
            for sequence records. Defaults to None.

    Returns:
        list: List of floating sequences or (if `id_col` provided) a list
            of SeqRecords
    """
    pss = ParentSeqSerialiser(parent_seq_object=parent_seq)
    if parent_col is None:
        parent_col = start_col
    floating_peptides = table.apply(
        lambda row: _float_epitope(
            start=row[start_col],
            seq=row[seq_col],
            parent_seq=pss.get_parent_seq(row[parent_col]),
            index=index,
        ),
        axis=1,
    )
    # floating_peptides = floating_peptides.apply(Seq.Seq)
    floating_peptides = floating_peptides.tolist()
    if id_col is not None:
        ids = table[id_col]
        floating_peptides = [
            SeqRecord(Seq(seq), id=id) for id, seq in zip(ids, floating_peptides)
        ]
    return floating_peptides


def _score_epitope_alignment(seq, parent_seq, gap="-", toupper=True):
    """Proportion of aligned epitope positions that match the parent sequence

    Args:
        seq (str): Aligned epitope sequence.
        parent_seq (str): Sequence the epitope is aligned to.
        gap (str, optional): Gap characters to ignore.
            Use a list of strings to ignore multiple gap types.
            Defaults to "-".
        toupper (bool, optional): Convert peptide and sequence to upper
            case before comparison. Defaults to True.

    Returns:
        tuple: (score, matches)

        - score (float): The proportion of non-gap epitope positions that
            match the sequence.
        - matches (list): List of booleans for matches of each non-gap position.
    """
    if not len(parent_seq) >= len(seq):
        raise AssertionError(f"The peptide ({seq}) is longer than the parent sequence.")
    if toupper:
        parent_seq = parent_seq.upper()
        seq = seq.upper()
    matches = []
    for parent_seqaa, epiaa in zip(parent_seq, seq):
        if epiaa not in gap:
            matches.append(parent_seqaa == epiaa)
    score = sum(matches) / len(matches)
    return score, matches


def score_epitope_alignments(
    table,
    parent_seq: str | dict,
    seq_col: str,
    parent_col: str | None = None,
    gap: str = "-",
    toupper: bool = True,
):
    """Score alignment between epitopes and parent sequences

    Args:
        table (pd.DataFrame): DataFrame of epitopes
        parent_seq (str | dict): A single parent sequence sting to use for all
            epitopes or a dictionary of multiple epitopes, or "parent_seq_column".
            See epitope_aligner.map.ParentSeqSerialiser for details.
        seq_col (str): Name of the column with epitope sequences in.
        parent_col (str | None, optional): The column with parent sequence
            information. If `parent_seq` is a dictionary the information should
            be keys to the dictionary. If `parent_seq` is the string "parent_seq_column"
            information should be the parent sequence to use. Defaults to None.
        gap (str, optional): Gap characters to ignore.
            Use a list of strings to ignore multiple gap types.
            Defaults to "-".
        toupper (bool, optional): Convert peptide and sequence to upper
            case before comparison. Defaults to True.

    Returns:
        pd.DataFrame: DataFrame with two columns.
            - score (float): The proportion of non-gap epitope positions that
                match the sequence.
            - matches (list): List of booleans for matches of each non-gap position.

    """
    pss = ParentSeqSerialiser(parent_seq_object=parent_seq)
    if parent_col is None:
        parent_col = seq_col
    scores_matches = table.apply(
        lambda row: _score_epitope_alignment(
            seq=row[seq_col],
            parent_seq=pss.get_parent_seq(row[parent_col]),
            gap=gap,
            toupper=toupper,
        ),
        axis=1,
        result_type="expand",
    )
    scores_matches.columns = ["score", "matches"]
    return scores_matches


def locate_epitope(aligned_seq, index, includeend):
    """Get start and end position of epitope in aligned sequence

    Returns the coordinates of the start and end of the epitope,
    i.e. discounting leading and trailing gaps.

    Args:
        aligned_seq (str): The aligned epitope sequence
        index (int): Counting index, i.e. do positions start at 0 or 1?
        includeend (bool): Should the end position be included in the peptide?

    Returns:
        tuple: Start and end positions of the peptide in the provided sequence
    """
    # This regex pattern matches a string with non hypher at start and end and
    # anything inbetween (including hyphens)
    pattern = "[^-].*[^-]"
    aligned_seq = str(aligned_seq)
    start, end = re.search(pattern, aligned_seq).span()
    if index == 1:
        start += 1
        end += 1
    if includeend:
        end -= 1
    return start, end


def _align_coord(
    coordinate: int, aligned_parent_seq: str, index: Literal[0, 1], gap="-"
) -> int:
    """Convert coordinate from unaligned to aligned position

    The position in an unaligned antigen sequence is converted to the
    equivalent position in an aligned version of the antigen sequence.

    Note though that if you use it for the end of a slice (:x) it may
    run to the end of the next gaps.

    Args:
        coordinate (int): Position in an unaligned sequence.
        aligned_parent_seq (str): The aligned version of the sequence.
        index (Literal[0,1]): Counting index, i.e. do the position counts start at
            0 or 1?
        gap (str, optional): Character used for alignment gaps. Defaults to "-".

    Raises:
        Exception: If the new coordinate raises an IndexError and is
            not the length of the sequence (accounting for index).

    Returns:
        int: The new coordinate
    """
    try:
        new_coord = [i for i, aa in enumerate(aligned_parent_seq, index) if aa != gap][
            coordinate - index
        ]
    except IndexError as e:
        if coordinate - index == len(aligned_parent_seq.replace(gap, "")):
            new_coord = len(aligned_parent_seq) + index
        else:
            raise Exception(
                f"{coordinate} not a valid position in ungapped aligned_seq"
            ) from e
    return new_coord


def align_coords(
    table,
    aligned_parent_seq: dict | str,
    coord_col: str,
    index: Literal[0, 1],
    parent_col: str | None = None,
    gap="-",
):
    """Convert column of unaligned coordinates to aligned coordinates.

    The positions in an unaligned antigen sequence are converted to the
    equivalent position in an aligned version of the antigen sequence.

    Note though that if you use it for the end of a slice (:x) it may
    run to the end of the next gaps.

    Args:
        table (pd.DataFrame): Dataframe of epitopes
        aligned_parent_seq (dict | str): Aligned parent sequence or dictionary of
            sequences. A single parent sequence sting to use for all
            epitopes or a dictionary of multiple epitopes, or "parent_seq_column".
            See epitope_aligner.map.ParentSeqSerialiser for details.
        coord_col (str): Name of column containing coordinates in the unaligned
            sequence
        index (Literal[0,1]): Counting index, i.e. do the position counts start at
            0 or 1?
        parent_col (str | None, optional): The column with parent sequence
            information. If `parent_seq` is a dictionary the information should
            be keys to the dictionary. If `parent_seq` is the string "parent_seq_column"
            information should be the parent sequence to use. Defaults to None.
        gap (str, optional): _description_. Defaults to "-".

    Returns:
        Series(int): The new aligned coordinates as a series of integers.
    """
    pss = ParentSeqSerialiser(parent_seq_object=aligned_parent_seq)
    if parent_col is None:
        parent_col = coord_col
    new_coords = table.apply(
        lambda row: _align_coord(
            coordinate=row[coord_col],
            aligned_parent_seq=pss.get_parent_seq(row[parent_col]),
            index=index,
            gap=gap,
        ),
        axis=1,
    )
    return new_coords


def _unalign_coord(
    coordinate: int, aligned_parent_seq: str, index: Literal[0, 1], gap="-"
) -> int:
    """Convert aligned coordinate to unaligned

    Convert a position in an anligned sequence to the equivalent in
    the unaligned sequence.

    Args:
        coordinate (int): the zero-indexed python coordinate
        aligned_parent_seq (str): Aligned sequence the coordinate refers to.
        index (Literal[0, 1]): Counting index, i.e. do the position
            counts start at 0 or 1?
        gap (str, optional):  Character used for alignment gaps. Defaults to "-".

    Returns:
        int: The equivalent coordinate in an unaligned sequence.
    """
    gaps = aligned_parent_seq[: (coordinate - index + 1)].count(gap)
    try:
        aa = aligned_parent_seq[coordinate - index]
    except IndexError:
        aa = None
    if aa == gap:
        gaps -= 1
        logging.warning(
            f"Amino acid at {coordinate} is {gap}\n"
            "Coordinate of gap in ungapped sequence is ambiguous\n"
            "Coordinate of next nongap character will be returned"
        )
    new_coord = coordinate - gaps
    return new_coord


def unalign_coords(
    table,
    aligned_parent_seq: dict | str,
    coord_col: str,
    index: Literal[0, 1],
    parent_col: str | None = None,
    gap="-",
):
    """Convert column of aligned coordinates to unaligned coordinates

    Convert positions in an anligned sequence to the equivalent in
    the unaligned sequence.

    Args:
        table (pd.DataFrame): Dataframe of epitopes
        aligned_parent_seq (dict | str): Aligned parent sequence or dictionary of
            sequences. A single parent sequence sting to use for all
            epitopes or a dictionary of multiple epitopes, or "parent_seq_column".
            See epitope_aligner.map.ParentSeqSerialiser for details.
        coord_col (str): Name of column containing coordinates in the unaligned
            sequence
        index (Literal[0,1]): Counting index, i.e. do the position counts start at
            0 or 1?
        parent_col (str | None, optional): The column with parent sequence
            information. If `parent_seq` is a dictionary the information should
            be keys to the dictionary. If `parent_seq` is the string "parent_seq_column"
            information should be the parent sequence to use. Defaults to None.
        gap (str, optional): _description_. Defaults to "-".

    Returns:
        Series(int): The new aligned coordinates as a series of integers.
    """
    pss = ParentSeqSerialiser(parent_seq_object=aligned_parent_seq)
    if parent_col is None:
        parent_col = coord_col
    new_coords = table.apply(
        lambda row: _unalign_coord(
            row[coord_col],
            aligned_parent_seq=pss.get_parent_seq(row[parent_col]),
            index=index,
            gap=gap,
        ),
        axis=1,
    )
    return new_coords


class ParentSeqSerialiser(object):
    """Get the correct parent sequence for each epitope

    Usually initialised from the `parent_seq` argument of functions like
    `float_epitopes()`. The function gets the needed parent sequence by calling
    the `get_parent_seq()` method. How it gets the parent sequence is based on
    the value of `parent_seq_object` used to initialise the class. 
    
    Attributes:
        parent_seq_object (dict | str):
            
            The parent sequence or sequences for epitopes.
            Can be a dictionary of sequences with parent sequence names as
            keys and sequence strings as values.
            Can be a single sequence as a string if all epitopes share a single
            parent sequence.
            Alternatively can be the string `"parent_seq_column"` if the parent
            sequences are given in a column of the epitope table.
        
        get_parent_seq (function):

            Function used to return the parent seq. The specific function is
            determined by the parent_seq_object at initialisation, as described
            above. For specifics see the `_get_serialiser` method or call
            `help()` on the get_parent_seq attribute.
    """

    def __init__(self, parent_seq_object: dict | str):
        """Initialise the ParentSeqSerializer

        Args:
            parent_seq_object (dict | str): If the `parent_seq_object` is:

                - a dictionary, it should have parent sequence names as
                keys and sequence strings as values. Sequence name is used to get
                sequence.

                - a string, it should usually be a single parent sequence used by
                all epitopes.
                
                - "parent_seq_column", the values in the column `parent_col` (in the
                calling function) are returned as is. This is useful when there is a column
                in your epitope table with parent sequence in.
        """
        self.parent_seq_object = parent_seq_object
        self.get_parent_seq = self._get_serialiser()

    def _serialise_single_seq(self, parent)->str:
        """Returns the parent sequence stored in ParentSeqSerialiser.parent_seq_object

        Args:
            parent: Ignored, likely because ParentSeqSerialiser was initialised 
                with a single sequence.

        Returns:
            str: Single parent sequence used to initialise ParentSeqSerialiser object.
        """
        return self.parent_seq_object

    def _serialise_parent_seq_dict(self, parent:str)->str:
        """Returns the sequence name `parent`

        ParentSeqSerialiser object was initialised with self.parent_seq_object as a
        dictionary. Keys of that dictionary are sequence names, and values are
        sequences. Uses the value of `parent` as a key to return a sequence.

        Args:
            parent (str): Parent sequence name, used as a key

        Raises:
            KeyError: If the value of `parent` is not a key in self.parent_seq_object

        Returns:
            str: Parent sequence
        """
        try:
            return self.parent_seq_object[parent]
        except KeyError as e:
            raise KeyError(
                f"{parent} not a key in parent_seq_object. Did you set `parent_col`?"
            )

    def _serialise_parent_seq_column(self, parent:str)->str:
        """
        Returns the value of `parent` unaltered. Useful when epitopes'
        parent sequences are available in a column.

        Args:
            parent (str): Parent sequence as a string

        Returns:
            str: Returns the value of `parent` unaltered
        """
        return parent

    def _get_serialiser(self):
        """Determines which function to use for the get_parent_seq() method"""
        if isinstance(self.parent_seq_object, dict):
            serialiser = self._serialise_parent_seq_dict
        elif self.parent_seq_object == "parent_seq_column":
            serialiser = self._serialise_parent_seq_column
        else:
            serialiser = self._serialise_single_seq
        return serialiser

"""Stretch epitopes to all the positions they cover
"""

import pandas as pd
from scipy.cluster.hierarchy import linkage, leaves_list
import itertools


def stretch(epitopes, length_col="length", start_col="start", seq_col="seq"):
    """Stretch a table of epitopes so each row is a single epitope position.

    Args:
        epitopes (pd.DataFrame): Table of epitopes where each row is an epitope
        epitopes (_type_): _description_
        length_col (str, optional): Name of column with epitope lengths. Defaults to "length".
        start_col (str, optional): Column with start positions. Defaults to "start".
        seq_col (str, optional): Column with epitope sequence. Defaults to "seq".

    Returns:
        pd.DataFrame: Stretched epitope table.
    """

    stretched = []
    epitopes = epitopes.copy()
    epitopes["position"] = epitopes[start_col]
    for i in range(epitopes[length_col].max()):
        updated_pos = epitopes.copy()
        mask = updated_pos[length_col] > i
        updated_pos = updated_pos[mask]
        updated_pos.position = updated_pos.position + i
        updated_pos["residue"] = updated_pos[seq_col].apply(lambda x: x[i])  #
        stretched.append(updated_pos)
    stretched = pd.concat(stretched)
    stretched = stretched.sort_values([start_col, "position"])
    return stretched


def add_empty_positions(
    series, parent_seq_length, index, empty_value, position_name="position"
):
    """Add empty positions to a series of values.

    Stretched epitopes can be useful for plotting but they do not include
    any information on positions without epitopes. For plotting it can be
    useful to add these in.

    Args:
        series (pd.Series): Series of values to add missing positions to.
        index (int): Counting index, i.e. do positions start at 0 or 1?
        parent_seq_length (int): Length of parent sequence.
        empty_value (any): Value to use for missing positions.
        position_name (str, optional): The name of index which describes the position.
            Defaults to "position".

    Returns:
        pd.Series: The series with missing positions added with `empty_value`s
    """
    if position_name not in series.index.names:
        raise AssertionError(f"Expected {position_name} in series.index.names")
    series = series.copy()
    full_positions = pd.Series(range(index, parent_seq_length + index))
    names = [name for name in series.index.names if name != position_name]
    index_levels = [series.index.unique(name) for name in names]
    for levels in itertools.product(*index_levels):
        series.sort_index(inplace=True)
        try:
            missing_positions = full_positions[
                ~full_positions.isin(series.loc[levels].index)
            ]
        except KeyError:
            # Unclear how this would be triggered
            missing_positions = full_positions.copy()
        for i in missing_positions:
            series.loc[levels + (i,)] = empty_value
    series = series.sort_index()
    return series


def _non_position_index(index, position_col):
    """Get name of index which is not the position index

    Args:
        index (pd.Index): The index to get non-positional name for
        position_col (str): Name of the positional index

    Raises:
        AssertionError: Expects two names

    Returns:
        str: Name of non-positional index
    """
    names = list(index.names)
    if len(names) != 2:
        raise AssertionError(f"Expected two index names, got {names}")
    names.remove(position_col)
    non_position_name = names[0]
    return non_position_name


def order_grid(grid):
    """Order a grid based on similarity

    Useful for plotting as similar rows are placed together

    Args:
        grid (pd.DataFrame): Grid to be ordered

    Returns:
        pd.DataFrame: Ordered grid
    """
    linkage_data = linkage(grid, method="ward", metric="euclidean")
    order = leaves_list(linkage_data)
    ordered_grid = grid.iloc[order]
    return ordered_grid


def make_grid(
    grid_values,
    index,
    parent_seq_length,
    empty_value,
    position_col="position",
    row_col=None,
):
    """Make a grid describing epitopes by position and a grouping value.

    Each column is a position in the sequence, each row is a group value.

    Args:
        grid_values (table): Values, groups, positions in long form to make in to grid.
        index (int): Counting index, i.e. do positions start at 0 or 1?
        parent_seq_length (int): length of the sequence being cast to a grid
        empty_value (any): Value to add for missing values.
        position_col (str, optional): Name of positions. Defaults to "position".
        row_col (str, optional): Name of grouping vector. Defaults to None.

    Returns:
        pd.DataFrame: Grid describing epitopes by position and a grouping value.
    """
    grid_values = add_empty_positions(
        series=grid_values,
        parent_seq_length=parent_seq_length,
        index=index,
        empty_value=empty_value,
    )
    if not row_col:
        row_col = _non_position_index(grid_values.index, position_col=position_col)
        grid_values = grid_values.reset_index()
    grid = grid_values.pivot(index=row_col, columns=position_col)
    grid = order_grid(grid)
    return grid


# def make_empty_grid(stretched, index, row_col, seq_length, default_value):
#     rows = stretched[row_col].unique()
#     cols = range(index, seq_length+index)
#     grid = np.zeros((len(rows), len(cols)))
#     grid = grid + default_value
#     grid = pd.DataFrame(grid)
#     grid.index = rows
#     grid.columns = cols
#     return grid

# def make_grid(stretched, grid_values, index, row_col, seq_length, default_value=0):
#     grid = make_empty_grid(stretched, index, row_col, seq_length, default_value)
#     for i,count in grid_values.items():
#         grid.loc[i[0], i[1]] = count
#     return grid

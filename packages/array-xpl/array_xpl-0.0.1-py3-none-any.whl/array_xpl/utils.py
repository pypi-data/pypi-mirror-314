import numpy as np


def validate_length(opt, min_length=2, err_msg=None):
    if len(opt) < min_length:
        raise ValueError(
            f"At least {min_length} arguments are required, but got {len(opt)}" if err_msg is None else err_msg
        )


def get_keys_ids(tags: list):  # example: ['array', 'frequency'] where 'array' is key and 'frequency' is id
    # tags = [['array', 'frequency'], ['array', 'frequency_2'], ['array', 'frequency_3']]
    keys, ids = [], []
    for a_tag in tags:
        keys.append(a_tag[0])
        if len(a_tag) == 2:
            ids.append(a_tag[1]) if a_tag[1] != "" else ids.append(a_tag[0])
        elif len(a_tag) == 1:
            ids.append(a_tag[0])
        else:
            raise ValueError(f"Invalid tag: {a_tag}")
    return keys, ids


def print_stats(arrays: dict):
    arrays = dict(sorted(arrays.items(), key=lambda item: item[0])) if len(arrays) > 0 else arrays
    info_ = []
    for kk, vv in arrays.items():
        info_.append([kk, vv.shape])
        if vv.dtype in (np.int32, np.int64):
            info_[-1].extend([f"{i:4.3f}" for i in (vv.min(), vv.max(), vv.mean(), vv.std())])
        elif vv.dtype in (np.float32, np.float64):
            info_[-1].extend([f"{i:4.3e}" for i in (vv.min(), vv.max(), vv.mean(), vv.std())])
        else:
            info_[-1].extend([f"{i:4s}" for i in ("-", "-", "-", "-")])
    print_table(info_, header=["Key", "Shape", "Min", "Max", "Mean", "Std"])


def pretty_print(row, cell_width, sep="|"):
    print(sep + sep.join([f"{a_cell:^{cell_width}}" for a_cell in row]) + sep)


def print_table(contents: list[list], header: list = None, pad=1):
    contents = [[f'{j}' for j in i] for i in contents]
    # print(contents)
    # n_rows = len(contents)
    assert all([len(contents[0]) == len(i) for i in contents]), "Unequal number of columns"
    n_col = len(contents[0])
    columns = [[] for _ in range(n_col)]
    for a_row in contents:
        for (col_idx, a_col) in enumerate(a_row):
            columns[col_idx].append(a_col)
    # print(columns)
    min_cell_width = max(len(j) for i in columns for j in i)
    cell_width = min_cell_width + (2 * pad)
    # print(cell_width)

    print("=" * (n_col * cell_width + 4))
    if header is not None:
        assert len(header) == n_col, "Unequal number of columns and headers"
        pretty_print(header, cell_width)
    print("=" * (n_col * cell_width + 4))
    for a_row in contents:
        pretty_print(a_row, cell_width)
    print("=" * (n_col * cell_width + 4))
    return


def print_arr(arr, tag=None):
    print(f"\n{'-' * 80}")
    print(f"\t\tArray{'' if tag is None else ' of ' + tag}\n>> Shape: {arr.shape}\t>> Dtype: {arr.dtype}")
    print(arr)
    print(f"{'-' * 80}\n")


def slices(num_dim: int, idx_range=None):
    if idx_range is not None:
        assert len(idx_range) % 2 == 0, "len(i_range) should be even with pairs of min and max indices"
        assert len(idx_range) // 2 == num_dim, "len(i_range) should be equal to 2 * num_dim"
        return tuple(
            slice(min_index, max_index + 1) for min_index, max_index in zip(idx_range[::2], idx_range[1::2])
        )
    else:
        return tuple(slice(None) for _ in range(num_dim))

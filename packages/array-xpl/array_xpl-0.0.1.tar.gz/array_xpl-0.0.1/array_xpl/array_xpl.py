"""
This module implements commandline operations for working with data stored in .npy and .npz files

Author: Rajesh Nakka
Date: 16/04/2024
"""

import numpy as np
from tabulate import tabulate

import argparse
import json
import glob
from os import path, makedirs


# import utils
# import eval_metrics
# import plotter
# import file_ops

NumPyArray = np.ndarray


# def key_pattern_rules():
#     return """
#     \tKeys must follow these rules:
#     One can pass multiple keys to access various keys of the NPZ file.
#     Each Key is should follow a pattern of <key>#<mn0:mx0>#<mn1:mx1>#.......#<mnN:mxN>.
#     In case of numpy array of .npy file, key is ignored, 
#     Note1: Pattern shouldn't end with #
#     Note2: In case of .npz file, key is required.
#     Note3: In case of .npy file range of axed can be passed as #<mn0:mx0>#<mn1:mx1>#.......#<mnN:mxN>.
#     Note4: : is used to indicate all the indices.
#     Note5: If no range is provided, it will be considered as :.
#     """


# def filter_data_by_key(data_: dict, ids):
#     def get_key_tag(ak, idx=None):
#         k_spl = ak.split("#")
#         ar_kt = k_spl[0].split('@')
#         tag = ar_kt[0] + f"{idx}" if (len(ar_kt) == 1 or ar_kt[1] == "") else ar_kt[1]
#         return ar_kt[0], tag, k_spl[1:]

#     filtered_data = {}
#     keys = []
#     for (id_count, a_key) in enumerate(ids):
#         arr_key, arr_tag, ind_keys = get_key_tag(a_key, id_count)
#         # print(arr_key, arr_tag, ind_keys)
#         assert arr_key in data_.keys(), f"{arr_key} not found in the data. Expecting one of {data_.keys()}"
#         value = data_[arr_key]
#         #
#         assert len(ind_keys) <= len(value.shape), f"Invalid key: {a_key}; {key_pattern_rules()}"
#         ind_keys = [(":" if ind_key == "" else ind_key) for ind_key in ind_keys]  # adding all indices for missing dims
#         for _ in range(len(ind_keys), len(value.shape)):  # adding all the indices of unspecified dimensions
#             ind_keys.append(":")
#         slices = []
#         for a_axis_info in ind_keys:
#             if a_axis_info.strip('-').isdigit():
#                 slices.append(int(a_axis_info))
#             else:
#                 indices = [(None if a_ax_ind == "" else int(a_ax_ind)) for a_ax_ind in a_axis_info.split(":")]
#                 slices.append(slice(*indices))
#         filtered_data[arr_tag] = value[tuple(slices)]
#         keys.append(arr_tag)
#     return filtered_data, keys


# def find_data(data_: dict):
#     for a_val in args.search:
#         print(f"Looking for {a_val}") if args.verbose > 10 else None
#         condition = eval('lambda x: x ' + str(a_val))
#         for (k, v) in data_.items():
#             indices = np.stack(np.nonzero(condition(v)), axis=1)
#             print(f"{'-' * 40}")
#             if len(indices) == 0:
#                 print(f"\tNo match found for {a_val} in {k}")
#             else:
#                 print(f"\tMatch found for x {a_val} in {k}")
#                 print(indices)


# def transform_data(data_: dict):
#     out = {}
#     for k, v in data_.items():
#         v = v if args.scale is None else (v * args.scale)
#         v = v if args.shift is None else (v + args.shift)
#         if args.sig_dig is not None and v.dtype.kind == "f":
#             v = np.around(v, decimals=args.sig_dig)
#         out[k] = v
#     return out


# def stack_data(data_: dict):
#     if args.stack is None:
#         return data_
#     assert len(args.stack) > 2, (
#         "At least 3 arguments are required, while the last argument is the axis for stacking "
#         "the arguments until the last one "
#     )
#     stacking_axis = int(args.stack[-1])
#     data_, _ = filter_data_by_key(data_, args.stack[:-1])
#     return {"A": np.stack(list(data_.values()), axis=stacking_axis), "keys": list(data_.keys())}


# def view_data(data_: dict):
#     if args.summary:
#         def get_row_ele(k, v):
#             if v.dtype.kind == "f":
#                 mn, mx, mean_, std_ = v.min(), v.max(), v.mean(), v.std()
#                 if args.sig_dig is not None:
#                     mn = np.around(mn, decimals=args.sig_dig)
#                     mx = np.around(mx, decimals=args.sig_dig)
#                     mean_ = np.around(mean_, decimals=args.sig_dig)
#                     std_ = np.around(std_, decimals=args.sig_dig)
#                 return [k, v.dtype, v.shape, mn, mx, mean_, std_]
#             else:
#                 return [k, v.dtype, v.shape, "-", "-", "-", "-"]

#         info = [get_row_ele(k, v) for (k, v) in data_.items()]
#         headers = ["Key", "Data Type", "Shape", "Min", "Max", "Mean", "Std. Dev"]
#         table = tabulate(info, headers=headers, tablefmt=args.table_fmt, floatfmt="4.3f")
#         table = f"Summary of {path.basename(args.fp)}:\n{table}\n"
#         print(table)

#     for (a_key, a_val) in data_.items():
#         utils.print_arr(a_val, tag=a_key) if args.print else None


# def plot_data(data_: dict):
#     if len(data_) == 0:
#         print(f""
#               f"\n\nNo data is found!\nPlease provide for plotting..!\n"
#               f"(May be you missed providing keys of NPZ file)\n")
#         return
#     if args.line_plot_keys is not None:
#         utils.validate_length(args.line_plot_keys, min_length=1)
#         data_, keys = filter_data_by_key(data_, args.line_plot_keys)
#         xs = {k.strip("x::"): data_[k] for k in keys if k.startswith("x::")}
#         ys = {k.strip("y::"): data_[k] for k in keys if k.startswith("y::")}
#         plotter.line_plot(xs, ys, args.line_plot_options, args)
#     elif args.hist1d_keys is not None:
#         utils.validate_length(args.hist1d_keys, min_length=1)
#         data_, keys = filter_data_by_key(data_, args.hist1d_keys)
#         plotter.histogram_1d_plot(data_, args.hist1d_options, args)
#     elif args.scatter_options is not None:
#         utils.validate_length(args.scatter_options, min_length=2)
#         data_, keys = filter_data_by_key(data_, args.scatter_options[0:2])
#         sct_opt = [] if len(args.scatter_options) == 2 else args.scatter_options[2:]
#         plotter.scatter_plot(data_[keys[0]], data_[keys[1]], sct_opt, args, tags=keys)
#     elif args.scatter3D_opt is not None:
#         utils.validate_length(args.scatter3D_opt, min_length=3)
#         data_, keys = filter_data_by_key(data_, args.scatter3D_opt[0:3])
#         sct_opt = [] if len(args.scatter3D_opt) == 3 else args.scatter3D_opt[3:]
#         plotter.scatter_plot_3d(data_[keys[0]], data_[keys[1]], data_[keys[2]], sct_opt, args, tags=keys)
#     else:
#         pass


# def save_data(data_: dict | NumPyArray):
#     if not (args.saveas is not None or args.saveas_json or args.saveas_dat):
#         return
#     if args.saveas_json or args.saveas_dat:
#         assert args.log_dir is not None, "Please provide log_dir for saving the data"
#         makedirs(args.log_dir, exist_ok=True)
#     if args.saveas_json:
#         for k, v in data_.items():
#             if isinstance(v, np.ndarray):
#                 data_[k] = v.tolist()
#         with open(path.join(args.log_dir, f"data.json"), "w") as fp:
#             json.dump(data_, fp)
#     elif args.saveas_dat:
#         for k, v in data_.items():
#             np.savetxt(path.join(args.log_dir, f"{k}.dat"), v, fmt="%4.8e", delimiter="     ")
#     elif args.saveas is not None:
#         if args.saveas.endswith(".npz"):
#             np.savez_compressed(args.saveas, **data_)
#     else:
#         pass


# def file_operations(files_: list[str]):
#     if args.merge:
#         utils.validate_length(files_, min_length=2)
#         file_ops.merge(files, args.saveas, args)
#     return


# def metrics(data_: dict):
#     if args.r2score_yp_yt is not None:
#         utils.validate_length(args.r2score_yp_yt, min_length=2)
#         data_, tags = filter_data_by_key(data_, args.r2score_yp_yt[0:2])
#         r2s_opt = [] if len(args.r2score_yp_yt) == 2 else args.r2score_yp_yt[2:]
#         print(f"\nR2 Score: {eval_metrics.r2_score(data_[tags[0]], data_[tags[1]], r2s_opt)}\n")


# def get_data_dictionary(fp: str, def_key="A"):
#     assert path.exists(fp), f"{fp} does not exist"
#     data = np.load(fp)
#     if isinstance(data, np.lib.npyio.NpzFile):  # Check if .npz file
#         arr_dict = {kk: vv for kk, vv in data.items()}
#     elif isinstance(data, np.ndarray):  # Check if .npy file
#         arr_dict = {def_key: data}
#     else:
#         raise Exception(f"{fp} is not a .npy or .npz file")
#     return arr_dict


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fp", type=str)
    #
    # =================================
    #           General
    # =================================
    #
    parser.add_argument("--key", type=str, nargs='+', default=None, help="")
    parser.add_argument("--tag", type=str, default='A')
    parser.add_argument("--verbose", type=int, default=0)
    #
    # =================================
    #           Find
    # =================================
    parser.add_argument("--search", type=str, nargs='+', default=())
    #
    # =================================
    #           Manipulations
    # =================================
    parser.add_argument("--cat", type=str, nargs='+', default=None)
    parser.add_argument("--stack", type=str, nargs='+', default=None)
    #
    # =================================
    #           View
    # =================================
    parser.add_argument("--summary", action="store_true", help="summarize the data")
    parser.add_argument("--sig_dig", type=int, default=None, help="number of significant digits")
    parser.add_argument("--print", action="store_true", help="print the data")
    parser.add_argument("--p_bar", action="store_true", help="show a progress bar")
    parser.add_argument("--table_fmt", type=str, default="grid")
    #
    # =================================
    #           Evaluations
    # =================================
    parser.add_argument("--r2_score", dest='r2score_yp_yt', nargs='+', default=None, help="R^2 score of two arrays")
    parser.add_argument("--find_sample_size", nargs='+', type=str, default=None)
    #
    # =================================
    #           Plotting
    # =================================
    parser.add_argument("-p", "--plot", action="store_true", help="plot the data")
    #
    parser.add_argument("--line_plot", dest="line_plot_keys", nargs='+', type=str, default=None)
    parser.add_argument("--line_plot_opt", dest="line_plot_options", nargs='+', type=str, default=None)
    #
    # Histogram plots
    parser.add_argument("--hist1D", dest="hist1d_keys", nargs='+', type=str, default=None)
    parser.add_argument("--hist1D_opt", dest="hist1d_options", nargs='+', type=str, default=None)
    parser.add_argument("--get_frequency", action="store_true", help="get the frequency of the data")
    #
    # Scatter plots  # TODO make it consistent with the rest
    parser.add_argument("--scatter", dest="scatter_options", nargs='+', type=str, default=None)
    parser.add_argument("--scatter3D", dest="scatter3D_opt", nargs='+', type=str, default=None)
    # Image plots
    parser.add_argument("--image_plot", action="store_true", help="view the data as images")
    #
    parser.add_argument("--no_pool", action="store_true", help="pool the plots on a single figure")
    #
    parser.add_argument("--fig_size", nargs=2, type=int, default=(6, 6))
    parser.add_argument("--add_grid", action="store_true", help="add a grid")
    parser.add_argument("--x_label", type=str, default=None)
    parser.add_argument("--y_label", type=str, default=None)
    parser.add_argument("--x_lim", nargs=2, type=float, default=None)
    parser.add_argument("--y_lim", nargs=2, type=float, default=None)
    parser.add_argument("--y_log", action="store_true", help="y-axis in log scale")
    parser.add_argument("--eq_axs", action="store_true", help="equal axis")
    parser.add_argument("--title", type=str, default=None)
    parser.add_argument("--no_axs", action="store_true", help="no axes")
    parser.add_argument("--tight_layout", action="store_true", help="tight layout")

    # =================================
    #           Transformations
    # =================================
    parser.add_argument("--scale", type=float, default=None)
    parser.add_argument("--shift", type=float, default=None)

    # =================================
    #           File Operations
    # =================================
    parser.add_argument("--merge", type=str, nargs='+', default=None)
    parser.add_argument("--append", type=str, nargs='+', default=None)
    parser.add_argument("--remove", type=str, nargs='+', default=None)
    parser.add_argument("--rename", type=str, nargs='+', default=None)

    # =================================
    #           Save
    # =================================
    parser.add_argument("-s", "--saveas", type=str, default=None)
    parser.add_argument("--saveas_json", action="store_true")
    parser.add_argument("--saveas_dat", action="store_true")
    parser.add_argument("--log_dir", type=str, default=None)
    #
    args = parser.parse_args()
    print(args)


if __name__ == "__main__":
    main()
    

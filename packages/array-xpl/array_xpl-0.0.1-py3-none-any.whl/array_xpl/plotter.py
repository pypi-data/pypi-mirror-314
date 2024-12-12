import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

NumpyArray = np.ndarray


def line_plot(xs: dict, ys: dict, lp_options, options):
    lp_options = () if lp_options is None else lp_options
    kwargs = {}  # prepare kwargs for matplotlib.pyplot.plot
    for a_opt in lp_options:  # Collect kwargs for matplotlib.pyplot.plot
        a_opt_k, a_opt_v = [i.strip() for i in a_opt.split("=")]
        if a_opt_k in ("c", "color"):
            kwargs["color"] = a_opt_v
        elif a_opt_k in ("ls", "linestyle"):
            kwargs["linestyle"] = a_opt_v
        elif a_opt_k in ("lw", "linewidth"):
            kwargs["linewidth"] = float(a_opt_v)
        elif a_opt_k in ("alpha", "a"):
            kwargs["alpha"] = float(a_opt_v)
        elif a_opt_k in ('marker', 'm'):
            kwargs["marker"] = a_opt_v
        elif a_opt_k in ('ms', 'markersize'):
            kwargs["markersize"] = float(a_opt_v)
        elif a_opt_k in ('mfc', 'markerfacecolor'):
            kwargs["markerfacecolor"] = a_opt_v
        elif a_opt_k in ('mec', 'markeredgecolor'):
            kwargs["markeredgecolor"] = a_opt_v
        else:
            raise ValueError(f"Unknown option: {a_opt}")
    if options.no_pool:
        raise NotImplementedError(f"No Pooling is not implemented yet.")
    else:  # pooling, by default
        fig, axs = plt.subplots(nrows=1, ncols=1, figsize=options.fig_size)
        #
        if len(ys) == 0:
            for (a_xs_label, a_xs_arr) in xs.items():
                axs.plot(a_xs_arr, label=a_xs_label, **kwargs)
        elif len(xs) == 1 and len(ys) >= 1:
            for (a_ys_label, a_ys_arr) in ys.items():
                axs.plot(xs[list(xs.keys())[0]], a_ys_arr, label=a_ys_label, **kwargs)
        elif len(xs) > 1 and len(ys) > 1:
            assert len(xs) == len(ys), f"Unequal number of xs and ys, {len(xs)} != {len(ys)}."
            for ((a_xs_label, a_xs_arr), (a_ys_label, a_ys_arr)) in zip(xs.items(), ys.items()):
                axs.plot(a_xs_arr, a_ys_arr, label=a_ys_label, **kwargs)
        else:
            raise ValueError()
        #
        axs.legend(loc='best')
        update_fig_axes(fig, axs, options)
        fig.savefig(options.saveas) if options.saveas else plt.show()


def histogram_1d_plot(data_: dict, hist_options, options):
    num_hist = len(data_)
    fig_size = (num_hist * options.fig_size[0], options.fig_size[0])
    fig_, axs_ = plt.subplots(nrows=1, ncols=num_hist, figsize=fig_size, squeeze=False)
    hist_options = () if hist_options is None else hist_options
    kwargs = {}
    for a_opt in hist_options:  # Collect kwargs for matplotlib.pyplot.hist
        a_opt_k, a_opt_v = [i.strip() for i in a_opt.split("=")]
        if a_opt_k in ("c", "color"):
            kwargs["color"] = a_opt_v
        elif a_opt_k in ("bins", "bin"):
            kwargs["bins"] = int(a_opt_v)
        elif a_opt_k in ("rwidth", "rw"):
            kwargs["rwidth"] = float(a_opt_v)
        elif a_opt_k in ("alpha", "a"):
            kwargs["alpha"] = float(a_opt_v)
        elif a_opt_k in ('cmap',):
            kwargs["cmap"] = a_opt_v
        elif a_opt_k in ('ec', 'edgecolor'):
            kwargs["edgecolor"] = a_opt_v
        elif a_opt_k == "hatch":
            kwargs["hatch"] = a_opt_v
        else:
            pass
    for (idx, (a_tag, a_arr)) in enumerate(data_.items()):
        frq, bins, _ = axs_[0, idx].hist(a_arr.ravel(), **kwargs)
        axs_[0, idx].set_title(a_tag)
        if options.get_frequency:
            print(f"Frequencies of {a_tag}")
            ln = f"{'bins':^25s}: {'frequency':^10s}"
            print(f"{'*'*len(ln)}\n{ln}\n{'*'*len(ln)}")
            for (jdx, a_frq) in enumerate(frq):
                print(f"[{bins[jdx]:^10.4f}, {bins[jdx+1]:^10.4f}] : {a_frq:^10.2f}")

    update_fig_axes(fig_, axs_, options)
    plt.tight_layout()
    fig_.savefig(options.saveas) if options.saveas is not None else plt.show()


def scatter_plot(x, y, scatter_options, options, tags=None, ):
    fig, axs = plt.subplots(figsize=options.fig_size)
    # prepare scatter options
    kwargs = {}
    for a_opt in scatter_options:
        a_opt_k, a_opt_v = [i.strip() for i in a_opt.split("=")]
        if a_opt_k in ("c", "color"):
            kwargs["c"] = a_opt_v
        elif a_opt_k in ("s", "size"):
            kwargs["s"] = float(a_opt_v)
        elif a_opt_k in ("marker",):
            kwargs["marker"] = a_opt_v
        elif a_opt_k in ("alpha", "a"):
            kwargs["alpha"] = float(a_opt_v)
        elif a_opt_k in ('cmap',):
            kwargs["cmap"] = a_opt_v
        elif a_opt_k in ('vmin',):
            kwargs["vmin"] = float(a_opt_v)
        elif a_opt_k in ('vmax', 'cmax'):
            kwargs["vmax"] = float(a_opt_v)
        elif a_opt_k in ('edgecolors', 'ec'):
            kwargs["edgecolors"] = a_opt_v
        elif a_opt_k in ('linewidths', 'lw'):
            kwargs["linewidths"] = float(a_opt_v)
        else:
            raise NotImplementedError(f"Unsupported option: {a_opt}")
    axs.scatter(x, y, **kwargs)
    axs.set_xlabel(tags[0]) if tags is not None else None
    axs.set_ylabel(tags[1]) if tags is not None else None
    update_fig_axes(fig, axs, options)
    fig.savefig(options.saveas) if options.saveas else plt.show()


def scatter_plot_3d(x, y, z, scatter_options, options, tags=None, ):
    fig = plt.figure(figsize=options.fig_size)
    axs = fig.add_subplot(111, projection='3d')
    # prepare scatter options
    kwargs = {}
    for a_opt in scatter_options:
        a_opt_k, a_opt_v = [i.strip() for i in a_opt.split("=")]
        if a_opt_k in ("c", "color"):
            kwargs["c"] = a_opt_v
        elif a_opt_k in ("s", "size"):
            kwargs["s"] = float(a_opt_v)
        elif a_opt_k in ("marker",):
            kwargs["marker"] = a_opt_v
        elif a_opt_k in ("alpha", "a"):
            kwargs["alpha"] = float(a_opt_v)
        elif a_opt_k in ('cmap',):
            kwargs["cmap"] = a_opt_v
        elif a_opt_k in ('vmin',):
            kwargs["vmin"] = float(a_opt_v)
        elif a_opt_k in ('vmax', 'cmax'):
            kwargs["vmax"] = float(a_opt_v)
        elif a_opt_k in ('edgecolors', 'ec'):
            kwargs["edgecolors"] = a_opt_v
        elif a_opt_k in ('linewidths', 'lw'):
            kwargs["linewidths"] = float(a_opt_v)
        else:
            raise NotImplementedError(f"Unsupported option: {a_opt}")

    axs.scatter(x, y, z, **kwargs)
    if tags is not None:
        axs.set_xlabel(tags[0])
        axs.set_ylabel(tags[1])
        axs.set_zlabel(tags[2])
    plt.show()


def update_fig_axes(fig_, axs_, args):
    if args.no_axs:
        axs_.axis("off")
        return
    if args.eq_axs:
        axs_.set_aspect("equal")
    if args.add_grid:
        axs_.grid()
    if args.x_label is not None:
        axs_.set_xlabel(args.x_label)
    if args.y_label is not None:
        axs_.set_ylabel(args.y_label)
    if args.x_lim is not None:
        axs_.set_xlim(args.x_lim)
    if args.y_lim is not None:
        axs_.set_ylim(args.y_lim)
    if args.title is not None:
        axs_.set_title(args.title)
    if args.y_log:
        axs_.set_yscale("log")
    if args.tight_layout:
        fig_.tight_layout()

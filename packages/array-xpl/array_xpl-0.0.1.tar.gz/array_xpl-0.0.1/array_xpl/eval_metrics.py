import numpy as np


def r2_score(y_p, y_t, opt):
    options = {'axis': None}
    for a_opt in opt:
        a_opt_k, a_opt_v = [i.strip() for i in a_opt.split("=")]
        options['axis'] = int(a_opt_v) if a_opt_k in ("axis",) else None

    y_mean = np.mean(y_t, axis=options['axis'])
    ss_tot = np.sum((y_t - y_mean) ** 2, axis=options['axis'])
    ss_res = np.sum((y_t - y_p) ** 2, axis=options['axis'])
    return 1 - (ss_res / ss_tot)

import numpy as np
from tqdm import tqdm


def merge(files: list[str], output_file_path: str, options):
    opf_extension = output_file_path.split(".")[-1]
    loop = tqdm(files, ascii=False, leave=False) if options.p_bar else files
    if opf_extension == "npz":
        if options.p_bar:
            loop.desc = "[Combining npz files ...]"
        else:
            print("[Combining npz files ...]")

        # Collecting the data in dictionary
        combined_data: dict[str, list | np.ndarray] = {}
        for a_file in loop:
            if not a_file.endswith(opf_extension):
                continue
            file_data = np.load(a_file)
            for (k, v) in file_data.items():
                # v = np.array(v)
                v = np.array([v]) if v.ndim == 0 else v
                if k in combined_data.keys():
                    combined_data[k].append(v)
                else:
                    combined_data[k] = [v]

        # Combining the data
        for (k, v) in combined_data.items():
            try:
                combined_data[k] = np.stack(v, axis=0).squeeze()
            except ValueError as e:
                print(f"Unable to stack {k} due to {e}")
        print(f"Combined data len: {len(combined_data)}") if options.verbose > 1 else None
        print("Individual key len: ", [len(v) for k, v in combined_data.items()]) if options.verbose > 10 else None
        np.savez(output_file_path, **combined_data)
    else:
        raise NotImplementedError(f"File format not supported: {opf_extension}")


def append(s, d):
    return


def rename_key(data: dict, old_key: str, new_key: str):
    return

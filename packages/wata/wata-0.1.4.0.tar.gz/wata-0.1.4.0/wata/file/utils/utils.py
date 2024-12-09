import os
from pathlib import Path
import numpy as np
from wata.file.utils import load_and_write_file


def load_file(path):
    file_ext = Path(path).suffix[1:]
    if file_ext in ['yaml', 'json', 'geojson', 'pkl', 'txt']:
        return eval('load_and_write_file.load_' + file_ext)(path)
    else:
        raise NameError("Unable to handle {} formatted files".format(file_ext))

def save_file(data, save_path):
    file_ext = Path(save_path).suffix[1:]
    if file_ext in ['yaml', 'json', 'pkl', 'txt']:
        return eval('load_and_write_file.write_' + file_ext)(data, save_path)
    else:
        raise NameError("Unable to handle {} formatted files".format(type))

def mkdir_if_not_exist(path):
    if not os.path.exists(path):
        os.makedirs(path)

def np2str(arr, return_type='list'):
    if isinstance(arr, list):
        arr = np.array(arr)
    if arr.ndim == 1:
        string = ' '.join(map(str, arr))
        return string

    elif arr.ndim == 2:
        string_list = []
        for arr_line in arr:
            string = ' '.join(map(str, arr_line)) + "\n"
            string_list.append(string)
        if return_type =='str':
            string = str(string_list)[2:-2].replace("', '", "").replace("\\n", "\n")
            return string
        elif return_type =='list':
            return string_list
        else:
            raise ValueError("Only 'str' and 'list' can be selected for return_type")
    else:
        raise ValueError("Only supports arrays of 2 dimensions and below")

def is_empty_directory(directory):
    assert isinstance(directory, Path),"This path is not a directory"
    return len(os.listdir(directory)) == 0


def delete_empty_directories(directory):
    path = Path(directory)
    for dir_to_check in path.rglob('*'):
        if dir_to_check.is_dir() and not any(dir_to_check.iterdir()):
            dir_to_check.rmdir()

def get_sorted_files(directory="."):
    files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    files.sort()
    return files

def get_sorted_directories(directory="."):
    dirs = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    dirs.sort()
    return dirs
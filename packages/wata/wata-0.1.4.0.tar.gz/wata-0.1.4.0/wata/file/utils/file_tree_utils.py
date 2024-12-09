import os
from pathlib import Path


def recursive_file_path(path):
    path_dict = {}
    num_dict = {}
    for foldername, subfolders, filenames in os.walk(path):
        if not subfolders:
            num_dict[foldername] = len(filenames)

        display_filenames = [os.path.join(foldername, file) for file in filenames[:2]]
        if len(filenames) > 10:
            display_filenames.append(os.path.join(foldername, '......'))

        display_subfolders = [os.path.join(foldername, folder) for folder in subfolders[:15]]
        path_dict[foldername] = [display_subfolders, display_filenames]

    return path_dict, num_dict


def recursion(dict, key, output, num, root_name):
    for k, i in enumerate(dict[key][0]):  # dir
        datai = os.path.relpath(i, root_name)
        datai_sp = datai.split(os.sep)
        if i in num.keys() and num[i] > 80:
            output.append((len(datai_sp) - 1) * '│  ' + "├── " + "{:20}".format(datai_sp[-1]) + "({})".format(num[i]))
        else:
            output.append((len(datai_sp) - 1) * '│  ' + "├── " + datai_sp[-1])

        recursion(dict, i, output, num, root_name)
    for k, i in enumerate(dict[key][1]):  # file
        datai = os.path.relpath(i, root_name)
        datai_sp = datai.split(os.sep)
        if k == len(dict[key][1]) - 1:
            output.append((len(datai_sp) - 1) * '│  ' + "└── " + datai_sp[-1])
        else:
            output.append((len(datai_sp) - 1) * '│  ' + "├── " + datai_sp[-1])


def file_tree(datasets_path, save_path=None):
    root_name = datasets_path
    dict, num = recursive_file_path(datasets_path)
    output = [Path(root_name).name]
    recursion(dict, datasets_path, output, num, root_name)
    for i in output:
        print(i)

    if save_path is not None:
        with open(save_path, 'w', encoding='utf-8') as f:
            for line in output:
                f.write(line + '\n')
        print('\n', save_path + " has been saved!")


if __name__ == '__main__':
    file_tree("D:\Code\wata")

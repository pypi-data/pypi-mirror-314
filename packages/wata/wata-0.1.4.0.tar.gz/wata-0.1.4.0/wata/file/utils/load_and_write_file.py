import yaml
import json
import pickle
import os


def load_yaml(path):
    with open(path, 'r', encoding='UTF-8') as f:
        yaml_datas = yaml.load(f.read(), Loader=yaml.FullLoader)
    return yaml_datas


def write_yaml(data, save_path):
    yaml_data = yaml.dump(data)
    with open(save_path, 'w', encoding='UTF-8') as f:
        f.write(yaml_data)


def load_json(path):
    with open(path, 'r', encoding='UTF-8') as f:
        json_datas = json.loads(f.read())
    return json_datas

def load_geojson(path):
    with open(path, 'r', encoding='UTF-8') as f:
        json_datas = json.loads(f.read())
    return json_datas


def write_json(data, save_path):
    json_data = json.dumps(data, indent=4, ensure_ascii=False)
    with open(save_path, 'w', encoding='UTF-8') as f:
        f.write(json_data)


def load_pkl(path):
    with open(path, 'rb') as f:
        pkl_datas = pickle.load(f)
    return pkl_datas


def write_pkl(data, save_path):
    with open(save_path, 'wb') as f:
        pickle.dump(data, f)


def load_txt(path):
    with open(path, 'r', encoding='UTF-8') as f:
        lines = f.readlines()
        content = [line.rstrip() for line in lines]
    return content


def write_txt(data, save_path):
    with open(save_path, 'w', encoding='UTF-8') as f:
        if isinstance(data,str):
            f.write(data)
        elif isinstance(data,list):
            for res in data:
                if str(res)[-1:] != '\n':
                    f.write(str(res) + '\n')
                else:
                    f.write(str(res))
        else:
            raise ValueError("Only str and list can be selected for data")
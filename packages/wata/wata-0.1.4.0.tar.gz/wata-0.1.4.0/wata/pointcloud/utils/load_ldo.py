# from decodelidardata import decode_lidar

import pathlib
import pandas as pd
import numpy as np
from numpy.lib import recfunctions
import wata

LIDAR_COLUMN_NAMES = ['x', 'y', 'z', 'intensity', 'lidar_identifier', 'delta_time',
                      'Class', 'ID', 'lidar_mat_id', 'normal_cos', 'part_id', 'point_idx',
                      'reference_reflectivity', 'nominator', 'denominator', 'reference_distance',
                      'normal angle theta', 'normal angle phi']

MINUS_FILL = ['Class', 'ID']

ZERO_FILL = ['x', 'y', 'z', 'intensity', 'lidar_identifier', 'delta_time', 'lidar_mat_id', 'normal_cos',
             'part_id', 'point_idx', 'reference_reflectivity', 'nominator', 'denominator', 'reference_distance',
             'normal angle theta', 'normal angle phi']

DROPPED_FIELDS = ['classInstance', 'StructurePointindex', 'fillfactor', 'place holder1',
                  'place holder2', 'place holder3', 'place holder4', 'place holder5', 'place holder6',
                  'place holder7']


def decodeLidarFile(file, withMeta=True):
    """
    Previous signature, kept for backwards compatibility

    :param file: full path to point_cloud file
    :param withMeta: depricated bool
    :return:
    """
    return decode_lidar(file)


def get_lidar_dtype(extension: str) -> np.dtype:
    """
    Constructs a point_cloud parsing np.dtype according to file extension

    :param extension: point_cloud file extension, valid exentions are 'ldo'/'ldg'/'ldx',
    passing an invalid string will raise a ValueError

    :return: np.dtype that can be used to parse the file with all fields
    """
    if extension not in ["ldo", "ldg", "ldx"]:
        raise ValueError(f"Invalid flie type passed: {extension}")

    lidar_dtype = [('x', np.float32), ('y', np.float32), ('z', np.float32),
                   ('delta_time', np.float16),
                   ('lidar_identifier', np.uint8),
                   ('intensity', np.uint8)]

    if extension != 'ldo':
        lidar_dtype.extend([('classInstance', np.uint32),
                            ('lidar_mat_id', np.uint16),
                            ('normal_cos', np.float16),
                            ('StructurePointindex', np.uint32),
                            ('reference_distance', np.float16),
                            ('fillfactor', np.uint8),
                            ('reference_reflectivity', np.uint8)])
        if extension != 'ldg':
            lidar_dtype.extend([('normal angle theta', np.float16),
                                ('normal angle phi', np.float16),
                                ('place holder1', np.float32),
                                ('place holder2', np.float32),
                                ('place holder3', np.float32),
                                ('place holder4', np.float32),
                                ('place holder5', np.float32),
                                ('place holder6', np.float32),
                                ('place holder7', np.float32)])

    return np.dtype(lidar_dtype)


def decode_lidar(file: str, extension: str = '') -> pd.DataFrame:
    """
    Decode Lidar binary 拼接点云.py and returns pd dataframe

    :param file: absolute path to binary point_cloud 拼接点云.py file
    :param extension: optional - indicates type of point_cloud file (valid values: 'ldo','ldg','ldx')

    :return: dataframe holding the parsed point_cloud 拼接点云.py
    """
    if not extension:
        extension = pathlib.Path(file).suffix[1:]
    lidar_dtype = get_lidar_dtype(extension)
    data = np.fromfile(file, lidar_dtype)
    if extension != 'ldo':
        # separate combo values
        object_class = data['classInstance'] >> 24
        object_instance = data['classInstance'] & 0xffffff
        object_structure = data['StructurePointindex'] >> 24
        object_pointindex = data['StructurePointindex'] & 0xffffff
        fill_nominator = (data['fillfactor'] >> 4) + 1
        fill_denominator = (data['fillfactor'] & 0xf) + 1
        # remove unneeded fields and add intensity and ring to 拼接点云.py structure
        data = recfunctions.drop_fields(data, DROPPED_FIELDS)
        data = recfunctions.append_fields(data, ['Class', 'ID', 'part_id', 'point_idx', 'nominator', 'denominator'],
                                          [object_class, object_instance, object_structure, object_pointindex,
                                           fill_nominator, fill_denominator])
    data = pd.DataFrame.from_records(data).reindex(LIDAR_COLUMN_NAMES, axis=1)
    data[ZERO_FILL] = data[ZERO_FILL].fillna(0)
    data[MINUS_FILL] = data[MINUS_FILL].fillna(-1)
    return data.values
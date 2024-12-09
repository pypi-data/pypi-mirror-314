import numpy as np
import struct

numpy_pcd_type_mappings = [(np.dtype('float32'), ('F', 4)),
                           (np.dtype('float64'), ('F', 8)),
                           (np.dtype('uint8'), ('U', 1)),
                           (np.dtype('uint16'), ('U', 2)),
                           (np.dtype('uint32'), ('U', 4)),
                           (np.dtype('uint64'), ('U', 8)),
                           (np.dtype('int16'), ('I', 2)),
                           (np.dtype('int32'), ('I', 4)),
                           (np.dtype('int64'), ('I', 8))]

numpy_struct_type_mappings = [(np.dtype('float32'), 'f'),
                              (np.dtype('float64'), 'd'),
                              (np.dtype('uint8'), 'B'),
                              (np.dtype('uint16'), 'H'),
                              (np.dtype('uint32'), 'I'),
                              (np.dtype('uint64'), 'Q'),
                              (np.dtype('int16'), 'h'),
                              (np.dtype('int32'), 'i'),
                              (np.dtype('int64'), 'q')]

np_numpy_type_mappings = [('f32', np.dtype('float32')),
                          ('f64', np.dtype('float64')),
                          ('u8', np.dtype('uint8')),
                          ('u16', np.dtype('uint16')),
                          ('u32', np.dtype('uint32')),
                          ('u64', np.dtype('uint64')),
                          ('i16', np.dtype('int16')),
                          ('i32', np.dtype('int32')),
                          ('i64', np.dtype('int64'))]


def numpy_type_to_pcd_type(key):
    return dict(numpy_pcd_type_mappings)[key]


def pcd_type_to_numpy_type(key):
    return dict((q, p) for (p, q) in numpy_pcd_type_mappings)[key]


def numpy_type_to_struct_type(key):
    return dict(numpy_struct_type_mappings)[key]


def struct_type_to_numpy_type(key):
    return dict((q, p) for (p, q) in numpy_struct_type_mappings)[key]


def np_type_to_numpy_type(key):
    return dict(np_numpy_type_mappings)[key]


def numpy_type_to_np_type(key):
    return dict((q, p) for (p, q) in np_numpy_type_mappings)[key]

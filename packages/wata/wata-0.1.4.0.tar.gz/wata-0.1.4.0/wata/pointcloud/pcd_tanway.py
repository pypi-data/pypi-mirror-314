from wata.pointcloud.utils import utils
from numpy import ndarray
import numpy as np
from pathlib import Path
from typing import Union




class PointCloudTanway:

    @staticmethod
    def saveTanwayRoadPCDBinaryCompressed(points: ndarray, save_path):
        '''
        **功能描述**: 保存 BinaryCompressed pcd格式的点云,仅支持tanway 路端的数据
        
        Args:
            points: numpy格式的点云  
            save_path: pcd格式的点云文件保存的路径

        Returns:  
            无  
        '''
        fields = ['x', 'y', 'z', 'intensity', 'channel', 'angle', 'echo', 'mirror', 'block', 't_sec', 't_usec', 'lidar_id']
        npdtype = ['f32', 'f32', 'f32', 'f32', 'i32','f32', 'i32', 'i32', 'i32', 'u32', 'u32', 'i32']

        utils.save_pcd(points, save_path=save_path, fields=fields, npdtype=npdtype, type='binary_compressed')


    @staticmethod
    def get_anno_from_tanwayjson(json_data):
        boxes = []
        class_list = []
        for agent in json_data:
            boxes.append(
                [agent["position3d"]["x"], agent["position3d"]["y"], agent["position3d"]["z"], agent["size3d"]["x"],
                 agent["size3d"]["y"], agent["size3d"]["z"], agent["heading"]])
            class_list.append(agent["type"])
        return np.array(boxes), class_list
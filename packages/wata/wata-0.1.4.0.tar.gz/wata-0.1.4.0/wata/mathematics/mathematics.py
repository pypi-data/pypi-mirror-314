from wata.mathematics.utils import utils
from wata.mathematics.utils import trans_coordinate
import numpy as np

class Maths:

    @staticmethod
    def point_in_polygon(point:list, polygon:list):
        '''
        **功能描述**:判断点是否在多边形内  
        
        Args:
            point: 平面中的点  
            polygon: 含多边形中的点的列表  

        Returns:
            返回 1 在多边形内,返回0不在多边形内  

        '''
        return utils.point_in_polygon(point, polygon)

    @staticmethod
    def xy2rt(x:float,y:float):
        '''
        **功能描述**: 平面直角坐标系转极坐标系  
        
        Args:
            x: 平面直角坐标系中的横坐标值  
            y: 平面直角坐标系中的纵坐标值  

        Returns:  
            极坐标系中的坐标 (r,theta)  
        '''
        return trans_coordinate.xy2rt(x,y)

    @staticmethod
    def rt2xy(r, theta):
        '''
        **功能描述**: 极坐标系转平面直角坐标系  
        
        Args:  
            r: 极坐标系中的原点距离  
            theta: 极坐标系中的极角  

        Returns:  
            平面直角坐标系(x,y)  

        '''
        return trans_coordinate.rt2xy(r, theta)

    @staticmethod
    def xyz2rtp(x, y, z):
        '''
        **功能描述**: 笛卡尔直角坐标系转球坐标系  
        
        Args:  
            x: 笛卡尔直角坐标系中的x值  
            y: 笛卡尔直角坐标系中的y值  
            z: 笛卡尔直角坐标系中的z值  

        Returns:
            球坐标系 r, theta, phi  
        '''
        return trans_coordinate.xyz2rtp(x, y, z)

    @staticmethod
    def rtp2xyz(r,theta,phi):
        '''
        **功能描述**: 球坐标系转笛卡尔坐标系  
        
        Args:  
            r: 原点距离  
            theta: 水平偏角  
            phi: 竖直偏角  

        Returns:  
            笛卡尔坐标系(x,y,z)  

        '''
        return trans_coordinate.rtp2xyz(r,theta,phi)
from wata.pointcloud.utils import utils
from wata.pointcloud.utils import move_pcd
from wata.pointcloud.utils import o3d_visualize_utils
from wata.pointcloud.pcd_vis import PointCloudVisualize
from wata.pointcloud.pcd_tanway import PointCloudTanway
from numpy import ndarray
from pathlib import Path
from typing import Union



class PointCloudProcess(PointCloudVisualize,PointCloudTanway):

    @staticmethod
    def cut_pcd(points: ndarray, pcd_range: list, axis: str):
        '''
        **功能描述**: 切割指定范围的点云  
        
        Args:  
            points: numpy格式的点云  
            pcd_range: [x1,y1,z1,x2,y2,z2]  
            axis: 可选 "xy","xz","yz","xz","xyz",默认为"xyz"  

        Returns:  
            返回范围内的点  
        '''
        return utils.cut_pcd(points, pcd_range, axis)

    @staticmethod
    def filter_points(points: ndarray, del_points: ndarray):
        '''
        **功能描述**: 过滤删除部分点,要求del_points是points的子集  
        
        Args:  
            points: numpy格式的点云  
            del_points: 要从points中删除的点,numpy格式的点云  

        Returns:  
            剩余的点,numpy格式  
        '''
        return utils.filter_points(points, del_points)

    @staticmethod
    def points_to_o3d_model(points: ndarray, point_colors: Union[None, list] = None):
        '''
        **功能描述**: 将numpy格式的点云转化为open3d模型  
        
        Args:
            points: numpy格式的点云  
            point_colors: 点云的颜色信息,可以为None,可以为长度为3的元素为int类型的RGB列表  

        Returns:  
            open3d模型  
        '''
        return o3d_visualize_utils.points_to_o3d_model(points=points, point_colors=point_colors)

    @staticmethod
    def save_o3d_camera_parameters(points: ndarray, save_file_path: Union[str, Path] = 'camera_parameters.json',
                                   window_size: list = [1200, 800]):
        '''
        **功能描述**:  保存手动调整的open3d的视角  
        
        Args:  
            points: numpy格式的点云  
            save_file_path: open3d 可视化视角文件保存的路径 json  
            window_size: 可视化窗口的大小 list  

        Returns:  
            无  
        '''
        return o3d_visualize_utils.save_o3d_camera_parameters(points, save_file_path, window_size)

    @staticmethod
    def get_points(path: str, num_features: Union[None, int] = None):
        '''
        **功能描述**: 读取点云文件获取点
        
        Args:
            path: 点云文件的路径支持 pcd npy bin 格式的点云  
            num_features: 当点云文件格式为pcd 或npy时,num_features为加载点的列数; 当点云文件格式为bin时,num_features为bin文件点云的列数  

        Returns:  
            返回numpy格式的点云矩阵  
        '''
        return utils.get_points(path, num_features)

    @staticmethod
    def pcd2bin(pcd_dir: Union[str, Path], bin_dir: Union[str, Path], num_features=4):
        '''
        **功能描述**: pcd格式点云转bin格式  
        
        Args:  
            pcd_dir: pcd格式点云数据的存放目录  
            bin_dir: bin格式点云的数据村帆帆目录  
            num_features: bin格式的点云列数  

        Returns:  
            无  
        '''
        utils.pcd2bin(pcd_dir, bin_dir, num_features)

    @staticmethod
    def xyzrpy2RTmatrix(xyz_rpy, seq="xyz", degrees=True):
        '''
        **功能描述**: xyzrpy2RTmatrix  
        
        Args:
            xyz_rpy: list [dx, dy, dz, roll, pitch, yaw]  
            seq: 绕轴旋转的顺序  
            degrees: roll, pitch, yaw 是弧度还是角度 默认为弧度(False)  

        Returns:  
            numpy格式的4x4旋转平移矩阵   
        '''
        return move_pcd.xyzrpy2RTmatrix(xyz_rpy, seq, degrees)

    @staticmethod
    def RTmatrix2xyzrpy(RTmatrix: ndarray,seq="xyz", degrees=True):
        '''
        **功能描述**: RTmatrix2xyzrpy  
        
        Args:  
            RTmatrix: numpy格式的4x4旋转平移矩阵
            seq: 绕轴旋转的顺序  
            degrees: 保存角度值还是弧度值,默认True

        Returns:  
            numpy格式1x6矩阵 分别为 dx, dy, dz, roll, pitch, yaw  
        '''
        return move_pcd.RTmatrix2xyzrpy(RTmatrix,seq, degrees)

    @staticmethod
    def move_pcd_with_RTmatrix(points: ndarray, RTmatrix: ndarray, inv=False):
        '''
        **功能描述**: 通过旋转平移矩阵移动点云  
        
        Args:
            points: numpy格式的点云  
            RTmatrix: numpy格式的4x4旋转平移矩阵  
            inv: 是否对 RTmatrix 取逆,默认为False  

        Returns:  
            旋转平移后的numpy格式的点云  
        '''
        return move_pcd.move_pcd_with_RTmatrix(points, RTmatrix, inv)

    @staticmethod
    def move_pcd_with_xyzrpy(points: ndarray, xyz_rpy, seq="xyz", degrees=False):
        '''
        **功能描述**: 用 dx, dy, dz, roll, pitch, yaw 旋转平移点云,注意按照xyz的顺序先旋转再平移
        
        Args:  
            points: numpy格式的点云,需要有x,y,z维度  
            xyz_rpy: 列表格式[dx, dy, dz, roll, pitch, yaw]  
            degrees: xyz_rpy 中的roll, pitch, yaw是否为角度值,默认为False  

        Returns:  
            返回旋转平移后的点云  
        '''
        return move_pcd.move_pcd_with_xyzrpy(points, xyz_rpy, seq, degrees=degrees)
    
    @staticmethod
    def rotate_pointcloud(points: ndarray,rpy, seq="xyz",degrees=True):
        '''
        **功能描述**: 用 roll, pitch, yaw 旋转点云,根据seq选择旋转顺序
        
        Args:  
            points: numpy格式的点云,需要有x,y,z维度  
            rpy: 列表格式[roll, pitch, yaw]  
            degrees: rpy 中的roll, pitch, yaw是否为角度值,默认为True  

        Returns:  
            返回旋转后的点云  
        '''
        return move_pcd.rotate_pointcloud(points,rpy,seq,degrees)
    
    @staticmethod
    def translate_pointcloud(points: ndarray,xyz):
        '''
        **功能描述**: 用 x y z 平移点云  

        Args:  
            points: numpy格式的点云,需要有x,y,z维度  
            xyz: 列表格式[dx, dy, dz]  

        Returns:  
            返回平移后的点云  
        '''
        return move_pcd.translate_pointcloud(points, xyz)

    @staticmethod
    def cartesian_to_spherical(points: ndarray, degrees=False):
        '''
        **功能描述**: 直角坐标系转极坐标系,单位是弧度
        
        Args:  
            points: 直角坐标系点云  
            degrees: 返回值是否为角度,默认False 弧度  

        Returns:
            (r, theta竖直极角, phi水平方位角)的numpy格式点云  
        '''
        return utils.cartesian_to_spherical(points=points, degrees=degrees)

    @staticmethod
    def get_v_channel_from_pcd(points: ndarray, vfov, channel_nums, offset=0.01):
        '''
        **功能描述**: 获取垂直方向的通道  
        
        Args:  
            points: numpy格式的点云,需要有x,y,z维度  
            vfov: 长度为2的列表,代表了垂直视场角的范围,水平方向为0度,低于水平方向为负  
            channel_nums: 垂直通道的线数  
            offset: 偏移量  

        Returns:  
            numpy格式的 nx1 的数组  
        '''
        return utils.get_v_channel_from_pcd(points, vfov, channel_nums, offset)

    @staticmethod
    def get_h_channel_from_pcd(points: ndarray, hfov, channel_nums, offset=0.001):
        '''
        **功能描述**: 获取点云水平方向的通道  
        
        Args:
            points: numpy格式的点云,需要有x,y,z维度  
            hfov: 长度为2的列表,代表了水平视场角的范围,前向120度的视场角可用[30,150]表示  
            channel_nums: 水平通道的线数  
            offset: 偏移量  

        Returns:
            numpy格式的 nx1 的数组  
        '''
        return utils.get_h_channel_from_pcd(points, hfov, channel_nums, offset)

    @staticmethod
    def points_in_boxes(points: ndarray, boxes, type="gpu"):
        '''
        **功能描述**: 此API需要安装pytorch,用于标记和查找点云中在指定框内的点  
        
        Args:
            points: numpy格式的点云,需要有x,y,z维度  
            boxes: nx7的numpy矩阵  
            type: 可选"gpu" "cpu"  

        Returns:
            返回每个点所在框的索引列表  
        '''
        return utils.points_in_boxes(points, boxes, type)

    @staticmethod
    def save_pcd(points: ndarray, save_path, fields=None, npdtype=None, type='binary_compressed'):
        '''
        **功能描述**: 保存pcd格式的点云  
        
        Args:
            points: numpy格式的点云  
            save_path: pcd格式的点云文件保存的路径  
            fields: 点云每一列的元信息,当为None时默认为["x","y","z","4","5",....]  
            npdtype: 点云每一列保存的数据类型,支持numpy格式和字符串格式。字符串格式可选 "f32","f64","i8","i16","i32","i64","u8","u16","u32","u64"  
            type: 有三种格式,分别为“binary”, “ascii”,“binary_compressed” ,默认为“binary_compressed”。binary格式保存为二进制文件,ascii保存为普通文件,“binary_compressed”保存为二进制压缩格式

        Returns:  
            无  
        '''
        return utils.save_pcd(points, save_path, fields, npdtype, type)

    @staticmethod
    def array_to_structured_array(array, fields, npdtype):
        '''
        **功能描述**: 将普通的numpy转换为结构化的numpy数据

        Args:
            array: numpy格式的矩阵
            fields: 矩阵每一列的元信息
            npdtype: 点云每一列保存的数据类型。字符串格式可选 "f32","f64","i8","i16","i32","i64","u8","u16","u32","u64"

        Returns:
            返回结构化数据
        '''
        return utils.array_to_structured_array(array, fields, npdtype)

    @staticmethod
    def extract_bev_points_by_mask(points, mask, range, other_index=-1):
        '''
        **功能描述**: 根据提供的mask提取对应部分的点云

        Args:
            points:numpy数据
            mask:numpy格式的mask
            range:mask作用的点云的范围,如[xmin,ymin,xmax,ymax]
        Returns:
            返回每个点的mask索引列表
        '''
        return utils.extract_bev_points_by_mask(points, mask, range, other_index)

    @staticmethod
    def structured_array_to_array(structured_array):
        '''
        **功能描述**: 将结构化的numpy转换为普通矩阵

        Args:
            structured_array：结构化numpy数据

        Returns:
            返回普通numpy矩阵
        '''
        return utils.structured_array_to_array(structured_array)

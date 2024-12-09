from wata.pointcloud.utils import utils
from wata.pointcloud.utils.o3d_visualize_utils import open3d_draw_scenes, show_pcd_from_points_by_open3d,show_o3d_model
from wata.pointcloud.utils.plot_visualize_utils import plot_draw_scenes, show_pcd_from_points_by_matplotlib
from wata.pointcloud.utils.qtopengl_visualize_utils import show_pcd_from_points_by_qtopengl
from numpy import ndarray
from pathlib import Path
from typing import Union




class PointCloudVisualize:

    @staticmethod
    def show_pcd(path: Union[str, Path], point_size: float = 1, background_color: list = None, pcd_range: list = None,
                 bin_num_features: int = None,
                 create_coordinate: bool = True, create_plane: bool = False, type: str = 'open3d'):
        '''
        **功能描述**: 直接可视化点云文件,目前支持bin pcd npy 格式的点云

        Args:
            path: 点云的路径
            point_size: 点的大小
            background_color: 背景颜色
            pcd_range: 可视化点云的范围
            bin_num_features: 如果是bin格式的文件,应给出bin格式点云的列数
            create_coordinate: 是否可视化坐标系
            create_plane: 是否可视化出一个平面
            type: 用什么工具可视化, 默认open3d 可选 matplotlib open3d qtopengl mayavi(未开发) vispy(未开发)

        Returns:
            直接弹出可视化界面
        '''
        utils.show_pcd(path, point_size, background_color, pcd_range, bin_num_features,
                       create_coordinate, create_plane, type)

    @staticmethod
    def show_pcd_from_points(points: Union[ndarray, list], point_size: float = 1, background_color: list = None,
                             colors: Union[list, int] = None, create_coordinate=True,
                             create_plane=False, type='open3d'):
        '''
        **功能描述**: 展示点云

        Args:
            points: numpy格式的点云;当points为list时代表将list中的numpy格式的点云全部可视化
            point_size: 可视化点的大小,默认为1
            background_color: 背景颜色
            colors: 点云的颜色,当colors为int类型时,为用点云的第几列显色;当colors为list类型时,colors代表[R,G,B]
            create_coordinate: 是否可视化坐标系 , 可以设置数字调整坐标轴的尺寸,默认大小为1
            create_plane: 是否可视化出一个平面 ,默认每个网格宽度为10m, 可以设置数调整每个网格的尺寸
            type: 用什么工具可视化, 默认open3d 可选 matplotlib open3d qtopengl mayavi(未开发) vispy(未开发)

        Returns:
            无
        '''
        utils.show_pcd_from_points(points, point_size, background_color, colors, create_coordinate, create_plane, type)

    @staticmethod
    def show_pcd_from_points_by_open3d(points: Union[ndarray, list], point_size: float = 1, background_color: list = [0,0,0],
                             colors: Union[list, int] = None, create_coordinate=True,create_plane=False,cam_param=None, window_size=[1200,800]):
        show_pcd_from_points_by_open3d(points, point_size, background_color, colors, create_coordinate,
                                   create_plane, cam_param, window_size)

    @staticmethod
    def show_pcd_from_points_by_matplotlib(points: Union[ndarray, list], point_size: float = 1, background_color: list = None,
                             colors: Union[list, int] = None, create_coordinate=True,savepath=None, plot_range=None):
        show_pcd_from_points_by_matplotlib(points, point_size, background_color, colors,
                                       create_coordinate, savepath, plot_range)
    @staticmethod
    def show_pcd_from_points_by_qtopengl(points, point_size=1.5, background_color=[0,0,0], create_coordinate=True, create_plane=True):
        show_pcd_from_points_by_qtopengl(points, point_size, background_color, create_coordinate, create_plane)

    @staticmethod
    def add_boxes(points: Union[ndarray, list], gt_boxes: Union[ndarray, None] = None,
                  gt_labels: Union[None, list] = None, pred_boxes: Union[ndarray, None] = None,
                  pred_labels: Union[None, list] = None, pred_scores: Union[None, list] = None,
                  point_size: int = 1,
                  background_color: list = None, create_plane: bool = False, point_colors: Union[None, list] = None,
                  create_coordinate=True, type='open3d',
                  savepath=None, plot_range=None):
        '''
        **功能描述**: 绘制点云、标注框、预测框

        Args:
            points: numpy格式的点云;当points为list时代表将list中的numpy格式的点云全部可视化
            gt_boxes: GT框
            gt_labels: GT框标签
            pred_boxes: 预测框
            pred_labels: 预测框标签
            pred_scores: 预测框的分数
            point_size: 可视化点的大小,默认为1
            background_color: 背景颜色
            create_plane: 是否创建一个可视化地面
            point_colors: 对应points为列表时的颜色,当points为numpy格式时不起作用
            create_coordinate: 是否在原点创建坐标系
            type: 用什么工具可视化, 默认open3d 可选 matplotlib open3d qtopengl mayavi(未开发) vispy(未开发)
            savepath: 当type为matplotlib时,保存图像的地址
            plot_range: 当type为matplotlib时,可视化的范围

        Returns:
            可视化界面
        '''
        utils.add_boxes(points, gt_boxes=gt_boxes, gt_labels=gt_labels, pred_boxes=pred_boxes, pred_labels=pred_labels,
                        pred_scores=pred_scores, point_size=point_size,
                        background_color=background_color, create_plane=create_plane, point_colors=point_colors,
                        create_coordinate=create_coordinate, type=type, savepath=savepath, plot_range=plot_range)

    @staticmethod
    def add_boxes_by_open3d(points, colors=None, gt_boxes=None, gt_labels=None, pred_boxes=None, pred_labels=None,
                       pred_scores=None,point_size=1, background_color=None, create_plane=True,
                       create_coordinate=True, cam_param=None, window_size=[1200, 800]):
        open3d_draw_scenes(points, colors, gt_boxes, gt_labels, pred_boxes, pred_labels,
                       pred_scores,point_size, background_color, create_plane,
                       create_coordinate, cam_param, window_size)

    @staticmethod
    def add_boxes_by_matplotlib(points, gt_boxes=None, gt_labels=None, pred_boxes=None, pred_labels=None,
                                pred_scores=None, point_size=1,
                                background_color=None, colors=None, create_coordinate=True, savepath=None, plot_range=None):
        plot_draw_scenes(points=points, gt_boxes=gt_boxes, gt_labels=gt_labels,
                         pred_boxes=pred_boxes, pred_labels=pred_labels, pred_scores=pred_scores,
                         point_size=point_size, background_color=background_color,
                         point_colors=colors, create_coordinate=create_coordinate, savepath=savepath, plot_range=plot_range)
    @staticmethod
    def show_o3d_model(o3d_model_list, point_size, background_color=[0,0,0], cam_param=None, window_size=[1200, 800]):
        show_o3d_model(o3d_model_list, point_size, background_color, cam_param, window_size)
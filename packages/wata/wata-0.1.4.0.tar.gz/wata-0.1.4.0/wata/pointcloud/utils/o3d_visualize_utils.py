import matplotlib
import numpy as np
try:
    import open3d
except:
    OPEN3D = None
import os
from matplotlib import pyplot as plt

gt_box_colormap = [
    [0, 0.5, 0],
    [0, 0.5, 0.5],
    [0.5, 0.5, 0],
    [0.5, 0, 0.5],
    [0.5, 0, 0],
    [0, 0, 0.5],
    [0.5, 0.5, 0.5],
]
per_box_colormap = [
    [0, 1, 0],
    [0, 1, 1],
    [1, 1, 0],
    [1, 0, 1],
    [1, 0, 0],
    [0, 0, 1],
    [1, 1, 1],
]


def create_mesh_plane(grid_width=10.0, plane_width=200.0, z_position=-1.7, color=[0.2, 0.2, 0.2]):
    lines = []
    line_points = []
    grid_nums = plane_width / grid_width / 2
    for j in range(int(-1 * grid_nums), int(grid_nums + 1)):
        line_points.extend([[plane_width / 2, -j * grid_width, z_position],
                            [-1 * plane_width / 2, -j * grid_width, z_position]])
        # print("-----------------")
        # for j in range(int(-1 * grid_nums), int(grid_nums + 1)):
        line_points.extend([[j * grid_width, plane_width / 2, z_position],
                            [j * grid_width, -1 * plane_width / 2, z_position]])
    for i in range(int(len(line_points) / 2)):
        lines.append([2 * i, 2 * i + 1])
    line_set = open3d.geometry.LineSet()
    line_set.points = open3d.utility.Vector3dVector(line_points)
    line_set.lines = open3d.utility.Vector2iVector(lines)
    line_set.colors = open3d.utility.Vector3dVector([color for i in range(len(lines))])  # 设置颜色为红色
    # o3d.visualization.draw_geometries([line_set])
    return line_set


def get_coor_colors(obj_labels):
    """
    Args:
        obj_labels: 1 is ground, labels > 1 indicates different instance cluster

    Returns:
        rgb: [N, 3]. color for each point.
    """
    colors = matplotlib.colors.XKCD_COLORS.values()
    max_color_num = obj_labels.max()

    color_list = list(colors)[: max_color_num + 1]
    colors_rgba = [matplotlib.colors.to_rgba_array(color) for color in color_list]
    label_rgba = np.array(colors_rgba)[obj_labels]
    label_rgba = label_rgba.squeeze()[:, :3]

    return label_rgba


def points_to_o3d_model(points, point_colors=None):
    pts = open3d.geometry.PointCloud()
    pts.points = open3d.utility.Vector3dVector(points[:, :3])
    if point_colors is not None:
        if isinstance(point_colors, list) and isinstance(point_colors[0], int):
            point_colors = np.tile(point_colors, (len(points), 1))
            pts.colors = open3d.utility.Vector3dVector(point_colors)
        if isinstance(point_colors, int):
            colors = points[:, point_colors]
            colors_normalized = np.minimum(1, colors / 255)
            colors_rgb = np.stack((colors_normalized, np.zeros_like(colors_normalized), 1 - colors_normalized), axis=-1)
            pts.colors = open3d.utility.Vector3dVector(colors_rgb)
    return pts




def open3d_draw_scenes(points, colors=None, gt_boxes=None, gt_labels=None, pred_boxes=None, pred_labels=None,
                       pred_scores=None,
                       point_size=1, background_color=None, create_plane=True,
                       create_coordinate=True, cam_param=None, window_size=[1200, 800]):
    o3d_model_list = []
    if isinstance(points, list):
        if isinstance(colors, int):
            points = np.vstack(points)
            points_pcd = points_to_o3d_model(points,colors)
            o3d_model_list.append(points_pcd)
        elif isinstance(colors, list):
            for i, single_points in enumerate(points):
                single_points_pcd = points_to_o3d_model(single_points)
                assert len(points) == len(colors), "The length of points color should be the same"
                points_colors = np.tile(colors[i], (len(single_points), 1))
                single_points_pcd.colors = open3d.utility.Vector3dVector(points_colors)
                o3d_model_list.append(single_points_pcd)
        elif colors is None:
            for i, single_points in enumerate(points):
                single_points_pcd = points_to_o3d_model(single_points)
                o3d_model_list.append(single_points_pcd)
    else:
        pts = points_to_o3d_model(points,colors)
        o3d_model_list.append(pts)

    if create_plane >0:
        plane = create_mesh_plane()
        o3d_model_list.append(plane)

    if create_coordinate >0:
        coordinate = open3d.geometry.TriangleMesh.create_coordinate_frame(size=create_coordinate, origin=[0, 0, 0])
        o3d_model_list.append(coordinate)

    if gt_boxes is not None:
        assert gt_boxes.shape[1] == 7,"The dim of gt_boxes should be (Nx7)"
        gt_boxes_lineset_list = draw_box(gt_boxes, (0.5, 0.5, 0.5), gt_labels, gt_box_colormap)
        o3d_model_list.extend(gt_boxes_lineset_list)

    if pred_boxes is not None:
        pred_boxes_lineset_list = draw_box(pred_boxes, (0, 1, 0), pred_labels, per_box_colormap, pred_scores)
        o3d_model_list.extend(pred_boxes_lineset_list)

    show_o3d_model(o3d_model_list, point_size, background_color, cam_param=cam_param, window_size=window_size)


def translate_boxes_to_open3d_instance(gt_boxes):
    """
       4-------- 6
     /|         /|
    5 -------- 3 .
    | |        | |
    . 7 -------- 1
    |/         |/
    2 -------- 0
    """
    center = gt_boxes[0:3]
    lwh = gt_boxes[3:6]
    axis_angles = np.array([0, 0, gt_boxes[6] + 1e-10])
    rot = open3d.geometry.get_rotation_matrix_from_axis_angle(axis_angles)
    box3d = open3d.geometry.OrientedBoundingBox(center, rot, lwh)

    line_set = open3d.geometry.LineSet.create_from_oriented_bounding_box(box3d)

    # import ipdb; ipdb.set_trace(context=20)
    lines = np.asarray(line_set.lines)
    lines = np.concatenate([lines, np.array([[1, 4], [7, 6]])], axis=0)

    line_set.lines = open3d.utility.Vector2iVector(lines)

    return line_set, box3d


def draw_box(gt_boxes, color=(1, 0, 0), labels=None, box_colormap=[[1, 0, 1], [1, 0, 0]], score=None):
    box_model_list = []
    for i in range(gt_boxes.shape[0]):
        line_set, box3d = translate_boxes_to_open3d_instance(gt_boxes[i])
        if labels is None:
            line_set.paint_uniform_color(color)
            box_model_list.append(line_set)
        else:
            line_set.paint_uniform_color(box_colormap[labels[i]])
            box_model_list.append(line_set)

        # if score is not None:
        #     corners = box3d.get_box_points()
        #     vis.add_3d_label(corners[5], '%.2f' % score[i])
    return box_model_list


def show_pcd_from_points_by_open3d(points, point_size=1, background_color=None, colors=None, create_coordinate=True,
                                   create_plane=True, cam_param=None, window_size=[1200, 800]):
    o3d_model_list = []
    if isinstance(colors, int):
        if isinstance(points, list):
            points = np.vstack(points)
        points_pcd = points_to_o3d_model(points,colors)
        o3d_model_list.append(points_pcd)
    else:
        if isinstance(points, list):
            for i, single_points in enumerate(points):
                single_points = single_points[:, :3]
                single_points_pcd = open3d.geometry.PointCloud()
                single_points_pcd.points = open3d.utility.Vector3dVector(single_points)

                if colors is not None:
                    assert isinstance(colors, list), "color should be list"
                    assert len(points) == len(colors), "The length of points color should be the same"
                    points_colors = np.tile(colors[i], (len(single_points), 1))
                    single_points_pcd.colors = open3d.utility.Vector3dVector(points_colors)
                o3d_model_list.append(single_points_pcd)
        else:
            points = points[:, :3]
            pcd = open3d.geometry.PointCloud()
            pcd.points = open3d.utility.Vector3dVector(points)
            if colors is not None:
                points_colors = np.tile(colors, (len(points), 1))
                pcd.colors = open3d.utility.Vector3dVector(points_colors)
            o3d_model_list.append(pcd)

    if create_coordinate > 0:
        print(create_coordinate)
        coordinate = open3d.geometry.TriangleMesh.create_coordinate_frame(size=create_coordinate, origin=[0, 0, 0])
        o3d_model_list.append(coordinate)

    if create_plane:
        if create_plane == True:
            create_plane = 10
        plane = create_mesh_plane(grid_width=create_plane)
        o3d_model_list.append(plane)

    show_o3d_model(o3d_model_list, point_size=point_size, background_color=background_color, cam_param=cam_param,
                   window_size=window_size)


def load_param(vis, param_path):
    """
    读取自定义点云显示视角
    """
    param = open3d.io.read_pinhole_camera_parameters(param_path)
    ctr = vis.get_view_control()
    ctr.convert_from_pinhole_camera_parameters(param)


def show_o3d_model(o3d_model_list, point_size, background_color, cam_param=None, window_size=[1200, 800]):
    vis = open3d.visualization.Visualizer()
    vis.create_window(window_name='show_pcd_by_open3d', width=window_size[0], height=window_size[1])

    opt = vis.get_render_option()
    opt.point_size = point_size

    background_color = [0, 0, 0] if background_color is None else background_color
    opt.background_color = np.asarray(background_color)

    for model in o3d_model_list:
        vis.add_geometry(model)
    if cam_param is not None:
        load_param(vis, cam_param)
    vis.run()
    vis.clear_geometries()
    vis.destroy_window()


def save_o3d_camera_parameters(points, save_file_path='camera_parameters.json', window_size=[1200, 800]):
    vis = open3d.visualization.Visualizer()
    vis.create_window(window_name='show_pcd_by_open3d', width=window_size[0], height=window_size[1])
    opt = vis.get_render_option()
    opt.point_size = 1
    opt.background_color = np.asarray([0, 0, 0])

    points = points[:, :3]
    pcd = open3d.geometry.PointCloud()
    pcd.points = open3d.utility.Vector3dVector(points)
    vis.add_geometry(pcd)
    coordinate = open3d.geometry.TriangleMesh.create_coordinate_frame(size=3)
    vis.add_geometry(coordinate)
    plane = create_mesh_plane()
    vis.add_geometry(plane)
    # print(os.path.splitext(save_file_path))
    assert os.path.splitext(save_file_path)[-1] == '.json'
    param = vis.get_view_control().convert_to_pinhole_camera_parameters()
    open3d.io.write_pinhole_camera_parameters(save_file_path, param)

    vis.run()
    vis.clear_geometries()
    vis.destroy_window()

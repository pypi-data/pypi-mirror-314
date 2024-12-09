from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
from pyquaternion import Quaternion
import matplotlib

_label_colors = ['k', 'b', 'g', 'c', 'm', 'y', 'r']


def draw_single_bbox(center, size, yaw, color, linewidth):
    """
        convert box size to corners polygon
                   X
                   |
                ___|___
               |\  |  /|
               | \ | / |
        Y______|__\|/  |
               |       |
               |       |
               |_______|
    """
    # start from top-left by clockwise
    dx, dy, dz = size

    tl_p = [dx / 2.0, dy / 2.0, dz / 2.0]
    tr_p = [dx / 2.0, -dy / 2.0, dz / 2.0]
    br_p = [-dx / 2.0, -dy / 2.0, dz / 2.0]
    bl_p = [-dx / 2.0, dy / 2.0, dz / 2.0]

    # TIPS:
    rotate_q = Quaternion(axis=[0, 0, 1], radians=yaw)

    rotated_p = []
    for point3d in list([tl_p, tr_p, br_p, bl_p]):
        rotated_point3d = rotate_q.rotate(point3d)
        rotated_p.append((rotated_point3d + center)[:2])

    # print('rotated p shape', rotated_p[0].shape)
    return Polygon(
        (rotated_p[0], rotated_p[1], rotated_p[2],
         rotated_p[3], rotated_p[0], center[:2], rotated_p[1]),
        edgecolor=color,
        facecolor="none",
        linewidth=linewidth,
    )


def darw_bboxes(ax, scene_bbox, labels=None, scores=None, gt=False):
    color = 'r' if gt else 'g'
    for i in range(scene_bbox.shape[0]):
        box = scene_bbox[i]
        linewidth = 1.0
        if labels is not None:
            label = labels[i]
            linewidth = 1.5
            if not gt:
                if label < 0 or label > len(_label_colors) - 1:
                    color = "g"
                else:
                    color = _label_colors[label]

            ax.text(box[0], box[1] + 1, str(label), fontsize=20, color=color, ha='center', va='center')

        if scores is not None:
            score = scores[i]
            ax.text(box[0], box[1], str(score), fontsize=30, color='black', ha='center', va='center')

        poly = draw_single_bbox(box[:3], box[3:6], box[6], color, linewidth)
        ax.add_patch(poly)


def onscroll(event, ax):
    x_center = event.xdata
    y_center = event.ydata

    if event.button == 'up':
        ax.set_xlim(x_center - (x_center - ax.get_xlim()[0]) * 1.1, x_center + (ax.get_xlim()[1] - x_center) * 1.1)
        ax.set_ylim(y_center - (y_center - ax.get_ylim()[0]) * 1.1, y_center + (ax.get_ylim()[1] - y_center) * 1.1)
    elif event.button == 'down':
        ax.set_xlim(x_center - (x_center - ax.get_xlim()[0]) * 0.9, x_center + (ax.get_xlim()[1] - x_center) * 0.9)
        ax.set_ylim(y_center - (y_center - ax.get_ylim()[0]) * 0.9, y_center + (ax.get_ylim()[1] - y_center) * 0.9)

    plt.draw()


def ondrag(event, ax, fig):
    if event.button == 3 and event.xdata is not None and event.ydata is not None:
        x_start, y_start = event.xdata, event.ydata
        xlims = ax.get_xlim()
        ylims = ax.get_ylim()

        def onmove(event):
            nonlocal x_start, y_start
            if event.inaxes == ax:
                dx = event.xdata - x_start
                dy = event.ydata - y_start
                ax.set_xlim(xlims[0] - dx, xlims[1] - dx)
                ax.set_ylim(ylims[0] - dy, ylims[1] - dy)
                plt.draw()

        def onrelease(event):
            fig.canvas.mpl_disconnect(ondrag.id)
            fig.canvas.mpl_disconnect(onrelease.id)

        ondrag.id = fig.canvas.mpl_connect('motion_notify_event', onmove)
        onrelease.id = fig.canvas.mpl_connect('button_release_event', onrelease)


def show_pcd_from_points_by_matplotlib(points, point_size=0.6, background_color=None, colors=None,
                                       create_coordinate=True, savepath=None, plot_range=None):
    figsize = (18, 15) if savepath is None else (40, 30)
    fig, ax = plt.subplots(1, 1, figsize=figsize)

    ax.plot(0, 0, "x", color="black")
    background_color = [1, 1, 1] if background_color is None else background_color
    ax.set_facecolor(background_color)

    if create_coordinate > 0:
        if create_coordinate == True:
            create_coordinate = 5
        ax.arrow(0, 0, create_coordinate, 0, head_width=1, head_length=1.2, fc='r', ec='r')
        ax.arrow(0, 0, 0, create_coordinate, head_width=1, head_length=1.2, fc='g', ec='g')

    if isinstance(points, list):
        all_points = np.concatenate(points, axis=0)
        points_list = []
        if colors is not None:
            if isinstance(colors, int): # color 按照点云的维度显色
                all_points = np.transpose(all_points, (1, 0)).astype(np.float32)
                colors = np.minimum(1, all_points[colors, :] / 50)
                ax.scatter(all_points[0, :], all_points[1, :], c=colors, s=point_size)
            elif isinstance(colors, list): # color 按照给定的颜色显色
                for i, single_points in enumerate(points):
                    single_points = np.transpose(single_points, (1, 0)).astype(np.float32)
                    points_list.append(single_points[:, :3])
                    ax.scatter(single_points[0, :], single_points[1, :], c=colors[i], s=point_size)
                all_points = np.transpose(all_points, (1, 0)).astype(np.float32)
        else:
            all_points = np.transpose(all_points, (1, 0)).astype(np.float32)
            dists = np.sqrt(np.sum(all_points[:2, :] ** 2, axis=0), dtype=np.float32)
            colors = np.minimum(1, dists / 50)
            ax.scatter(all_points[0, :], all_points[1, :], c=colors, s=point_size)

    else:
        all_points = np.transpose(points, (1, 0)).astype(np.float32)
        if colors is None:
            dists = np.sqrt(np.sum(all_points[:2, :] ** 2, axis=0), dtype=np.float32)
            colors = np.minimum(1, dists / 50)
            # Colors = plt.get_cmap('Greens')  # 参考:https://zhuanlan.zhihu.com/p/114420786
            # colors = Colors(dists / 50)
        else:
            if isinstance(colors, int):
                colors = np.minimum(1, all_points[colors, :] / 50)
                ax.scatter(all_points[0, :], all_points[1, :], c=colors, s=point_size)
            # elif isinstance(colors, list):
            #     ax.scatter(all_points[0, :], all_points[1, :], c=colors, s=point_size)
        ax.scatter(all_points[0, :], all_points[1, :], c=colors, s=point_size)

    # Limit visible range.
    if plot_range is None:
        x_min = np.min(all_points[0, :])
        x_max = np.max(all_points[0, :])
        y_min = np.min(all_points[1, :])
        y_max = np.max(all_points[1, :])
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
    else:
        ax.set_xlim(plot_range[0], plot_range[2])
        ax.set_ylim(plot_range[1], plot_range[3])

    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)
    ax.set_aspect('equal')

    plt.title(savepath)
    if savepath is not None:
        plt.savefig(savepath)
        plt.close()
    else:
        # matplotlib.use('TkAgg')
        fig.canvas.mpl_connect('button_press_event', lambda event: ondrag(event, ax, fig))
        fig.canvas.mpl_connect('scroll_event', lambda event: onscroll(event, ax))
        plt.show()


def plot_draw_scenes(points, gt_boxes=None, gt_labels=None, pred_boxes=None, pred_labels=None, pred_scores=None,
                     point_size=1, background_color=None, point_colors=None, create_coordinate=True, savepath=None,
                     plot_range=None):
    """
        plot the gt and dt in BEV
    """
    matplotlib.use("Agg")
    pc_points = np.transpose(points, (1, 0)).astype(np.float32)
    fig, ax = plt.subplots(1, 1, figsize=(40, 30))
    # plot ego vehicle.
    ax.plot(0, 0, "x", color="black")
    background_color = [1, 1, 1] if background_color is None else background_color
    ax.set_facecolor(background_color)

    # 在0，0位置处设置一个坐标系
    if create_coordinate:
        ax.arrow(0, 0, 5, 0, head_width=1, head_length=1.2, fc='r', ec='r')
        ax.arrow(0, 0, 0, 5, head_width=1, head_length=1.2, fc='g', ec='g')

    # Limit visible range.
    if plot_range is None:
        x_min = np.min(pc_points[0, :])
        x_max = np.max(pc_points[0, :])
        y_min = np.min(pc_points[1, :])
        y_max = np.max(pc_points[1, :])
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
    else:
        ax.set_xlim(plot_range[0], plot_range[2])
        ax.set_ylim(plot_range[1], plot_range[3])
    ax.tick_params(axis='x', labelsize=20)
    ax.tick_params(axis='y', labelsize=20)
    ax.set_aspect('equal')

    # change color with distance
    dist = np.sqrt(np.sum(pc_points[:2, :] ** 2, axis=0), dtype=np.float32)
    colors = np.minimum(1, dist / 50) if point_colors is None else plt.get_cmap(point_colors)(
        dist / 50)  # 参考:https://zhuanlan.zhihu.com/p/114420786

    ax.scatter(pc_points[0, :], pc_points[1, :], c=colors, s=point_size)

    # plot gt_bboxes
    if gt_boxes is not None:
        darw_bboxes(ax, gt_boxes, gt_labels, gt=True)

    if pred_boxes is not None:
        darw_bboxes(ax, pred_boxes, pred_labels, pred_scores, gt=False)

    plt.title(savepath)
    if savepath is not None:
        plt.savefig(savepath)
        plt.close()
    else:
        fig.canvas.mpl_connect('button_press_event', lambda event: ondrag(event, ax, fig))
        fig.canvas.mpl_connect('scroll_event', lambda event: onscroll(event, ax))
        plt.show()

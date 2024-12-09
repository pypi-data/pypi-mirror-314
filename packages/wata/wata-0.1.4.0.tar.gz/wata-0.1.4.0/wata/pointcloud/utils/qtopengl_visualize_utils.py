
try:
    from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel
    from PyQt5.QtOpenGL import QGLWidget
    from PyQt5.QtCore import Qt
    from PyQt5 import QtCore, QtGui
    from PyQt5.QtGui import QColor
    import pyqtgraph.opengl as gl
    from pyqtgraph.opengl import GLAxisItem
except:
    PYQT5 = None

import numpy as np
from scipy.spatial.distance import cdist
import matplotlib.pyplot as plt

def quit_application():
    QApplication.quit()


def show_pcd_from_points_by_qtopengl(points, point_size, background_color, create_coordinate=True, create_plane=True):
    points = points[:, 0:3]
    app = QApplication([])

    """创建主窗口部件"""
    window = QWidget()
    window.resize(1200, 800)

    """创建OpenGL视图窗口"""
    widget = gl.GLViewWidget()
    widget.setWindowTitle('Point Cloud Viewer')

    Colors = plt.get_cmap('cool')  # 参考:https://zhuanlan.zhihu.com/p/114420786
    colors = Colors(points[:, 0] / 40)

    """添加点云"""
    scatter = gl.GLScatterPlotItem(pos=points, color=colors, size=point_size)
    widget.addItem(scatter)

    """添加平面网格"""
    if create_plane:
        if create_plane == True:
            create_plane = 10
        plane = gl.GLGridItem(size=QtGui.QVector3D(200, 200, 0), color=QColor(40, 40, 40, 255), glOptions='translucent')
        plane.setSpacing(create_plane, create_plane, 1)
        plane_center = (0, 0, -3)
        plane.translate(*plane_center)
        widget.addItem(plane)

    '''添加坐标系'''
    if create_coordinate:
        if create_coordinate == True:
            create_coordinate = 3
        axis = gl.GLAxisItem(size=QtGui.QVector3D(create_coordinate, create_coordinate, create_coordinate))
        widget.addItem(axis)

    """调整视角"""
    widget.opts['distance'] = 80
    widget.setCameraPosition(distance=widget.opts['distance'], elevation=15, azimuth=-110)

    """设置背景颜色"""
    widget.setBackgroundColor(background_color[0], background_color[1], background_color[2], 1)

    layout = QVBoxLayout()
    layout.addWidget(widget)

    window.setLayout(layout)
    window.show()
    # 运行应用程序
    app.exec_()

# # 从文件中读取点云数据
# point_cloud = o3d.io.read_point_cloud("../example.pcd")
# points = np.asarray(point_cloud.points)
# Colors = plt.get_cmap('cool')  # 参考:https://zhuanlan.zhihu.com/p/114420786
# colors = Colors(points[:, 0] / 40)

# """创建PyQt应用程序对象"""
# app = QApplication([])

# """创建主窗口部件"""
# window = QWidget()
# window.resize(800, 600)

# """创建OpenGL视图窗口"""
# widget = gl.GLViewWidget()
# widget.setWindowTitle('Point Cloud Viewer')

# """添加网格项到视图窗口中"""
# grid = gl.GLGridItem()
# widget.addItem(grid)

# """调整视角"""
# widget.opts['distance'] = 40
# widget.setCameraPosition(distance=widget.opts['distance'], elevation=15, azimuth=45)

# """添加点云到视图窗口中"""
# point_size = 2  # 设置点的大小
# scatter = gl.GLScatterPlotItem(pos=points, color=colors, size=point_size)
# widget.addItem(scatter)

# """画线的方法"""
# box_center = np.array([0, 0, 0])  # 框的中心点
# box_size = np.array([1, 1, 1])  # 框的尺寸
# box_pos = box_center - box_size / 2
# box_lines = np.array([  # 就是把下面的点按照顺序连接起来
#     [box_pos[0], box_pos[1] + 0.5, box_pos[2] - 0.5], [box_pos[0], box_pos[1] - 0.5, box_pos[2] + 0.5],
#     [box_pos[0], box_pos[1] + 0.5, box_pos[2] + 0.5]  # lower edges
# ])
# box_color = (1, 0, 0, 1)  # 设置线的颜色
# box_width = 2  # 设置线的宽度
# box_lines_item = gl.GLLinePlotItem(pos=box_lines, color=box_color, width=box_width)
# widget.addItem(box_lines_item)

# """画3d线框的方法"""
# '''
# 感觉没啥用啊！
# 'additive'：将盒子以加法混合模式渲染，形成颜色累积效应。
# 'opaque'：将盒子设置为不透明。
# 'translucent'：将盒子设置为半透明。
# '''
# box = gl.GLBoxItem(size=QtGui.QVector3D(1, 2, 1), color=QColor(255, 255, 0, 255), glOptions='opaque')
# widget.addItem(box)
# # 设置立方体的中心点位置
# box_center = (1, 1, 0)
# box.translate(*box_center)
# """ 
# Rotate the object around the axis specified by (x,y,z).
# *angle* is in degrees.
# """
# box.rotate(90, 0, 0, 1)


# """添加平面网格"""
# plane = gl.GLGridItem(size=QtGui.QVector3D(10, 20, 1), color=QColor(255, 0, 0, 255), glOptions='translucent')
# plane_center = (1, 10, 1)
# plane.translate(*plane_center)
# widget.addItem(plane)


# ''' 创建mesh平面, 可以用它来画3d实心框'''
# vertexes = [[0, 0, 0], [0, 2, 2], [0, 0, 2], [0, 2, 0]]
# faces = [[0, 1, 2], [1, 0, 3]]
# meshface = gl.MeshData(vertexes=np.array(vertexes), faces=np.array(faces))
# meshface = gl.GLMeshItem(meshdata=meshface, smooth=False, shader='shaded', glOptions='translucent', drawEdges=True,
#                          color=QColor(255, 0, 255, 200))
# # meshface.translate(1, 0, 0)
# widget.addItem(meshface)

# text_label = gl.GLTextItem(text="3D 框", pos=(0, 0, 0), color=QColor(QtCore.Qt.blue),
#                            font=QtGui.QFont('Helvetica', 16))

# widget.addItem(text_label)


# '''创建退出按钮'''
# quit_button = QPushButton("退出")
# quit_button.clicked.connect(quit_application)

# # 创建垂直布局，并将OpenGL视图窗口和退出按钮添加到其中
# layout = QVBoxLayout()
# layout.addWidget(widget)
# layout.addWidget(quit_button)

# # 将布局设置给主窗口部件
# window.setLayout(layout)
# window.show()

# # 运行应用程序
# app.exec_()

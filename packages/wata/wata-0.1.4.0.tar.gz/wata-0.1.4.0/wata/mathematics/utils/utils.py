import math
import numpy as np

def point_in_polygon(point, polygon):
        # 在圆内就返回1，圆外返回0
        x, y = point
        n = len(polygon)
        count = 0
        for i in range(n):
            x1, y1 = polygon[i]
            x2, y2 = polygon[(i + 1) % n]
            # 判断点是否在多边形顶点处
            if (x == x1 and y == y1) or (x == x2 and y == y2):
                return 1
            if min(y1, y2) < y <= max(y1, y2):
                # 计算交点的横坐标
                x0 = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                # 如果交点位于射线之右，则计数器加1
                if x0 > x:
                    count += 1     
        return 1 if count % 2 == 1 else 0
import numpy as np
import math

def xy2rt(x,y):
    # 球坐标系
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan2(y, x)
    return r, theta


def rt2xy(r, theta):
    # 极坐标系转直角坐标系
    x = r * np.cos(theta)
    y = r * np.sin(theta)
    return x, y

def xyz2rtp(x, y, z):
    # 柱标系
    r = np.sqrt(x**2 + y**2 + z**2)
    phi = np.arccos(z / r)
    theta = np.arctan2(y, x)
    return r, theta, phi


def rtp2xyz(r,theta,phi):
    x = r * np.sin(phi) * np.cos(theta)
    y = r * np.sin(phi) * np.sin(theta)
    z = r * np.cos(phi)
    return x, y, z
import math
import numpy as np

def is_normalized(vector):
    return np.linalg.norm(vector) == 1

def _3d_distance(a, b):

    a = np.array(a)
    b = np.array(b)

    return np.linalg.norm(a - b)

def _compose(pose):
    rotation = pose[3:]
    position = pose[:3]
    x = rotation[0]
    y = rotation[1]
    z = rotation[2]

    cos = math.cos
    sin = math.sin

    c1 = cos(x/2)
    c2 = cos(y/2)
    c3 = cos(z/2)

    s1 = sin(x/2)
    s2 = sin(y/2)
    s3 = sin(z/2)

    qx = s1 * c2 * c3 + c1 * s2 * s3
    qy = c1 * s2 * c3 - s1 * c2 * s3
    qz = c1 * c2 * s3 + s1 * s2 * c3
    qw = c1 * c2 * c3 - s1 * s2 * s3

    qx2 = (qx * qx)
    qy2 = (qy * qy)
    qz2 = (qz * qz)
    qxqy = (qx * qy)
    qyqz = (qy * qz)
    qzqx = (qz * qx)
    qwqx = (qw * qx)
    qwqy = (qw * qy)
    qwqz = (qw * qz)

    d10 = (1 - 2 * (qy2 + qz2))
    d11 = 2 * (qxqy + qwqz)
    d12 = 2 * (qzqx - qwqy)
    d13 = 0
    d20 = 2 * (qxqy - qwqz)
    d21 = (1 - 2 * (qx2 + qz2))
    d22 = 2 * (qyqz + qwqx)
    d23 = 0
    d30 = 2 * (qzqx + qwqy)
    d31 = 2 * (qyqz - qwqx)
    d32 = (1 - 2 * (qx2 + qy2))
    d33 = 0
    d40 = position[0]
    d41 = position[1]
    d42 = position[2]
    d43 = 1

    d1 = [d10, d11, d12, d13]
    d2 = [d20, d21, d22, d23]
    d3 = [d30, d31, d32, d33]
    d4 = [d40, d41, d42, d43]

    matrix = np.array([d1, d2, d3, d4])

    return matrix

def _matmul(a, b):
    return np.matmul(a, b)

def _invert(a):
    return np.linalg.inv(a)

def rad_to_deg(radians):
    return math.degrees(radians)

def deg_to_rad(degrees):
    return math.radians(degrees)

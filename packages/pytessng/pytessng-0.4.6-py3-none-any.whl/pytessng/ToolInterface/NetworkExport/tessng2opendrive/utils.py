import numpy as np


# 计算向量2相对向量1的旋转角度（-pi~pi）
def clockwise_angle(v1, v2):
    x1, y1 = v1.x, v1.y
    x2, y2 = v2.x, v2.y
    dot = x1 * x2 + y1 * y2
    det = x1 * y2 - y1 * x2
    theta = np.arctan2(det, dot)
    return theta

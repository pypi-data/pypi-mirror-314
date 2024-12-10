import numpy as np
from scipy.optimize import curve_fit


# 定义三次参数曲线函数
def cubic_parametric(t, a0, a1, a2, a3, b0, b1, b2, b3):
    x = a0 + a1 * t + a2 * t**2 + a3 * t**3
    y = b0 + b1 * t + b2 * t**2 + b3 * t**3
    return np.array([x, y])

# 拟合函数，增加权重参数
def fit_function(t, a0, a1, a2, a3, b0, b1, b2, b3, weights):
    x, y = cubic_parametric(t, a0, a1, a2, a3, b0, b1, b2, b3)
    x_weighted = x * weights
    y_weighted = y * weights
    return np.concatenate((x_weighted, y_weighted))

# 计算拟合优度 R^2
def calculate_r_squared(x_data, y_data, x_fit, y_fit):
    ss_res = np.sum((x_data - x_fit)**2 + (y_data - y_fit)**2)
    ss_tot = np.sum((x_data - np.mean(x_data))**2 + (y_data - np.mean(y_data))**2)
    r_squared = 1 - (ss_res / ss_tot)
    return r_squared

def fit(points):
    x_data = np.array([p[0] for p in points])
    y_data = np.array([p[1] for p in points])
    
    # 将样本数据打包
    t_data = np.linspace(0, 1, len(x_data))
    
    # 初始猜测参数
    initial_guess = [0, 1, 0, 0, 0, 1, 0, 0]
    
    # 设置权重，增加首尾两点的权重
    weights = np.ones_like(t_data)
    weights[0] = 100  # 首点权重
    # weights[1] = 100  # 首点权重
    # # # weights[3] = 10
    # # # weights[-4] = 10
    # weights[-2] = 100  # 尾点权重
    weights[-1] = 100  # 尾点权重

    # 执行拟合
    popt, pcov = curve_fit(
        lambda t, a0, a1, a2, a3, b0, b1, b2, b3: fit_function(t, a0, a1, a2, a3, b0, b1, b2, b3, weights), 
        t_data, 
        np.concatenate((x_data * weights, y_data * weights)), 
        p0=initial_guess
        )
    
    # 拟合参数
    a0, a1, a2, a3, b0, b1, b2, b3 = popt
    
    # # 用拟合参数计算拟合曲线
    # t_fit = np.linspace(0, 1, 100)
    # x_fit, y_fit = cubic_parametric(t_fit, a0, a1, a2, a3, b0, b1, b2, b3)
    #
    # 计算 R^2
    x_fit_data, y_fit_data = cubic_parametric(t_data, a0, a1, a2, a3, b0, b1, b2, b3)
    r_squared = calculate_r_squared(x_data, y_data, x_fit_data, y_fit_data)
    #
    # # 绘图
    # plt.plot(x_data, y_data, 'ro', label='Data points')
    # plt.plot(x_fit, y_fit, 'b-', label='Fitted cubic curve')
    # plt.xlabel('x')
    # plt.ylabel('y')
    # # plt.title(f'Cubic Parametric Curve Fitting (R^2 = {r_squared:.3f})')
    # # plt.legend()
    # plt.show()
    return r_squared, a0, a1, a2, a3, b0, b1, b2, b3

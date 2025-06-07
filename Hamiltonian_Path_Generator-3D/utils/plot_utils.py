import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_path(path, dimensions=(5, 5, 5)):
    points = np.array(path)

    # 创建3D绘图
    fig = plt.figure(facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')

    # 绘制路径
    for i in range(1, len(points)):
        x1, y1, z1 = points[i - 1]
        x2, y2, z2 = points[i]
        ax.plot([x1, x2], [y1, y2], [z1, z2], linewidth=2, color='brown')

    # 绘制路径点
    ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=100, marker='o', color='pink')

    # 设置图形标题和标签
    ax.set_title("3D Path", color='white')
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.set_zlabel('Z', color='white')

    # 设置图形显示的角度
    ax.view_init(elev=90, azim=0)

    # 设置背景颜色为黑色
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')

    # 设置坐标轴颜色为白色
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.zaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    ax.tick_params(axis='z', colors='white')

    return fig
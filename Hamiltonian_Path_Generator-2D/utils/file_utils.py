import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

def save_favourite_image(path, size_x, size_y, favourite_name, min_length):
    current_dir = os.path.dirname(__file__)
    target_folder = os.path.abspath(os.path.join(current_dir, '..', 'screenshots', 'favour', str(min_length)))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    existing_files = os.listdir(target_folder)
    base_name = favourite_name
    counter = 1

    target_file = os.path.join(target_folder, f"{favourite_name}.png")
    while os.path.exists(target_file):
        favourite_name = f"{base_name}_{counter}"
        target_file = os.path.join(target_folder, f"{favourite_name}.png")
        counter += 1

    # 生成贝塞尔曲线图并保存
    points = np.array(path)
    fig2 = plt.figure(facecolor='white')
    ax2 = fig2.add_subplot(111, facecolor='white')
    x = points[:, 0]
    y = points[:, 1]
    t = np.linspace(0, 1, len(points))
    spl_x = make_interp_spline(t, x, k=3)
    spl_y = make_interp_spline(t, y, k=3)
    
    # 根据点阵的密集程度调整平滑度
    num_points = size_x * size_y * 10  # 点阵越密集，贝塞尔曲线越平滑
    t_new = np.linspace(0, 1, num_points)
    x_smooth = spl_x(t_new)
    y_smooth = spl_y(t_new)

    # 动态调整linewidth
    base_linewidth = 15
    base_size = 5 * 5
    current_size = size_x * size_y
    linewidth = base_linewidth * (base_size / current_size)

    ax2.plot(x_smooth, y_smooth, linewidth=linewidth, color='lightblue')

    # 设置坐标轴范围，为不存在的点预留空间
    ax2.set_xlim(0, size_x + 1)
    ax2.set_ylim(0, size_y + 1)
    ax2.set_aspect('equal')
    ax2.set_axis_off()
    fig2.savefig(target_file, bbox_inches='tight', pad_inches=0.1, dpi=300)
    plt.close(fig2)
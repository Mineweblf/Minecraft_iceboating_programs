import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline

def plot_path(path, dimensions=(5, 5)):
    points = np.array(path)
    fig, ax = plt.subplots(facecolor='black')

    for i in range(1, len(points)):
        x1, y1 = points[i - 1]
        x2, y2 = points[i]
        ax.plot([x1, x2], [y1, y2], linewidth=2, color='brown')

    ax.scatter(points[:, 0], points[:, 1], s=100, marker='o', color='pink')
    ax.set_title("2D Path", color='white')
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    return fig

def plot_bezier_path(path, dimensions=(5, 5)):
    points = np.array(path)
    fig, ax = plt.subplots(facecolor='black')

    x = points[:, 0]
    y = points[:, 1]
    t = np.linspace(0, 1, len(points))
    spl_x = make_interp_spline(t, x, k=3)
    spl_y = make_interp_spline(t, y, k=3)
    t_new = np.linspace(0, 1, 300)
    x_smooth = spl_x(t_new)
    y_smooth = spl_y(t_new)
    ax.plot(x_smooth, y_smooth, linewidth=2, color='blue')

    ax.scatter(points[:, 0], points[:, 1], s=100, marker='o', color='pink')
    ax.set_title("Bezier Path", color='white')
    ax.set_xlabel('X', color='white')
    ax.set_ylabel('Y', color='white')
    ax.set_facecolor('black')
    fig.patch.set_facecolor('black')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    return fig
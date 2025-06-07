import os
import csv
import numpy as np
import matplotlib.pyplot as plt

def save_plane_images(x_size, y_size, z_size, path, output_folder):
    current_dir = os.path.dirname(__file__)
    output_folder = os.path.join(current_dir, '..', output_folder)
    plane_folder = os.path.join(output_folder, 'xoy_plane')
    if not os.path.exists(plane_folder):
        os.makedirs(plane_folder)
    else:
        for file_name in os.listdir(plane_folder):
            file_path = os.path.join(plane_folder, file_name)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    offset = 0.15
    path_color = 'lightblue'
    path_linewidth = 2

    csv_file = os.path.join(current_dir, '..', 'data', 'path_data.csv')
    abs_csv_file = os.path.abspath(csv_file)
    path_data = []
    with open(abs_csv_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            path_data.append(row)

    for z in range(1, z_size + 1):
        fig, ax = plt.subplots()
        for x in range(1, x_size + 1):
            for y in range(1, y_size + 1):
                ax.scatter(x, y, s=100, color='gray')

        for data in path_data:
            x = int(data['x'])
            y = int(data['y'])
            z_coord = int(data['z'])
            if z_coord == z:
                ax.scatter(x, y, s=400, color='darkred')
                if data['up'] == 'True':
                    ax.scatter(x, y, s=225, color='black', marker='o')
                if data['down'] == 'True':
                    ax.scatter(x, y, s=324, color='yellow', marker='x')

                if data['right'] == 'True':
                    ax.plot([x + offset, (x + 1) - offset], [y, y], color=path_color, linewidth=path_linewidth)
                if data['left'] == 'True':
                    ax.plot([x - offset, (x - 1) + offset], [y, y], color=path_color, linewidth=path_linewidth)
                if data['forward'] == 'True':
                    ax.plot([x, x], [y + offset, (y + 1) - offset], color=path_color, linewidth=path_linewidth)
                if data['backward'] == 'True':
                    ax.plot([x, x], [y - offset, (y - 1) + offset], color=path_color, linewidth=path_linewidth)

        ax.set_facecolor('black')
        ax.grid(False)
        ax.set_xticks(range(1, x_size + 1))
        ax.set_yticks(range(1, y_size + 1))
        ax.set_aspect('equal', 'box')

        fig.savefig(os.path.join(plane_folder, f"xoy_plane_{z}.png"), facecolor='black')
        plt.close(fig)
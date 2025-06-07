import csv
import os

def save_path_to_csv(path, directions, output_folder):
    current_dir = os.path.dirname(__file__)
    output_folder = os.path.join(current_dir, '..', output_folder)
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    csv_file = os.path.join(output_folder, 'path_data.csv')
    abs_csv_file = os.path.abspath(csv_file)

    with open(abs_csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['x', 'y', 'z', 'up', 'down', 'left', 'right', 'forward', 'backward'])

        direction_map = {
            'up': (0, 0, 1),
            'down': (0, 0, -1),
            'left': (-1, 0, 0),
            'right': (1, 0, 0),
            'forward': (0, 1, 0),
            'backward': (0, -1, 0)
        }

        for i, point in enumerate(path):
            x, y, z = point
            up = down = left = right = forward = backward = False
            if i < len(directions):
                direction = directions[i]
                dx, dy, dz = direction_map[direction]
                if dx == 1:
                    right = True
                elif dx == -1:
                    left = True
                elif dy == 1:
                    forward = True
                elif dy == -1:
                    backward = True
                elif dz == 1:
                    up = True
                elif dz == -1:
                    down = True
            writer.writerow([x, y, z, up, down, left, right, forward, backward])
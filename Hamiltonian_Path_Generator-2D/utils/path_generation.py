import random
import numpy as np
from queue import PriorityQueue

def generate_path(size_x, size_y, num_points, start_point=None, random_start=False, consider_45_degrees=False):
    max_attempts = 100000

    def is_valid_move(point, path, size_x, size_y):
        x, y = point
        return 1 <= x <= size_x and 1 <= y <= size_y and point not in path

    def backtrack(path, directions, size_x, size_y, num_points, consider_45_degrees):
        if len(path) == num_points:
            return path, directions

        current_point = path[-1]
        possible_moves = [(current_point[0] + 1, current_point[1], 'right'),
                          (current_point[0] - 1, current_point[1], 'left'),
                          (current_point[0], current_point[1] + 1, 'forward'),
                          (current_point[0], current_point[1] - 1, 'backward')]
        
        if consider_45_degrees:
            possible_moves.extend([(current_point[0] + 1, current_point[1] + 1, 'right-forward'),
                                   (current_point[0] - 1, current_point[1] - 1, 'left-backward'),
                                   (current_point[0] + 1, current_point[1] - 1, 'right-backward'),
                                   (current_point[0] - 1, current_point[1] + 1, 'left-forward')])
        
        random.shuffle(possible_moves)

        for move in possible_moves:
            next_point, direction = move[:2], move[2]
            if is_valid_move(next_point, path, size_x, size_y):
                path.append(next_point)
                directions.append(direction)
                result = backtrack(path, directions, size_x, size_y, num_points, consider_45_degrees)
                if result:
                    return result
                path.pop()
                directions.pop()

        return None, None

    attempts = 0
    for _ in range(max_attempts):
        attempts += 1
        if random_start or start_point is None:
            start_point = (random.randint(1, size_x), random.randint(1, size_y))
        path = [start_point]
        directions = []

        result, directions = backtrack(path, directions, size_x, size_y, num_points, consider_45_degrees)

        if result:
            return result, directions, attempts, True

    return None, None, attempts, False
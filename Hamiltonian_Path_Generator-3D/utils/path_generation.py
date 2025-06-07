import random
import numpy as np
from queue import PriorityQueue
import os

def generate_path(size, num_points, start_point=None, random_start=False, mode="Open Path"):
    max_attempts = 10000
    open_path_attempts = 0
    closed_loop_attempts = 0

    def is_valid_move(point, path, size):
        x, y, z = point
        if not (1 <= x <= size and 1 <= y <= size and 1 <= z <= size):
            return False
        if point in path:
            return False
        return True

    def backtrack(path, directions, size, num_points, mode):
        if len(path) == num_points:
            if mode == "Closed Loop" and path[0] != path[-1]:
                return None, None
            return path, directions

        current_point = path[-1]
        possible_moves = [(current_point[0] + 1, current_point[1], current_point[2], 'right'),
                          (current_point[0] - 1, current_point[1], current_point[2], 'left'),
                          (current_point[0], current_point[1] + 1, current_point[2], 'forward'),
                          (current_point[0], current_point[1] - 1, current_point[2], 'backward'),
                          (current_point[0], current_point[1], current_point[2] + 1, 'up'),
                          (current_point[0], current_point[1], current_point[2] - 1, 'down')]
        random.shuffle(possible_moves)

        for move in possible_moves:
            next_point, direction = move[:3], move[3]
            if is_valid_move(next_point, path, size):
                path.append(next_point)
                directions.append(direction)
                result = backtrack(path, directions, size, num_points, mode)
                if result:
                    return result
                path.pop()
                directions.pop()

        return None, None

    def branch_and_bound(start_point, size, num_points):
        def heuristic(point, end_point):
            return abs(point[0] - end_point[0]) + abs(point[1] - end_point[1]) + abs(point[2] - end_point[2])

        end_point = start_point
        pq = PriorityQueue()
        pq.put((0, [start_point], []))

        while not pq.empty():
            _, path, directions = pq.get()
            if len(path) == num_points:
                if path[-1] == end_point:
                    return path, directions
                continue

            current_point = path[-1]
            possible_moves = [(current_point[0] + 1, current_point[1], current_point[2], 'right'),
                              (current_point[0] - 1, current_point[1], current_point[2], 'left'),
                              (current_point[0], current_point[1] + 1, current_point[2], 'forward'),
                              (current_point[0], current_point[1] - 1, current_point[2], 'backward'),
                              (current_point[0], current_point[1], current_point[2] + 1, 'up'),
                              (current_point[0], current_point[1], current_point[2] - 1, 'down')]
            random.shuffle(possible_moves)

            for move in possible_moves:
                next_point, direction = move[:3], move[3]
                if is_valid_move(next_point, path, size):
                    new_path = path + [next_point]
                    new_directions = directions + [direction]
                    cost = len(new_path) + heuristic(next_point, end_point)
                    pq.put((cost, new_path, new_directions))

        return None, None

    while open_path_attempts < max_attempts or closed_loop_attempts < max_attempts:
        if mode == "Closed Loop":
            closed_loop_attempts += 1
            print(f"Closed Loop 尝试次数: {closed_loop_attempts}")
        else:
            open_path_attempts += 1
            print(f"Open Path 尝试次数: {open_path_attempts}")

        if random_start or start_point is None:
            start_point = (random.randint(1, size),
                           random.randint(1, size),
                           random.randint(1, size))
        path = [start_point]
        directions = []

        if mode == "Closed Loop":
            result, directions = branch_and_bound(start_point, size, num_points)
        else:
            result, directions = backtrack(path, directions, size, num_points, mode)

        if result:
            return result, directions

    return None, None
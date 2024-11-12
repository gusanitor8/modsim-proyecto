import math 
import random
from constants import WALL, PATH, DIRECTIONS


def fitness(path, maze):
    exit = maze["exit"]
    solutions = maze["solutions"]
    
    # We calculate the distance
    last_coordinate = path[-1]
    dist = distance(last_coordinate[0], last_coordinate[1], exit[0], exit[1])

    if dist == 0:
        if last_coordinate in solutions:
            maze["solutions"][last_coordinate] += 1
        else:
            maze["solutions"][last_coordinate] = 1

        return 0 

    # We penalize recurring solutions
    if last_coordinate in solutions:
        maze["solutions"][last_coordinate] += 1
        return dist * maze["solutions"][last_coordinate]
    
    else:
        maze["solutions"][last_coordinate] = 1
        return dist
    
def fitness_explore(path, maze):
    exit = maze["exit"]
    solutions = maze["solutions"]
    
    # We calculate the distance
    last_coordinate = path[-1]
    dist = distance(last_coordinate[0], last_coordinate[1], exit[0], exit[1])

    if dist == 0:
        if last_coordinate in solutions:
            maze["solutions"][last_coordinate] += 1
        else:
            maze["solutions"][last_coordinate] = 1

        return 0 - 99999

    # We penalize recurring solutions
    if last_coordinate in solutions:
        maze["solutions"][last_coordinate] += 1
        return dist * maze["solutions"][last_coordinate]
    
    else:
        maze["solutions"][last_coordinate] = 1
        return dist - 30
    
def fitness_log(path, maze):
    exit = maze["exit"]
    solutions = maze["solutions"]

    # Calculamos la distancia
    last_coordinate = path[-1]
    dist = distance(last_coordinate[0], last_coordinate[1], exit[0], exit[1])

    if dist == 0:
        if last_coordinate in solutions:
            maze["solutions"][last_coordinate] += 1
        else:
            maze["solutions"][last_coordinate] = 1

        return 0 

    # Penalización logarítmica para soluciones recurrentes
    if last_coordinate in solutions:
        maze["solutions"][last_coordinate] += 1
        recurrence_penalty = math.log(maze["solutions"][last_coordinate] + 1)
        return dist + recurrence_penalty
    
    else:
        maze["solutions"][last_coordinate] = 1
        return dist
    

def fitness_exp(path, maze, distance_factor=2):
    exit = maze["exit"]
    solutions = maze["solutions"]

    # Calculamos la distancia y la ajustamos con una función cuadrática
    last_coordinate = path[-1]
    dist = distance(last_coordinate[0], last_coordinate[1], exit[0], exit[1]) ** distance_factor

    if dist == 0:
        if last_coordinate in solutions:
            maze["solutions"][last_coordinate] += 1
        else:
            maze["solutions"][last_coordinate] = 1

        return 0 

    # Penalización de soluciones recurrentes
    if last_coordinate in solutions:
        maze["solutions"][last_coordinate] += 1
        return dist + maze["solutions"][last_coordinate]
    
    else:
        maze["solutions"][last_coordinate] = 1
        return dist
    
def fitness_sqrt(path, maze):
    exit = maze["exit"]
    solutions = maze["solutions"]
    
    # We calculate the distance
    last_coordinate = path[-1]
    dist = distance(last_coordinate[0], last_coordinate[1], exit[0], exit[1])

    if dist == 0:
        if last_coordinate in solutions:
            maze["solutions"][last_coordinate] += 1
        else:
            maze["solutions"][last_coordinate] = 1

        return 0 

    # We penalize recurring solutions
    if last_coordinate in solutions:
        maze["solutions"][last_coordinate] += 1
        rpt_sqrt = math.sqrt(maze["solutions"][last_coordinate])
        return dist * rpt_sqrt + rpt_sqrt
    
    else:
        maze["solutions"][last_coordinate] = 1
        return dist
        

def mutation(path, maze, mutation_rate):
    maze_matrix = maze["matrix"]
    entry = maze["entry"]           

    # We first pick where the mutations begins
    beg = int(len(path) * (1 - mutation_rate))
    end = len(path)

    random_idx = random.randint(beg, end)

    path = path[:random_idx]

    #usefull vars
    visited = set()

    # Now we generate a path
    current = entry
    to_generate = is_valid(current[0], current[1], visited, maze_matrix)
    path = [(current[1], current[0])]     # We have to put it backwards (not sure why)

    while to_generate:
        visited.add(current)

        random.shuffle(DIRECTIONS)
        for dx, dy in DIRECTIONS:                                                
            nx = current[0] + dx
            ny = current[1] + dy
                            
            if is_valid(nx, ny, visited, maze_matrix):
                current = (nx, ny)
                path.append((current[1], current[0]))
                break

        to_generate = is_valid(current[0], current[1], visited, maze_matrix)

    return path

def is_valid(x, y, visited, maze):
        if (x,y) in visited:
            return False
        
        return maze[x][y] == PATH

def crossover(path1, path2, maze):
    checkpoints = maze["checkpoints"]

    set_path1 = set(path1)
    set_path2 = set(path2)
    set_checkpoints = set(checkpoints)

    intersection = set_path1 & set_path2
    aval_checkpoints = intersection & set_checkpoints

    if not aval_checkpoints:
        return max([path1, path2], key=lambda path: fitness(path, maze))

    random_checkpoint = random.choice(list(aval_checkpoints))

    idx1 = None
    for index, point in enumerate(path1):
        if point == random_checkpoint:
            idx1 = index

    idx2 = None
    for index, point in enumerate(path2):
        if point == random_checkpoint:
            idx2 = index

    return path1[:idx1] + path2[idx2:]

def distance(x1, y1, x2, y2):
    return abs(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2))
    
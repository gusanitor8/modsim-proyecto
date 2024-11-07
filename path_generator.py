from constants import WALL, PATH
import random

class PathGenerator:
    DIRECTIONS = [(0,1), (0,-1), (1,0), (-1,0)]

    def __init__(self, maze, entry):
        self.maze = maze
        self.entry = entry        
        
        # path generation
        self.visited = set()
        self.paths = []

        random.seed(42)

    def generate_paths(self, path_no: int):
        for _ in range(path_no):
            self.generate_path()        

    def generate_path(self):
        current = self.entry
        to_generate = self.is_valid(current[0], current[1])
        path = [(current[1], current[0])]     # We have to put it backwards (not sure why)

        while to_generate:
            self.visited.add(current)

            random.shuffle(self.DIRECTIONS)
            for dx, dy in self.DIRECTIONS:                                                
                nx = current[0] + dx
                ny = current[1] + dy
                                
                if self.is_valid(nx, ny):
                    current = (nx, ny)
                    path.append((current[1], current[0]))
                    break

            to_generate = self.is_valid(current[0], current[1])

        self.paths.append(path)
        self.visited = set()

    def get_paths(self):
        return self.paths        
        
    def is_valid(self, x, y):
        if (x,y) in self.visited:
            return False
        
        return self.maze[x][y] == PATH
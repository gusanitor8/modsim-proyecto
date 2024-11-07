import random 
from constants import WALL, PATH

class MazeGenerator:
    DIRECTIONS = [(0, -2), (0, 2), (-2, 0), (2, 0)]

    def __init__(self, width=21, height=21):
        # Ensure width and height are odd for proper wall structure
        if width % 2 == 0: width += 1
        if height % 2 == 0: height += 1
        
        self.width = width
        self.height = height
        self.maze = [[WALL for _ in range(width)] for _ in range(height)]
        self.entry = (1, 1)
        self.exit = (width - 2, height - 2)
        self.checkpoints = []

        self.generate_maze()

    def get_maze(self):
        return self.maze
    
    def get_entry(self):
        return self.entry

    def get_exit(self):
        return self.exit
    
    def get_checkpoints(self):
        return set(self.checkpoints)

    def is_within_bounds(self, x, y):
        """Check if the coordinates are within the maze bounds."""
        return 0 <= x < self.width and 0 <= y < self.height

    def carve_passages_from(self, x, y):
        """Carve paths in the maze using DFS and backtracking."""
        self.maze[y][x] = PATH
        random.shuffle(self.DIRECTIONS)

        checkpoint_count = 0
        for dx, dy in self.DIRECTIONS:             
            nx, ny = x + dx, y + dy
            if self.is_within_bounds(nx, ny) and self.maze[ny][nx] == WALL:
                checkpoint_count += 1 
                # Carve a path between the current cell and the next cell
                self.maze[y + dy // 2][x + dx // 2] = PATH
                # Recursively carve passages from the next cell
                self.carve_passages_from(nx, ny)
        
        # We determine if the point (x,y) is a checkpoint
        if checkpoint_count >= 2:
            self.checkpoints.append((x,y))

    def generate_maze(self):
        """Generate the maze and set entry/exit points."""
        self.carve_passages_from(1, 1)
        # self.set_entry_and_exit()

    def set_entry_and_exit(self):
        """Set entry and exit points in the maze."""
        self.maze[self.entry[1]][self.entry[0]] = 'S'  # Start point
        self.maze[self.exit[1]][self.exit[0]] = 'E'  # End point

    def display_maze(self):
        """Print the maze to the console."""
        for row in self.maze:
            print("".join(row))
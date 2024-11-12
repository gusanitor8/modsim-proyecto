import random
import matplotlib.pyplot as plt
import pickle
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
    
    def get_matrix_dic(self, path=None):
        if path is not None:
            with open(path, 'rb') as file:
                maze_dic = pickle.load(file)

            return maze_dic

        return {
            "matrix": self.get_maze(),
            "entry": self.get_entry(),
            "exit": self.get_exit(),
            "checkpoints": self.get_checkpoints(),
            "solutions": {}        
        }
    
    def save_maze(self, path='mazes/my_dict.pkl'):
        my_dict = {
            "matrix": self.get_maze(),
            "entry": self.get_entry(),
            "exit": self.get_exit(),
            "checkpoints": self.get_checkpoints(),
            "solutions": {}        
        }

        # Open a file in binary write mode
        with open(path, 'wb') as file:
            pickle.dump(my_dict, file)
        

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

    def display_maze(self, checkpoints=False):
        """Display the maze with start and end points in different colors."""
        # Display the maze
        plt.imshow(self.maze, cmap="binary", interpolation="nearest")
        
        # Mark the start point (green) and end point (red)
        start_x, start_y = self.entry
        end_x, end_y = self.exit
        plt.scatter(start_x, start_y, color='green', s=100, label='Start')  # Green for start
        plt.scatter(end_x, end_y, color='red', s=100, label='End')          # Red for end

        # Optionally display the checkpoints in a different color (e.g., blue)
        if checkpoints:
            for checkpoint in self.checkpoints:
                plt.scatter(checkpoint[0], checkpoint[1], color='blue', s=50, alpha=0.5)

        plt.axis("off")  # Hide the axes
        plt.show()
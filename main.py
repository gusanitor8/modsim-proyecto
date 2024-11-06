from maze import MazeGenerator
from maze_drawer import matrix_to_image

if __name__ == "__main__":
    maze_gen = MazeGenerator()
    maze_matrix = maze_gen.get_maze()
    
    entry_position = maze_gen.get_entry()
    exit_position = maze_gen.get_exit()
    checkpoints = maze_gen.get_checkpoints()

    # Convert the matrix to an image
    maze_image = matrix_to_image(maze_matrix, entry_position, exit_position, cell_size=20)
    maze_image.show()  # Display the maze image
    maze_image.save("maze_output.png")  # Save the maze image``
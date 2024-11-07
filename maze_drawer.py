from PIL import Image

# Define colors for the maze
WALL_COLOR = (0, 0, 0)       # Black for walls
PATH_COLOR = (255, 255, 255)  # White for paths
ENTRY_COLOR = (0, 255, 0)     # Green for the entry point
EXIT_COLOR = (255, 0, 0)      # Red for the exit point
CHECKPOINT_COLOR = (255, 255, 0)  # Yellow for checkpoints
MADE_PATH_COLOR = (0, 255, 100)  # Path color 

def matrix_to_image(matrix, entry, exit, cell_size=20, checkpoints=set(), path = []):
    """
    Converts a binary matrix to an image of a maze.

    Parameters:
        matrix (list of list of int): A 2D list where 1 represents walls and 0 represents paths.
        entry (tuple): Coordinates (x, y) for the entry point.
        exit (tuple): Coordinates (x, y) for the exit point.
        cell_size (int): Size of each cell in pixels. Default is 20.
        checkpoints (list of tuple): List of (x, y) coordinates to mark as checkpoints in yellow.

    Returns:
        Image: A PIL Image object of the maze.
    """    
    path = set(path)
    height = len(matrix)
    width = len(matrix[0]) if height > 0 else 0
    img_width, img_height = width * cell_size, height * cell_size

    # Create a new image with RGB mode
    image = Image.new("RGB", (img_width, img_height), WALL_COLOR)
    pixels = image.load()

    # Draw the maze based on the matrix values
    for y in range(height):
        for x in range(width):
            # Set the color based on matrix values
            color = WALL_COLOR if matrix[y][x] == 1 else PATH_COLOR
            if (x, y) == entry:
                color = ENTRY_COLOR
            elif (x, y) == exit:
                color = EXIT_COLOR
            elif (x, y) in path:
                color = MADE_PATH_COLOR
            elif checkpoints and (x, y) in checkpoints:
                color = CHECKPOINT_COLOR
            
            # Fill the corresponding cell area with the color
            for i in range(cell_size):
                for j in range(cell_size):
                    pixels[x * cell_size + i, y * cell_size + j] = color

    return image
from maze import MazeGenerator
from maze_drawer import matrix_to_image
from path_generator import PathGenerator
from genetic_algorithm import GeneticAlgorithm
import pickle
from path_genetic import fitness, mutation, crossover
import random

EPOCHS = 100
POPULATION = 10


if __name__ == "__main__":
    random.seed(42)

    # maze_gen = MazeGenerator()
    # maze_matrix = maze_gen.get_maze()
    # entry_position = maze_gen.get_entry()
    # exit_position = maze_gen.get_exit()
    # checkpoints = maze_gen.get_checkpoints()

    # maze_dic = {
    #     "matrix": maze_matrix,
    #     "entry": entry_position,
    #     "exit": exit_position,
    #     "checkpoints": checkpoints
    # }

    # # Save to a file
    # with open('mazes/my_dict.pkl', 'wb') as file:
    #     pickle.dump(maze_dic, file)


    # Load from a file
    with open('mazes/my_dict.pkl', 'rb') as file:
        maze_dic = pickle.load(file)

    maze_matrix = maze_dic["matrix"]    
    entry_position = maze_dic["entry"]
    exit_position = maze_dic["exit"]
    checkpoints = maze_dic["checkpoints"]

    # Convert the matrix to an image
    maze_image = matrix_to_image(maze_matrix, entry_position, exit_position, cell_size=20, checkpoints=checkpoints)
    maze_image.show()  # Display the maze image
    maze_image.save("out/maze_output.png")  # Save the maze image

    path_gen = PathGenerator(maze_matrix, entry_position)
    path_gen.generate_paths(POPULATION)
    paths = path_gen.get_paths()
    
    maze_image = matrix_to_image(maze_matrix, entry_position, exit_position, cell_size=20, path=paths[0])    
    maze_image.save("out/maze_output_path.png")  # Save the maze image
    
    genetic = GeneticAlgorithm(paths, maze_dic, EPOCHS, POPULATION, fitness, crossover, mutation)
    new_population = genetic.run()

    # display solution
    maze_image = matrix_to_image(maze_matrix, entry_position, exit_position, cell_size=20, path=new_population[0])
    maze_image.show()  # Display the maze image
    maze_image.save("out/solution.png") 
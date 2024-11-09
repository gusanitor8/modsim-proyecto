import pygame
from maze import MazeGenerator
from maze_drawer import matrix_to_image
from path_generator import PathGenerator
from genetic_algorithm import GeneticAlgorithm
import pickle
from path_genetic import fitness, mutation, crossover
import random
from animator import MazeSolver

EPOCHS = 1000
POPULATION = 50

if __name__ == "__main__":

    #random.seed(42)
    maze_gen = MazeGenerator(50,50)
    maze_matrix = maze_gen.get_maze()
    entry_position = maze_gen.get_entry()
    exit_position = maze_gen.get_exit()
    checkpoints = maze_gen.get_checkpoints()

    maze_dic = {
        "matrix": maze_matrix,
        "entry": entry_position,
        "exit": exit_position,
        "checkpoints": checkpoints
    }

    # Cargar desde un archivo
    # with open('mazes/my_dict.pkl', 'rb') as file:
    #     maze_dic = pickle.load(file)

    # # Cargar la data del laberinto desde el archivo
    # maze_matrix = maze_dic["matrix"]
    # entry_position = maze_dic["entry"]
    # exit_position = maze_dic["exit"]
    # checkpoints = maze_dic["checkpoints"]

    # Generar una población de caminos inicial
    path_gen = PathGenerator(maze_matrix, entry_position)
    path_gen.generate_paths(POPULATION)
    paths = path_gen.get_paths()

    # Aplicar el algoritmo genético para encontrar la solución
    genetic = GeneticAlgorithm(paths, maze_dic, EPOCHS, POPULATION, fitness, crossover, mutation)
    generations, fitness_history = genetic.run()

    # Mostrar solución en una ventana de Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    solver = MazeSolver(maze_matrix, generations, screen, clock)
    solver.run_animation()

    pygame.quit()

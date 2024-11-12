import pygame
from maze import MazeGenerator
from path_generator import PathGenerator
from genetic_algorithm import GeneticAlgorithm
from gen_functions import fitness_explore, mutation, crossover
from animator import MazeSolver

EPOCHS = 1000
POPULATION = 50
MUTATION_RATE = 0.5

if __name__ == "__main__":

    maze_gen = MazeGenerator(50,50)   
    maze_dic = maze_gen.get_matrix_dic("mazes/my_dict.pkl")

    # Cargar la data del laberinto desde el archivo
    maze_matrix = maze_dic["matrix"]
    entry_position = maze_dic["entry"]
    exit_position = maze_dic["exit"]
    checkpoints = maze_dic["checkpoints"]

    # Generar una población de caminos inicial
    path_gen = PathGenerator(maze_matrix, entry_position)
    path_gen.generate_paths(POPULATION)
    paths = path_gen.get_paths()

    # Aplicar el algoritmo genético para encontrar la solución
    genetic = GeneticAlgorithm(paths, maze_dic, MUTATION_RATE, EPOCHS, POPULATION, fitness_explore, crossover, mutation)
    generations, fitness_history, solution_found, final_epoch = genetic.run()
    if solution_found:
        print("solution_found!")

    # Mostrar solución en una ventana de Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()

    solver = MazeSolver(maze_matrix, generations, screen, clock)
    solver.run_animation()

    pygame.quit()

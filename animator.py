import pygame
import time
# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (113, 121, 126)

class MazeSolver:
    def __init__(self, maze, generations, screen, clock):
        self.maze = maze
        self.generations = generations
        self.screen = screen
        self.clock = clock

        # Fuentes para los diferentes textos
        self.title_font = pygame.font.Font(None, 48)  # Fuente más grande para el título
        self.generation_font = pygame.font.Font(None, 40)  # Fuente mediana para información inferior

        # Dimensiones del laberinto
        self.maze_height = len(maze)
        self.maze_width = len(maze[0]) if self.maze_height > 0 else 0

        # Dimensiones de la pantalla
        self.screen_width = screen.get_width()
        self.screen_height = screen.get_height()

        # Márgenes ajustados
        self.top_margin = 90
        self.bottom_margin = 100
        self.left_margin = 50
        self.right_margin = 50

        # Área disponible para dibujar el laberinto
        self.available_width = self.screen_width - self.left_margin - self.right_margin
        self.available_height = self.screen_height - self.top_margin - self.bottom_margin

        # Tamaño de cada celda (dinámico)
        self.cell_size = min(self.available_width / self.maze_width, self.available_height / self.maze_height) * 1.1

        # Tamaño real del laberinto dibujado
        self.maze_draw_width = self.cell_size * self.maze_width
        self.maze_draw_height = self.cell_size * self.maze_height

        # Desplazamientos para centrar el laberinto
        self.offset_x = self.left_margin + (self.available_width - self.maze_draw_width) / 2
        self.offset_y = self.top_margin + (self.available_height - self.maze_draw_height) / 2

    def draw_maze(self):
        # Coordenadas de la salida y la meta
        start_pos = (1, 1)
        end_pos = (self.maze_height - 2, self.maze_width - 2)

        # Dibuja el laberinto centrado en la pantalla
        for x, row in enumerate(self.maze):
            for y, cell in enumerate(row):
                color = GRAY if cell == 0 else BLACK
                rect = pygame.Rect(
                    self.offset_x + y * self.cell_size,
                    self.offset_y + x * self.cell_size,
                    self.cell_size + 1,  # Añade 1 píxel al ancho
                    self.cell_size + 1   # Añade 1 píxel a la altura
                )
                pygame.draw.rect(self.screen, color, rect)

        # Dibuja la salida en verde
        start_rect = pygame.Rect(
            self.offset_x + start_pos[0] * self.cell_size,
            self.offset_y + start_pos[1] * self.cell_size,
            self.cell_size + 1,
            self.cell_size + 1
        )
        pygame.draw.rect(self.screen, GREEN, start_rect)  # Verde

        # Dibuja la meta en rojo
        end_rect = pygame.Rect(
            self.offset_x + end_pos[0] * self.cell_size,
            self.offset_y + end_pos[1] * self.cell_size,
            self.cell_size + 1,
            self.cell_size + 1
        )
        pygame.draw.rect(self.screen, RED, end_rect)  # Rojo


    def display_top_text(self):
        # Muestra el título con menos padding
        n = self.maze_width
        title_text = self.title_font.render(f"Laberinto de {n}x{n} celdas", True, BLACK)
        title_rect = title_text.get_rect(center=(self.screen_width / 2, self.top_margin / 2 - 10))
        self.screen.blit(title_text, title_rect)


    def display_bottom_text(self, generation_number):
        # Muestra el texto de la generación actual en la parte inferior, centrado y más grande
        generation_text = self.generation_font.render(f"Generación Actual: {generation_number}", True, BLACK)
        generation_rect = generation_text.get_rect(center=(self.screen_width / 2, self.screen_height - self.bottom_margin / 2))
        self.screen.blit(generation_text, generation_rect)


    def animate_generation(self, population, generation_number, speed):
        agents = []
        # Crear "agentes" para cada camino en la población, asignando un frame de inicio escalonado
        for i, path in enumerate(population):
            agents.append({
                "path": path,
                "index": 0,
                "color": BLUE,
                "finished": False,
                "start_frame": i  # Cada agente empieza un frame después del anterior
            })

        step = 0  # Contador de frames global para controlar el inicio de cada agente
        running = True
        while running:
            self.screen.fill(GRAY)  # Limpia la pantalla
            self.draw_maze()  # Dibuja el laberinto
            self.display_top_text()  # Muestra el texto superior
            self.display_bottom_text(generation_number)  # Muestra el texto inferior

            running = False  # Este valor se usará para detener el bucle si todos los agentes han terminado

            for agent in agents:
                # Si el agente no ha terminado y ha llegado a su frame de inicio, sigue avanzando
                if not agent["finished"] and step >= agent["start_frame"]:
                    running = True  # Al menos un agente sigue en movimiento
                    if agent["index"] < len(agent["path"]):
                        pos = agent["path"][agent["index"]]
                        agent["position"] = pos  # Guarda la posición actual
                        agent["index"] += 1  # Mover al siguiente paso en el camino
                    else:
                        agent["finished"] = True  # Marca el agente como terminado

                # Dibuja el agente en su última posición si ya ha comenzado
                if "position" in agent:
                    pos = agent["position"]
                    pygame.draw.circle(
                        self.screen,
                        agent["color"],
                        (
                            self.offset_x + pos[0] * self.cell_size + self.cell_size / 2,
                            self.offset_y + pos[1] * self.cell_size + self.cell_size / 2
                        ),
                        self.cell_size / 2
                    )

            pygame.display.flip()  # Actualiza la pantalla
            self.clock.tick(speed)  # Controla la velocidad de la animación
            time.sleep(0.01)  # Pausa breve para suavizar la animación
            step += 1  # Incrementa el contador de frames


    def run_animation(self):
        pygame.display.set_caption("Solucionador de Laberintos con Algoritmos Genéticos")
        total_generations = len(self.generations)
        
        # Determinar las generaciones a mostrar
        generations_to_show = []
        if total_generations > 1:
            generations_to_show.append(0)  # Primera generación
            if total_generations > 2:
                generations_to_show.append(1)  # Segunda generación
            if total_generations > 3:
                generations_to_show.append(2)  # Tercera generación
            if total_generations > 4:
                generations_to_show.append(total_generations - 3)  # Antepenúltima generación
            if total_generations > 5:
                generations_to_show.append(total_generations - 2)  # Penúltima generación
            if total_generations > 6:
                generations_to_show.append(total_generations - 1)  # Última generación

            # Añadir 5 generaciones intermedias si el número total de generaciones es suficiente
            if total_generations > 10:
                mid_generations = total_generations // 5
                generations_to_show += [mid_generations * i for i in range(1, 5)]

            generations_to_show = sorted(set(generations_to_show))

        # Loop para animar solo las generaciones seleccionadas con diferentes velocidades
        for i, generation_number in enumerate(generations_to_show):
            if generation_number >= total_generations:
                break
            generation = self.generations[generation_number]

            # Definir velocidad de animación según posición de la generación
            if i == 0 or i == len(generations_to_show) - 1:  # Primera y última
                speed = 15
            elif i == 1 or i == len(generations_to_show) - 2:  # Segunda y penúltima
                speed = 25
            elif i == 2 or i == len(generations_to_show) - 3:  # Tercera y antepenúltima
                speed = 35
            else:  # Generaciones intermedias más rápidas
                speed = 60

            # Llamar a la animación con la velocidad definida
            self.animate_generation(generation, generation_number, speed)
            time.sleep(0.5)  # Pausa entre generaciones

        # Espera a que el usuario cierre la ventana
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
            self.clock.tick(60)
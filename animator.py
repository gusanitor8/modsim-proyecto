import pygame
import time

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
        # Dibuja el laberinto centrado en la pantalla
        for x, row in enumerate(self.maze):
            for y, cell in enumerate(row):
                color = (255, 255, 255) if cell == 0 else (0, 0, 0)
                rect = pygame.Rect(
                    self.offset_x + y * self.cell_size,
                    self.offset_y + x * self.cell_size,
                    self.cell_size + 1,  # Añade 1 píxel al ancho
                    self.cell_size + 1   # Añade 1 píxel a la altura
                )
                pygame.draw.rect(self.screen, color, rect)

    def display_top_text(self):
        # Muestra el título con menos padding
        n = self.maze_width
        title_text = self.title_font.render(f"Laberinto de {n}x{n} celdas", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.screen_width / 2, self.top_margin / 2 - 10))
        self.screen.blit(title_text, title_rect)


    def display_bottom_text(self, generation_number):
        # Muestra el texto de la generación actual en la parte inferior, centrado y más grande
        generation_text = self.generation_font.render(f"Generación Actual: {generation_number}", True, (0, 0, 0))
        generation_rect = generation_text.get_rect(center=(self.screen_width / 2, self.screen_height - self.bottom_margin / 2))
        self.screen.blit(generation_text, generation_rect)


    def animate_generation(self, population, generation_number):
        agents = []
        # Crear "agentes" para cada camino en la población
        for path in population:
            start_pos = path[0]  # posición inicial de cada camino
            agents.append({"path": path, "index": 0, "color": (0, 0, 255), "finished": False})

        # Animar cada paso del camino
        for step in range(max(len(agent["path"]) for agent in agents)):
            self.screen.fill((255, 255, 255))  # Limpia la pantalla
            self.draw_maze()  # Dibuja el laberinto
            self.display_top_text()  # Muestra el texto superior
            self.display_bottom_text(generation_number)  # Muestra el texto inferior

            for agent in agents:
                # Si el agente no ha terminado, sigue avanzando
                if not agent["finished"]:
                    if agent["index"] < len(agent["path"]):
                        pos = agent["path"][agent["index"]]
                        agent["position"] = pos  # Guarda la posición actual
                        agent["index"] += 1  # Mover al siguiente paso en el camino
                    else:
                        agent["finished"] = True  # Marca el agente como terminado

                # Dibuja el agente en su última posición
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
            self.clock.tick(20)  # Controla la velocidad de la animación
            time.sleep(0.02)  # Pausa breve para suavizar la animación

    def run_animation(self):
        pygame.display.set_caption("Solucionador de Laberintos con Algoritmos Genéticos")  # Título de la ventana
        running = True
        for generation_number, generation in enumerate(self.generations, start=1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
            if not running:
                break
            self.animate_generation(generation, generation_number)
            time.sleep(0.5)  # Pausa entre generaciones
        # Espera a que el usuario cierre la ventana
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            pygame.display.flip()
            self.clock.tick(60)

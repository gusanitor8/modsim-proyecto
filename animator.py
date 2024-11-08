import pygame
import time

class MazeSolver:
    def __init__(self, maze, generations, screen, clock):
        self.maze = maze  # matriz del laberinto
        self.generations = generations  # lista de poblaciones de cada generación
        self.cell_size = 20  # Tamaño de cada celda (ajusta según sea necesario)
        self.screen = screen
        self.clock = clock
        self.font = pygame.font.Font(None, 36)  # Fuente para el texto de la generación
        
    def draw_maze(self):
        # Dibuja el laberinto en la pantalla
        for x, row in enumerate(self.maze):
            for y, cell in enumerate(row):
                color = (255, 255, 255) if cell == 0 else (0, 0, 0)
                pygame.draw.rect(self.screen, color, pygame.Rect(y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size))

    def display_generation_text(self, generation_number):
        # Renderizar el texto de la generación
        text = self.font.render(f"Generación: {generation_number}", True, (0, 0, 0))
        self.screen.blit(text, (10, 10))  # Posiciona el texto en la parte superior izquierda de la pantalla

    def animate_generation(self, population, generation_number):
        agents = []
        
        # Crear "agentes" como círculos para cada camino en la población
        for path in population:
            start_pos = path[0]  # posición inicial de cada camino
            agents.append({"path": path, "index": 0, "color": (0, 0, 255, 128), "finished": False})  # Agrega transparencia del 50%

        # Animar cada paso del camino
        for step in range(max(len(agent["path"]) for agent in agents)):
            self.screen.fill((255, 255, 255))  # Limpia la pantalla con un color blanco
            self.draw_maze()  # Dibuja el laberinto
            self.display_generation_text(generation_number)  # Muestra la generación actual

            for agent in agents:
                # Si el agente no ha terminado, sigue avanzando
                if not agent["finished"]:
                    if agent["index"] < len(agent["path"]):
                        pos = agent["path"][agent["index"]]
                        agent["position"] = pos  # Guarda la posición final
                        agent["index"] += 1  # Mover al siguiente paso en el camino
                    else:
                        # Marca el agente como terminado
                        agent["finished"] = True

                # Dibuja el agente en su última posición
                pos = agent["position"]
                pygame.draw.circle(self.screen, agent["color"], 
                                   (pos[0] * self.cell_size + self.cell_size // 2, 
                                    pos[1] * self.cell_size + self.cell_size // 2), 
                                   self.cell_size // 2)

            pygame.display.flip()  # Actualiza la pantalla completa
            self.clock.tick(20)  # Aumenta el framerate para una animación más fluida
            
            # Reduce el delay entre cada paso para suavizar la animación
            time.sleep(0.02)

    def run_animation(self):
        for generation_number, generation in enumerate(self.generations, start=1):
            self.animate_generation(generation, generation_number)
            time.sleep(0.5)  # Pausa entre generaciones para resaltar el cambio

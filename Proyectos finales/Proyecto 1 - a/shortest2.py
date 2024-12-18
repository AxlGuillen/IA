import pygame
import heapq
import math

# Configuraciones iniciales
ANCHO_VENTANA = 800
VENTANA = pygame.display.set_mode((ANCHO_VENTANA, ANCHO_VENTANA))
pygame.display.set_caption("Visualización de Nodos")

# Colores (RGB)
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
GRIS = (128, 128, 128)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
NARANJA = (255, 165, 0)
PURPURA = (128, 0, 128)
AZUL = (0, 0, 255)
CERRADO = (192, 192, 192)

class Nodo:
    def __init__(self, fila, col, ancho, total_filas):
        self.fila = fila
        self.col = col
        self.x = fila * ancho
        self.y = col * ancho
        self.color = BLANCO
        self.ancho = ancho
        self.total_filas = total_filas
        self.vecinos = []
        self.g = float("inf")
        self.f = float("inf")

    def get_pos(self):
        return self.fila, self.col

    def es_pared(self):
        return self.color == NEGRO

    def es_inicio(self):
        return self.color == NARANJA

    def es_fin(self):
        return self.color == PURPURA

    def restablecer(self):
        self.color = BLANCO

    def hacer_inicio(self):
        self.color = NARANJA

    def hacer_pared(self):
        self.color = NEGRO

    def hacer_fin(self):
        self.color = PURPURA

    def hacer_camino(self):
        self.color = AZUL

    def hacer_cerrado(self):
        self.color = CERRADO

    def actualizar_vecinos(self, grid):
        self.vecinos = []
        # Arriba
        if self.fila > 0 and not grid[self.fila - 1][self.col].es_pared():
            self.vecinos.append((grid[self.fila - 1][self.col], 1))
        # Abajo
        if self.fila < self.total_filas - 1 and not grid[self.fila + 1][self.col].es_pared():
            self.vecinos.append((grid[self.fila + 1][self.col], 1))
        # Izquierda
        if self.col > 0 and not grid[self.fila][self.col - 1].es_pared():
            self.vecinos.append((grid[self.fila][self.col - 1], 1))
        # Derecha
        if self.col < self.total_filas - 1 and not grid[self.fila][self.col + 1].es_pared():
            self.vecinos.append((grid[self.fila][self.col + 1], 1))
        # Diagonales
        if self.fila > 0 and self.col > 0 and not grid[self.fila - 1][self.col - 1].es_pared():
            self.vecinos.append((grid[self.fila - 1][self.col - 1], math.sqrt(2)))
        if self.fila > 0 and self.col < self.total_filas - 1 and not grid[self.fila - 1][self.col + 1].es_pared():
            self.vecinos.append((grid[self.fila - 1][self.col + 1], math.sqrt(2)))
        if self.fila < self.total_filas - 1 and self.col > 0 and not grid[self.fila + 1][self.col - 1].es_pared():
            self.vecinos.append((grid[self.fila + 1][self.col - 1], math.sqrt(2)))
        if self.fila < self.total_filas - 1 and self.col < self.total_filas - 1 and not grid[self.fila + 1][
            self.col + 1].es_pared():
            self.vecinos.append((grid[self.fila + 1][self.col + 1], math.sqrt(2)))

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, (self.x, self.y, self.ancho, self.ancho))

    def __lt__(self, otro):
        return self.f < otro.f

def crear_grid(filas, ancho):
    grid = []
    ancho_nodo = ancho // filas
    for i in range(filas):
        grid.append([])
        for j in range(filas):
            nodo = Nodo(i, j, ancho_nodo, filas)
            grid[i].append(nodo)
    return grid

def dibujar_grid(ventana, filas, ancho):
    ancho_nodo = ancho // filas
    for i in range(filas):
        pygame.draw.line(ventana, GRIS, (0, i * ancho_nodo), (ancho, i * ancho_nodo))
        for j in range(filas):
            pygame.draw.line(ventana, GRIS, (j * ancho_nodo, 0), (j * ancho_nodo, ancho))

def dibujar(ventana, grid, filas, ancho):
    ventana.fill(BLANCO)
    for fila in grid:
        for nodo in fila:
            nodo.dibujar(ventana)

    dibujar_grid(ventana, filas, ancho)
    pygame.display.update()

def obtener_click_pos(pos, filas, ancho):
    ancho_nodo = ancho // filas
    y, x = pos
    fila = y // ancho_nodo
    col = x // ancho_nodo
    return fila, col

def heuristica(nodo1, nodo2):
    """Calcula la distancia Manhattan entre dos nodos."""
    x1, y1 = nodo1.get_pos()
    x2, y2 = nodo2.get_pos()
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruir_camino(came_from, current, dibujar, inicio, fin):
    """Reconstruye el camino desde el nodo final hasta el inicial."""
    while current in came_from:
        current = came_from[current]
        if current != inicio and current != fin:  # Evitar colorear inicio y fin
            current.hacer_camino()
        dibujar()

def algoritmo_a_estrella(dibujar, grid, inicio, fin):
    open_set = []
    heapq.heappush(open_set, (0, inicio))
    came_from = {}
    inicio.g = 0
    inicio.f = heuristica(inicio, fin)
    open_set_hash = {inicio}

    closed_set = set()  # Definir el conjunto para la lista cerrada

    while open_set:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = heapq.heappop(open_set)[1]
        open_set_hash.remove(current)

        # Agregar a la lista cerrada si no está ya
        if current not in closed_set:
            closed_set.add(current)
            if current != inicio and current != fin:
                current.hacer_cerrado()  # Colorear el nodo como cerrado

        if current == fin:
            reconstruir_camino(came_from, fin, dibujar, inicio, fin)

            # Imprimir la lista abierta
            open_positions = [nodo.get_pos() for nodo in open_set_hash]
            print("Lista abierta (open set):")
            print(open_positions)

            # Imprimir la lista cerrada
            closed_positions = [nodo.get_pos() for nodo in closed_set]
            print("Lista cerrada (closed set):")
            print(closed_positions)

            return True

        for vecino, costo in current.vecinos:
            tentative_g_score = current.g + costo  # Costo es 1 para ortogonales, √2 para diagonales
            if tentative_g_score < vecino.g:
                came_from[vecino] = current
                vecino.g = tentative_g_score
                vecino.f = vecino.g + heuristica(vecino, fin)

                if vecino not in open_set_hash and vecino not in closed_set:
                    heapq.heappush(open_set, (vecino.f, vecino))
                    open_set_hash.add(vecino)

        dibujar()
        pygame.time.delay(50)

    # Si no se encontró un camino, imprimir la lista cerrada
    closed_positions = [nodo.get_pos() for nodo in closed_set]
    print("Lista cerrada (closed set):")
    print(closed_positions)
    return False

def main(ventana, ancho):
    FILAS = 9
    grid = crear_grid(FILAS, ancho)

    inicio = None
    fin = None

    corriendo = True

    while corriendo:
        dibujar(ventana, grid, FILAS, ancho)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                corriendo = False

            if pygame.mouse.get_pressed()[0]:  # Click izquierdo
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                if fila < 0 or fila >= FILAS or col < 0 or col >= FILAS:
                    continue
                nodo = grid[fila][col]
                if not inicio and nodo != fin:
                    inicio = nodo
                    inicio.hacer_inicio()

                elif not fin and nodo != inicio:
                    fin = nodo
                    fin.hacer_fin()

                elif nodo != fin and nodo != inicio:
                    nodo.hacer_pared()

            elif pygame.mouse.get_pressed()[2]:  # Click derecho
                pos = pygame.mouse.get_pos()
                fila, col = obtener_click_pos(pos, FILAS, ancho)
                if fila < 0 or fila >= FILAS or col < 0 or col >= FILAS:
                    continue
                nodo = grid[fila][col]
                nodo.restablecer()
                if nodo == inicio:
                    inicio = None
                elif nodo == fin:
                    fin = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and inicio and fin:
                    for fila in grid:
                        for nodo in fila:
                            nodo.actualizar_vecinos(grid)

                    algoritmo_a_estrella(lambda: dibujar(ventana, grid, FILAS, ancho), grid, inicio, fin)

    pygame.quit()

main(VENTANA, ANCHO_VENTANA)
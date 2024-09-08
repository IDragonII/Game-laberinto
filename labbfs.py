import pygame
import sys
import time
from collections import deque

pygame.init()

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)
GRIS = (200, 200, 200)

ANCHO = 600
ALTO = 600
TAM_CELDA = 30

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Resolución de Laberinto - BFS")

laberinto = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

inicio = (1, 1)
fin = (10, 18)

def dibujar_laberinto():
    for fila in range(len(laberinto)):
        for col in range(len(laberinto[0])):
            color = BLANCO if laberinto[fila][col] == 0 else NEGRO
            pygame.draw.rect(pantalla, color, (col * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA))
    pygame.draw.rect(pantalla, VERDE, (inicio[1] * TAM_CELDA, inicio[0] * TAM_CELDA, TAM_CELDA, TAM_CELDA))
    pygame.draw.rect(pantalla, ROJO, (fin[1] * TAM_CELDA, fin[0] * TAM_CELDA, TAM_CELDA, TAM_CELDA))

def bfs(laberinto, inicio):
    cola = deque([inicio])
    visitado = set([inicio])
    camino = {inicio: None}

    while cola:
        actual = cola.popleft()

        if actual == fin:
            break

        x, y = actual

        for mov in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + mov[0], y + mov[1]

            if (0 <= nx < len(laberinto) and 0 <= ny < len(laberinto[0]) and
                    laberinto[nx][ny] == 0 and (nx, ny) not in visitado):
                visitado.add((nx, ny))
                camino[(nx, ny)] = actual
                cola.append((nx, ny))

                time.sleep(0.05)
                pygame.draw.rect(pantalla, AZUL, (ny * TAM_CELDA, nx * TAM_CELDA, TAM_CELDA, TAM_CELDA))
                pygame.display.update()

    if actual == fin:
        while actual:
            pygame.draw.rect(pantalla, VERDE, (actual[1] * TAM_CELDA, actual[0] * TAM_CELDA, TAM_CELDA, TAM_CELDA))
            pygame.display.update()
            actual = camino[actual]

def main():
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pantalla.fill(BLANCO)
        dibujar_laberinto()

        bfs(laberinto, inicio)

        pygame.display.update()

if __name__ == "__main__":
    main()

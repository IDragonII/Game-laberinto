import pygame
import sys
import time

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
pygame.display.set_caption("Resolución de Laberinto - DFS")

laberinto = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 1],
    [1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
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

def dfs(laberinto, pos, visitado):
    if pos == fin:
        return True

    x, y = pos
    visitado.add(pos)

    for mov in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + mov[0], y + mov[1]
        if (0 <= nx < len(laberinto) and 0 <= ny < len(laberinto[0]) and
                laberinto[nx][ny] == 0 and (nx, ny) not in visitado):
            time.sleep(0.05)
            pygame.draw.rect(pantalla, AZUL, (ny * TAM_CELDA, nx * TAM_CELDA, TAM_CELDA, TAM_CELDA))
            pygame.display.update()

            if dfs(laberinto, (nx, ny), visitado):
                pygame.draw.rect(pantalla, VERDE, (ny * TAM_CELDA, nx * TAM_CELDA, TAM_CELDA, TAM_CELDA))
                pygame.display.update()
                return True

            time.sleep(0.05)
            pygame.draw.rect(pantalla, GRIS, (ny * TAM_CELDA, nx * TAM_CELDA, TAM_CELDA, TAM_CELDA))
            pygame.display.update()

    return False

def main():
    visitado = set()
    ejecutando = True

    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pantalla.fill(BLANCO)
        dibujar_laberinto()

        dfs(laberinto, inicio, visitado)

        pygame.display.update()

if __name__ == "__main__":
    main()

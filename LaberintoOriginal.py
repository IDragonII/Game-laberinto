import pygame
import heapq
import time
from collections import deque

ANCHO_MAXIMO = 700
ALTO_MAXIMO = 700
COLOR_VISITADO = (173, 216, 230)
COLOR_TEXTO = (255, 255, 255)
FPS = 30

def cargar_laberinto(archivo):
    with open(archivo, 'r') as f:
        laberinto = [list(line.strip()) for line in f.readlines()]
    return laberinto

def encontrar_posicion(laberinto, caracter):
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == caracter:
                return (fila, columna)
    return None

def calcular_tamano_celdas(filas, columnas):
    tam_celda = min(ANCHO_MAXIMO // columnas, ALTO_MAXIMO // filas)
    return tam_celda


def resolver_laberinto(laberinto, inicio, fin, pantalla, imagen_pared, tam_celda, modo_automatico, velocidad, imagen_camino_original, imagen_inicio, imagen_objetivo, metodo_resolucion="A*"):
    filas, columnas = len(laberinto), len(laberinto[0])
    movimientos = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def heuristica(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    if metodo_resolucion == "A*" or metodo_resolucion == "Greedy":
        cola = []
        heapq.heappush(cola, (0, inicio))
    elif metodo_resolucion == "BFS":
        cola = deque([inicio])
    elif metodo_resolucion == "DFS":
        cola = [inicio]

    padres = {}
    padres[inicio] = None

    costos = {}
    costos[inicio] = 0

    reloj = pygame.time.Clock()

    while cola:
        if metodo_resolucion == "A*" or metodo_resolucion == "Greedy":
            _, actual = heapq.heappop(cola)
        elif metodo_resolucion == "BFS":
            actual = cola.popleft()
        elif metodo_resolucion == "DFS":
            actual = cola.pop()

        if actual == fin:
            camino = []
            while actual:
                camino.append(actual)
                actual = padres[actual]
            return camino[::-1]

        for movimiento in movimientos:
            vecino = (actual[0] + movimiento[0], actual[1] + movimiento[1])
            if 0 <= vecino[0] < filas and 0 <= vecino[1] < columnas:
                if laberinto[vecino[0]][vecino[1]] != '#':
                    nuevo_costo = costos[actual] + 1
                    heur = heuristica(vecino, fin)

                    if metodo_resolucion == "A*":
                        prioridad = nuevo_costo + heur  # A*
                    elif metodo_resolucion == "Greedy":
                        prioridad = heur  # Greedy
                    elif metodo_resolucion == "BFS" or metodo_resolucion == "DFS":
                        prioridad = nuevo_costo

                    if vecino not in costos or nuevo_costo < costos[vecino]:
                        costos[vecino] = nuevo_costo
                        if metodo_resolucion == "A*" or metodo_resolucion == "Greedy":
                            heapq.heappush(cola, (prioridad, vecino))
                        else:
                            if metodo_resolucion == "BFS":
                                cola.append(vecino)
                            else:  # DFS
                                cola.append(vecino)

                        padres[vecino] = actual

                        if laberinto[vecino[0]][vecino[1]] not in ('S', 'E'):
                            laberinto[vecino[0]][vecino[1]] = 'V'
                            dibujar_laberinto(pantalla, laberinto, imagen_pared, tam_celda, imagen_camino_original, imagen_inicio, imagen_objetivo)
                            pygame.display.update()
                            if modo_automatico:
                                time.sleep(velocidad)

    return None

def dibujar_laberinto(pantalla, laberinto, imagen_pared, tam_celda, imagen_camino_original,imagen_inicio,imagen_objetivo):
    if pantalla is None:
        return
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == '#':
                pantalla.blit(imagen_pared, (columna * tam_celda, fila * tam_celda))
            elif laberinto[fila][columna] == 'S':
                pantalla.blit(imagen_camino_original, (columna * tam_celda, fila * tam_celda))
                pantalla.blit(imagen_inicio, (columna * tam_celda, fila * tam_celda))
            elif laberinto[fila][columna] == 'E':
                pantalla.blit(imagen_camino_original, (columna * tam_celda, fila * tam_celda))
                pantalla.blit(imagen_objetivo, (columna * tam_celda, fila * tam_celda))
            elif laberinto[fila][columna] == 'V':
                pygame.draw.rect(pantalla, COLOR_VISITADO, (columna * tam_celda, fila * tam_celda, tam_celda, tam_celda))
            else:
                pantalla.blit(imagen_camino_original, (columna * tam_celda, fila * tam_celda))

def mostrar_seleccion_metodo(pantalla, botones, fuente, fondo_menu, imagen_boton_normal, imagen_boton_hover):
    if pantalla is None:
        return None

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for metodo, boton in botones.items():
                    if boton.collidepoint(evento.pos):
                        return metodo

        pantalla.blit(fondo_menu, (200, 200))
        for texto, boton in botones.items():
            dibujar_boton(pantalla, texto, boton, imagen_boton_normal, imagen_boton_hover, COLOR_TEXTO, fuente)
        pygame.display.update()

def limpiar_caminos_explorados(laberinto, camino):
    for fila in range(len(laberinto)):
        for columna in range(len(laberinto[0])):
            if laberinto[fila][columna] == 'V' and (fila, columna) not in camino:
                laberinto[fila][columna] = ' '

def mostrar_camino(pantalla, laberinto, camino, inicio, fin, imagen_pared, tam_celda,imagen_camino,imagen_inicio,imagen_objetivo):
    if pantalla is None:
        return

    limpiar_caminos_explorados(laberinto, camino)

    for posicion in camino:
        if posicion != inicio and posicion != fin:
            laberinto[posicion[0]][posicion[1]] = '*'

    dibujar_laberinto(pantalla, laberinto, imagen_pared, tam_celda,imagen_camino,imagen_inicio,imagen_objetivo)
    pygame.display.update()

def mover_personaje(pantalla, laberinto, camino, inicio, fin, imagen_pared, imagen_personaje, tam_celda,imagen_camino,imagen_inicio,imagen_objetivo):
    if pantalla is None:
        return 0

    reloj = pygame.time.Clock()
    cantidad_movimientos = 0

    for posicion in camino:
        if pantalla is None:
            return 0

        dibujar_laberinto(pantalla, laberinto, imagen_pared, tam_celda,imagen_camino,imagen_inicio,imagen_objetivo)
        pantalla.blit(imagen_personaje, (posicion[1] * tam_celda, posicion[0] * tam_celda))
        pygame.display.update()

        reloj.tick(FPS)
        time.sleep(0.1)
        cantidad_movimientos += 1

    return cantidad_movimientos

def mover_personaje_manual(pantalla, laberinto, posicion_actual, fin, imagen_pared, imagen_personaje, tam_celda,imagen_camino,imagen_inicio, imagen_objetivo):
    if pantalla is None:
        return 0

    reloj = pygame.time.Clock()
    movimientos = {
        pygame.K_UP: (-1, 0),
        pygame.K_DOWN: (1, 0),
        pygame.K_LEFT: (0, -1),
        pygame.K_RIGHT: (0, 1)
    }

    cantidad_movimientos = 0
    jugando = True
    while jugando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return 0
            if evento.type == pygame.KEYDOWN:
                if evento.key in movimientos:
                    movimiento = movimientos[evento.key]
                    nueva_posicion = (posicion_actual[0] + movimiento[0], posicion_actual[1] + movimiento[1])
                    if 0 <= nueva_posicion[0] < len(laberinto) and 0 <= nueva_posicion[1] < len(laberinto[0]):
                        if laberinto[nueva_posicion[0]][nueva_posicion[1]] != '#':
                            posicion_actual = nueva_posicion
                            cantidad_movimientos += 1
                            if posicion_actual == fin:
                                return cantidad_movimientos

        dibujar_laberinto(pantalla, laberinto, imagen_pared, tam_celda,imagen_camino,imagen_inicio,imagen_objetivo)
        pantalla.blit(imagen_personaje, (posicion_actual[1] * tam_celda, posicion_actual[0] * tam_celda))
        pygame.display.update()
        reloj.tick(FPS)

    return 0

def dibujar_boton(pantalla, texto, rect, imagen_boton_normal, imagen_boton_hover, color_texto, fuente):
    if pantalla is None:
        return

    mouse = pygame.mouse.get_pos()

    if rect.collidepoint(mouse):
        pantalla.blit(imagen_boton_hover, rect.topleft)
    else:
        pantalla.blit(imagen_boton_normal, rect.topleft)

    texto_superficie = fuente.render(texto, True, color_texto)
    texto_rect = texto_superficie.get_rect(center=rect.center)
    pantalla.blit(texto_superficie, texto_rect)


def mostrar_ganador(pantalla, imagen_winner, boton_reintentar, fuente, cantidad_movimientos, imagen_boton_normal, imagen_boton_hover):
    if pantalla is None:
        return

    mouse_pressed = False

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reintentar.collidepoint(evento.pos):
                    mouse_pressed = True

            if evento.type == pygame.MOUSEBUTTONUP:
                if boton_reintentar.collidepoint(evento.pos) and mouse_pressed:
                    return
                mouse_pressed = False

        pantalla.fill((0, 0, 0))
        imagen_winner = pygame.transform.scale(imagen_winner, (ANCHO_MAXIMO, ALTO_MAXIMO))
        pantalla.blit(imagen_winner, (0, 0))

        texto_movimientos = fuente.render(f"Movimientos: {cantidad_movimientos}", True, (0, 0, 0))
        pantalla.blit(texto_movimientos, (250, 550))

        if boton_reintentar.collidepoint(pygame.mouse.get_pos()):
            pantalla.blit(imagen_boton_hover, boton_reintentar.topleft)
        else:
            pantalla.blit(imagen_boton_normal, boton_reintentar.topleft)

        texto_superficie = fuente.render("Reintentar", True, COLOR_TEXTO)
        texto_rect = texto_superficie.get_rect(center=boton_reintentar.center)
        pantalla.blit(texto_superficie, texto_rect)

        pygame.display.update()

    

def mostrar_menu(pantalla, fondo_menu, boton_iniciar, boton_salir, fuente, imagen_boton_normal, imagen_boton_hover):
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return "salir"

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_iniciar.collidepoint(evento.pos):
                    return
                elif boton_salir.collidepoint(evento.pos):
                    pygame.quit()
                    return "salir"
            
        pantalla.blit(fondo_menu, (0, 0))
        dibujar_boton(pantalla, "Iniciar", boton_iniciar, imagen_boton_normal, imagen_boton_hover, COLOR_TEXTO, fuente)
        dibujar_boton(pantalla, "Salir", boton_salir, imagen_boton_normal, imagen_boton_hover, COLOR_TEXTO, fuente)
        pygame.display.update()

def mostrar_seleccion_niveles(pantalla, botones, fuente, fondo_menu,imagen_boton_normal, imagen_boton_hover):
    if pantalla is None:
        return

    while True:
        pygame.init()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return None

            if evento.type == pygame.MOUSEBUTTONDOWN:
                for nivel, boton in botones.items():
                    if boton.collidepoint(evento.pos):
                        return nivel

        pantalla.blit(fondo_menu, (0, 0))
        for texto, boton in botones.items():
            dibujar_boton(pantalla, texto, boton, imagen_boton_normal, imagen_boton_hover, COLOR_TEXTO, fuente)
        pygame.display.update()

def seleccionar_niveles(pantalla, botones_niveles, fuente, imagen_fondo_menu, imagen_boton_normal, imagen_boton_hover):
    nivel_seleccionado = mostrar_seleccion_niveles(pantalla, botones_niveles, fuente, imagen_fondo_menu, imagen_boton_normal, imagen_boton_hover)
    return nivel_seleccionado

def iniciar_juego(archivo_laberinto):
    global laberinto, inicio, fin, camino_resuelto
    laberinto = cargar_laberinto(archivo_laberinto)
    inicio = encontrar_posicion(laberinto, 'S')
    fin = encontrar_posicion(laberinto, 'E')
    tam_celda = calcular_tamano_celdas(len(laberinto), len(laberinto[0]))

    imagen_pared = pygame.transform.scale(imagen_pared_original, (tam_celda, tam_celda))
    imagen_personaje = pygame.transform.scale(imagen_personaje_original, (tam_celda, tam_celda))
    imagen_camino = pygame.transform.scale(imagen_camino_original, (tam_celda, tam_celda))
    imagen_inicio = pygame.transform.scale(imagen_inicio_original, (tam_celda, tam_celda))
    imagen_objetivo = pygame.transform.scale(imagen_objetivo_original, (tam_celda, tam_celda))
    imagen_opciones = pygame.transform.scale(imagen_panel_opciones, (tam_celda, tam_celda))
    imagen_opciones = pygame.transform.scale(imagen_opciones, (300, 350))
    
    camino_resuelto = False

    botones_metodo = {
        "A*": pygame.Rect(ANCHO_MAXIMO // 2 - 100, ALTO_MAXIMO // 2 - 90, 200, 62),
        "Greedy": pygame.Rect(ANCHO_MAXIMO // 2 - 100, ALTO_MAXIMO // 2 - 30, 200, 62),
        "BFS": pygame.Rect(ANCHO_MAXIMO // 2 - 100, ALTO_MAXIMO // 2 + 30, 200, 62),
        "DFS": pygame.Rect(ANCHO_MAXIMO // 2 - 100, ALTO_MAXIMO // 2 + 90, 200, 62)
    }
    while True:
        if pantalla is None:
            return

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_automatico.collidepoint(evento.pos):
                    if not camino_resuelto:
                        metodo_resolucion = mostrar_seleccion_metodo(pantalla, botones_metodo, fuente, imagen_opciones, imagen_boton_normal, imagen_boton_hover)
                        if metodo_resolucion:
                            camino = resolver_laberinto(laberinto, inicio, fin, pantalla, imagen_pared, tam_celda, True, 0.1, imagen_camino, imagen_inicio, imagen_objetivo, metodo_resolucion)
                            if camino:
                                mostrar_camino(pantalla, laberinto, camino, inicio, fin, imagen_pared, tam_celda, imagen_camino, imagen_inicio, imagen_objetivo)
                                cantidad_movimientos = mover_personaje(pantalla, laberinto, camino, inicio, fin, imagen_pared, imagen_personaje, tam_celda, imagen_camino, imagen_inicio, imagen_objetivo)
                                mostrar_ganador(pantalla, imagen_winner, boton_reintentar, fuente, cantidad_movimientos, imagen_boton_normal, imagen_boton_hover)
                                camino_resuelto = True
                elif boton_manual.collidepoint(evento.pos):
                    if not camino_resuelto:
                        cantidad_movimientos = mover_personaje_manual(pantalla, laberinto, inicio, fin, imagen_pared, imagen_personaje, tam_celda, imagen_camino, imagen_inicio, imagen_objetivo)
                        if cantidad_movimientos > 0:
                            mostrar_ganador(pantalla, imagen_winner, boton_reintentar, fuente, cantidad_movimientos, imagen_boton_normal, imagen_boton_hover)
                            camino_resuelto = True
                elif boton_reintentar.collidepoint(evento.pos):
                    return

        if not camino_resuelto:
            pantalla.fill((0, 0, 0))
            dibujar_laberinto(pantalla, laberinto, imagen_pared, tam_celda, imagen_camino, imagen_inicio, imagen_objetivo)
            dibujar_boton(pantalla, "Automático", boton_automatico, imagen_boton_norma_auto, imagen_boton_hover_auto, COLOR_TEXTO, fuenteAM)
            dibujar_boton(pantalla, "Manual", boton_manual, imagen_boton_norma_auto, imagen_boton_hover_auto, COLOR_TEXTO, fuenteAM)
            pygame.display.update()

def main():
    pygame.init()
    global pantalla,imagen_panel_opciones, fuente, fuenteAM, imagen_pared_original,imagen_objetivo_original, imagen_inicio_original, imagen_personaje_original,imagen_camino_original , imagen_winner,imagen_boton_normal,imagen_boton_hover, imagen_boton_norma_auto,imagen_boton_hover_auto
    global boton_automatico, boton_manual, boton_reintentar, boton_iniciar, boton_salir

    pantalla = pygame.display.set_mode((ANCHO_MAXIMO, ALTO_MAXIMO))
    fuente = pygame.font.Font(None, 30)
    fuenteAM = pygame.font.Font(None, 20)

    imagen_pared_original = pygame.image.load("pared.png").convert_alpha()
    imagen_inicio_original = pygame.image.load("castillo.png").convert_alpha()
    imagen_camino_original = pygame.image.load("camino.png").convert_alpha()
    imagen_objetivo_original = pygame.image.load("objetivo.png").convert_alpha()
    imagen_personaje_original = pygame.image.load("personaje.png").convert_alpha()
    imagen_winner = pygame.image.load("winner.png").convert_alpha()
    imagen_fondo_menu = pygame.image.load("fondo_menu.png").convert()
    imagen_boton_normal = pygame.image.load("imagen_boton.png").convert_alpha()
    imagen_boton_hover = pygame.image.load("imagen_boton_hover.png").convert_alpha()
    imagen_panel_opciones = pygame.image.load("opciones.png").convert_alpha()
    imagen_boton_normal = pygame.transform.scale(imagen_boton_normal, (200, 60))
    imagen_boton_hover = pygame.transform.scale(imagen_boton_hover, (200, 60))

    imagen_boton_norma_auto = pygame.transform.scale(imagen_boton_normal, (150, 25))
    imagen_boton_hover_auto = pygame.transform.scale(imagen_boton_hover, (150, 25))

    imagen_fondo_menu = pygame.transform.scale(imagen_fondo_menu, (ANCHO_MAXIMO, ALTO_MAXIMO))
    boton_automatico = pygame.Rect(10, 10, 150, 25)
    boton_manual = pygame.Rect(150, 10, 150, 25)
    boton_reintentar = pygame.Rect(240, 570, 200, 62)
    boton_iniciar = pygame.Rect(ANCHO_MAXIMO // 2 - 100, ALTO_MAXIMO // 2 - 20, 200, 62)
    boton_salir = pygame.Rect(ANCHO_MAXIMO // 2 - 100, ALTO_MAXIMO // 2 + 40, 200, 62)

    botones_niveles = {
        "Nivel 1": pygame.Rect(ANCHO_MAXIMO // 2 - 100, ALTO_MAXIMO // 2 - 60, 200, 62),
        "Nivel 2": pygame.Rect(ANCHO_MAXIMO // 2 - 100, ALTO_MAXIMO // 2, 200, 62),
        "Nivel 3": pygame.Rect(ANCHO_MAXIMO // 2 - 100, ALTO_MAXIMO // 2 + 60, 200, 62),
        "Nivel 4": pygame.Rect(ANCHO_MAXIMO // 2 - 100, ALTO_MAXIMO // 2 + 120, 200, 62),
        "Nivel 5": pygame.Rect(ANCHO_MAXIMO // 2 - 100, ALTO_MAXIMO // 2 + 180, 200, 62)
    }

    def mostrar_menu_func():
        mostrar_menu(pantalla, imagen_fondo_menu, boton_iniciar, boton_salir, fuente, imagen_boton_normal, imagen_boton_hover)

    def seleccionar_nivel():
        nivel_seleccionado = seleccionar_niveles(pantalla, botones_niveles, fuente, imagen_fondo_menu,imagen_boton_normal, imagen_boton_hover)
        if nivel_seleccionado:
            archivos_niveles = {
                "Nivel 1": 'maze.txt',
                "Nivel 2": 'maze1.txt',
                "Nivel 3": 'maze2.txt',
                "Nivel 4": 'maze3.txt',
                "Nivel 5": 'maze4.txt'
            }
            archivo_laberinto = archivos_niveles.get(nivel_seleccionado)
            if archivo_laberinto:
                iniciar_juego(archivo_laberinto)

    while True:
        mostrar_menu_func()
        seleccionar_nivel()

if __name__ == "__main__":
    main()

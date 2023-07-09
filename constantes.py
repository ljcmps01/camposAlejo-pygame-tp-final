import pygame
FPS = 45

TAM_X_JUGADOR = 20
TAM_Y_JUGADOR = 20
VEL_JUGADOR = 3
SALTO_JUGADOR = 4
RUN_FACTOR = 1.25

ANCHO_VENTANA = 640
ALTO_VENTANA = 480

OFFSET_VENTANA = 64
OFFSET_PISO = 2

Y_PISO_BASE = 234

DIR_OBSTACULOS = "Recursos\\Obstaculos\\"
DIR_SPRITES = "Recursos\\personajes\\"
DIR_DATA = "data\\"

pygame.init()
display = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))

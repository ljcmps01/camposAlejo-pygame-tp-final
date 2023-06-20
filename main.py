import pygame
import sys
from jugador import Player
from constantes import *
import sala

pygame.init()

display = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))

background = pygame.image.load("Recursos\\fondo\palacio_diamante.png")
background = sala.scale_image(background, ALTO_VENTANA, "height")
# bakckground = pygame.image.scale(bakckground,(ANCHO_VENTANA,ALTO_VENTANA))

clock = pygame.time.Clock()

tecnico = Player(0,0)


while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    teclas = pygame.key.get_pressed()
    
    if teclas[ pygame.K_LEFT]:
        tecnico.control("GO_LEFT",display)
    
    if teclas[ pygame.K_RIGHT]:
        tecnico.control("GO_RIGHT",display)

    if teclas[ pygame.K_UP]:
        tecnico.control("JUMP",display)

    if teclas[ pygame.K_DOWN]:
        tecnico.control("GO_DOWN",display)

    display.blit(background,background.get_rect())

    tecnico.update_position(display)
    pygame.display.flip()
    
    clock.tick(60)

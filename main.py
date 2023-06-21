import pygame
import sys
from jugador import Player
from constantes import *
import sala

pygame.init()

display = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))

background = sala.Background("Recursos\\fondo\palacio_diamante.png")
# bakckground = pygame.image.scale(bakckground,(ANCHO_VENTANA,ALTO_VENTANA))

clock = pygame.time.Clock()

tecnico = Player(0,355)


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

    background_surface = pygame.Surface(background.visible_rect.size)
    background_surface.blit(background.background_image, (0,0), background.visible_rect)
    display.blit(background_surface, (0,0))

    if tecnico.x > ANCHO_VENTANA:
        background.shift_background(tecnico.x)
        tecnico.x = 0


    tecnico.update_position(display)
    pygame.display.flip()
    
    clock.tick(60)

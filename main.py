import pygame
import sys
from jugador import Player
from constantes import *
import sala

pygame.init()

display = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))

background = sala.Background("Recursos\\fondo\palacio_diamante_rojo.png")
# bakckground = pygame.image.scale(bakckground,(ANCHO_VENTANA,ALTO_VENTANA))

clock = pygame.time.Clock()

tecnico = Player(0,Y_PISO_BASE)


while True:
    
    clock.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    teclas = pygame.key.get_pressed()
    
    tecnico.x_vel = 0
    if teclas[ pygame.K_LEFT]:
        tecnico.control("GO_LEFT")
    
    if teclas[ pygame.K_RIGHT]:
        tecnico.control("GO_RIGHT")

    # if teclas[ pygame.K_UP]:
    #     tecnico.control("JUMP")

    # if teclas[ pygame.K_DOWN]:
    #     tecnico.control("GO_DOWN")

    display.blit(background.visible_surface, (0,0))

    if tecnico.rect.x > ANCHO_VENTANA or tecnico.rect.x < 0:
        tecnico.rect.x = background.shift_background(tecnico.rect.x)
        
    tecnico.loop(FPS)

    tecnico.draw(display)
    pygame.display.flip()
    

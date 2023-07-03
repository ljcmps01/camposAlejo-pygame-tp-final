import pygame
import sys
from jugador import Player
from constantes import *
import sala

pygame.init()

display = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))

background = sala.Background("Recursos\\fondo\palacio_diamante_rojo_bajobrillo.png")
# bakckground = pygame.image.scale(bakckground,(ANCHO_VENTANA,ALTO_VENTANA))

clock = pygame.time.Clock()

tecnico = Player(0,0)

block_size = 64
# blocks = [sala.Bloque(150,Y_PISO_BASE+block_size, block_size)]
floor = [sala.Bloque(i * block_size,ALTO_VENTANA-block_size, block_size, 2)
         for i in range(-ANCHO_VENTANA // block_size,(ANCHO_VENTANA * 2)//block_size)]
# floor.extend([sala.Bloque(i * block_size,ALTO_VENTANA-block_size*2, block_size, 2)
#          for i in range(-ANCHO_VENTANA // block_size,(ANCHO_VENTANA * 2)//block_size)])
def draw (display, background:sala.Background, jugador:Player, objetos):
    display.blit(background.visible_surface,(0,0))
    for objeto in objetos:
        objeto.draw(display)
    
    jugador.draw(display)

    pygame.display.update()


while True:
    
    clock.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP and tecnico.contador_salto<2:
                tecnico.salto()
            # if (evento.key == pygame.K_RIGHT and tecnico.direccion == "der")\
            # or (evento.key == pygame.K_LEFT and tecnico.direccion == "izq"):
            #     tecnico.contador_correr+=1
    

    tecnico.loop(FPS)

    teclas = pygame.key.get_pressed()
    
    tecnico.x_vel = 0
    if teclas[pygame.K_LEFT]:
        tecnico.control("GO_LEFT")
    
    if teclas[pygame.K_RIGHT]:
        tecnico.control("GO_RIGHT")

    if teclas[pygame.K_LEFT] and teclas[pygame.K_LCTRL]:
        tecnico.control("RUN_LEFT")
    
    if teclas[pygame.K_RIGHT] and teclas[pygame.K_LCTRL]:
        tecnico.control("RUN_RIGHT")

    # if teclas[ pygame.K_UP]:
    #     tecnico.control("JUMP")

    # if teclas[ pygame.K_DOWN]:
    #     tecnico.control("GO_DOWN")
    sala.manejar_colisiones_verticales(tecnico,floor,tecnico.y_vel)

    if tecnico.rect.x+OFFSET_VENTANA > ANCHO_VENTANA or tecnico.rect.x < 0:
        tecnico.rect.x = sala.shift_background(background, tecnico.rect.x)

    display.blit(background.visible_surface, (0,0))

    for bloque in floor:
        bloque.draw(display)
        

    tecnico.draw(display)

    pygame.display.flip()
    

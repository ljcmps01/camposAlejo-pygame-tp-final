import pygame
import sys
from constantes import *
from jugador import Player
import sala

background = sala.Background("Recursos\\fondo\palacio_diamante_rojo_bajobrillo.png")
# bakckground = pygame.image.scale(bakckground,(ANCHO_VENTANA,ALTO_VENTANA))

clock = pygame.time.Clock()

tecnico = Player(0,0)

block_size = 64
blocks = [sala.Bloque(150,Y_PISO_BASE*1.55, block_size, 1)]
floor = [sala.Bloque(i * block_size,ALTO_VENTANA-block_size, block_size, 2)
         for i in range(-ANCHO_VENTANA // block_size,(ANCHO_VENTANA * 2)//block_size)]

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
    

    tecnico.loop(FPS)

    colisiones_izq = sala.colision(tecnico, blocks, (-tecnico.x_vel)-10)
    colisiones_der = sala.colision(tecnico, blocks, tecnico.x_vel+10)

    teclas = pygame.key.get_pressed()
    
    tecnico.x_vel = 0
    if teclas[pygame.K_LEFT] and not colisiones_izq:
        tecnico.control("GO_LEFT")
    
    if teclas[pygame.K_RIGHT] and not colisiones_der:
        tecnico.control("GO_RIGHT")

    if teclas[pygame.K_LEFT] and teclas[pygame.K_LCTRL] and not colisiones_izq:
        tecnico.control("RUN_LEFT")
    
    if teclas[pygame.K_RIGHT] and teclas[pygame.K_LCTRL] and not colisiones_der:
        tecnico.control("RUN_RIGHT")

    sala.manejar_colisiones_verticales(tecnico,floor,tecnico.y_vel)
    sala.manejar_colisiones_verticales(tecnico,blocks,tecnico.y_vel)


    if tecnico.rect.x+OFFSET_VENTANA > ANCHO_VENTANA or tecnico.rect.x < 0:
        tecnico.rect.x = sala.shift_background(background, tecnico.rect.x)

    display.blit(background.visible_surface, (0,0))

    for bloque in floor:
        bloque.draw(display)
        
    for bloque in blocks:
        bloque.draw(display)
        

    tecnico.draw(display)

    pygame.display.flip()
    

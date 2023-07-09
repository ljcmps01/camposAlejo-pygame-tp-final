import pygame
import sys
from constantes import *
from personajes import Personaje
import sala

background = sala.Background("Recursos\\fondo\palacio_diamante_rojo_bajobrillo.png")
# bakckground = pygame.image.scale(bakckground,(ANCHO_VENTANA,ALTO_VENTANA))

clock = pygame.time.Clock()

jugador = Personaje(0,0)

block_size = 64
floor = [sala.Bloque(i * block_size,ALTO_VENTANA-block_size, block_size, 2)
         for i in range(-ANCHO_VENTANA // block_size,(ANCHO_VENTANA * 2)//block_size)]


def draw (display, background:sala.Background, jugador:Personaje, objetos):
    display.blit(background.visible_surface,(0,0))
    for objeto in objetos:
        objeto.draw(display)
    
    jugador.draw(display)

    pygame.display.update()

mapa_bloques = sala.gen_plataformas_from_JSON("escenas.json","facil")

plataformas = mapa_bloques[0]


while True:
    
    clock.tick(FPS)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_UP and jugador.contador_salto<2:
                jugador.salto()
    

    jugador.loop(FPS)

    colisiones_izq = sala.colision(jugador, plataformas, (-jugador.x_vel)-10)
    colisiones_der = sala.colision(jugador, plataformas, jugador.x_vel+10)

    teclas = pygame.key.get_pressed()
    
    jugador.x_vel = 0
    if teclas[pygame.K_LEFT] and not colisiones_izq:
        jugador.control("GO_LEFT")
    
    if teclas[pygame.K_RIGHT] and not colisiones_der:
        jugador.control("GO_RIGHT")

    if teclas[pygame.K_LEFT] and teclas[pygame.K_LCTRL] and not colisiones_izq:
        jugador.control("RUN_LEFT")
    
    if teclas[pygame.K_RIGHT] and teclas[pygame.K_LCTRL] and not colisiones_der:
        jugador.control("RUN_RIGHT")

    sala.manejar_colisiones_verticales(jugador,floor,jugador.y_vel)
    sala.manejar_colisiones_verticales(jugador,plataformas,jugador.y_vel)


    if jugador.rect.x+OFFSET_VENTANA > ANCHO_VENTANA or jugador.rect.x < 0:
        jugador.rect.x,plataformas = sala.mover_escena(background,mapa_bloques, jugador.rect.x)


    display.blit(background.visible_surface, (0,0))

    for bloque in floor:
        bloque.draw(display)
        
    for bloque in plataformas:
        bloque.draw(display)


        

    jugador.draw(display)

    pygame.display.flip()
    

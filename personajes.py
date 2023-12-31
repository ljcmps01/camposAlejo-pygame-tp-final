from typing import Any
import pygame
from constantes import *
from sprites import *
from os import *


def cargar_sprite_sheets(sprite_path, width, height, multidireccion = False):
        offset = 16
        directorio_base = path.join(DIR_SPRITES+sprite_path)
        animaciones = [imagen for imagen in listdir(directorio_base)] 

        dict_sprite = {}

        for imagen in animaciones:
            sprite_sheet= pygame.image.load(path.join(directorio_base,imagen)).convert_alpha()

            lista_sprites = []

            for columna in range(sprite_sheet.get_width()//(width)):
            
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                if columna == 0:
                    rect = pygame.Rect((columna*width), 0, width, height)
                else:
                    rect = pygame.Rect((columna*width), 0, width, height)
                surface.blit(sprite_sheet,(0,0),rect)
                surface=trim_transparent(surface)
                lista_sprites.append(pygame.transform.scale_by(surface,2.5))

            if multidireccion:
                dict_sprite.update({"{0}_{1}".format(imagen.replace(".png",""),'der') : lista_sprites})
                dict_sprite.update({"{0}_{1}".format(imagen.replace(".png",""),'izq') : flip_sprite(lista_sprites)})
            else:
                dict_sprite.update({imagen.replace(".png",""):lista_sprites})

        # del dict_sprite["salto_izq"][-2:]
        # del dict_sprite["salto_der"][-2:]
        # del dict_sprite["caida_der"][-2:]
        # del dict_sprite["caida_izq"][-2:]
        return dict_sprite


def flip_sprite(sprites: list):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


class Jugador(pygame.sprite.Sprite):
    def __init__(self,x,y, vidas):
        self.vida = vidas

class Personaje(pygame.sprite.Sprite):

    COLOR = (255, 0, 0)
    GRAVEDAD = 1
    DELAY_ANIMACION = 10

    def __init__(self, x, y)->None:
        self.SPRITES = cargar_sprite_sheets("tecnico",64,32,True)
        self.rect = pygame.Rect(x, y, TAM_X_JUGADOR, TAM_Y_JUGADOR)
        self.mask = None
        self.x_vel = 0
        self.y_vel = 0
        self.direccion = 'izq'
        self.contador_animacion = 0
        self.contador_caida = 0
        self.contador_salto = 0
        self.correr = False

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direccion != 'izq':
            self.direccion = 'izq'
            self.contador_animacion = 0
    
    def move_right(self, vel):
        self.x_vel = +vel
        if self.direccion != 'der':
            self.direccion = 'der'
            self.contador_animacion = 0

    def salto(self):
        self.y_vel = -self.GRAVEDAD * 8
        self.contador_animacion = 0
        self.contador_salto += 1

        if self.contador_salto == 1:
            self.contador_caida = 0
        

    def loop(self, fps):
        self.y_vel+=min(1,(self.contador_caida / fps) * self.GRAVEDAD)
        self.move(self.x_vel,self.y_vel)

        self.contador_caida += 1
        if self.x_vel == 0:
            self.correr = False
        self.update_sprite()

    def update_sprite(self):
        sprite_sheet = "espera"
        if self.y_vel < 0:
            sprite_sheet = "salto"

        if self.y_vel > self.GRAVEDAD*2:
            sprite_sheet = "caida"

        if self.x_vel != 0 and self.contador_salto==0:
            if self.correr == True:
                sprite_sheet = "correr"
            else:
                sprite_sheet = "caminar"
        
        nombre_sprite_sheet = "{0}_{1}".format(sprite_sheet,self.direccion)
        sprites = self.SPRITES[nombre_sprite_sheet]
        sprite_index = (self.contador_animacion // self.DELAY_ANIMACION) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.contador_animacion+=1
        self.update()
        

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x,self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)
######        
        # self.sprite = self.mask.to_surface()

    def draw(self, display):
        display.blit(self.sprite, (self.rect.x,self.rect.y))

    def control(self, accion:str):
        """Movimientos basicos del jugador
        GO_LEFT = desplazamiento izquierda
        GO_RIGHT = desplazamiento derecha
        JUMP = desplazamiento arriba
        GO_DOWN = desplazamiento abajo

        Args:
            accion (str): movimiento a realizar
            display (pygame.display): pantalla sobre la cual realizar el movimiento
        """
        match accion:
            case "GO_LEFT":
                self.move_left(VEL_JUGADOR)
                self.correr = False
            case "GO_RIGHT":
                self.move_right(VEL_JUGADOR)
                self.correr = False
            case "RUN_LEFT":
                self.move_left(VEL_JUGADOR*RUN_FACTOR)
                self.correr = True
            case "RUN_RIGHT":
                self.move_right(VEL_JUGADOR*RUN_FACTOR)
                self.correr = True
            case _:
                pass
        # print("pos: {0},{1}".format(self.rect.x,self.rect.y))
        # print("speed: {0}".format(self.correr))

    def aterrizar(self):
        self.contador_caida = 0
        self.y_vel = 0
        self.contador_salto = 0
    
    def choque_cabeza(self):
        self.count = 0
        self.y_vel *= -1




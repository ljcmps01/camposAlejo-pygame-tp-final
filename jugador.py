import pygame
from constantes import *

def cargar_sprite_sheets(sprite_path,width,height, multidireccion = False):
        sprite_sheet= pygame.image.load(sprite_path)

        lista_acciones = ['espera','caminar','correr','salto','caida']

        dict_sprite = {}

        for fila in range((sprite_sheet.get_height()//height)):
            
            lista_sprites = []
            # dict_sprite.update(lista_acciones[fila])

            for columna in range(sprite_sheet.get_width()//width):
            
                surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect = pygame.Rect(columna*width, fila*height, width, height)
                surface.blit(sprite_sheet,(0,0),rect)
                lista_sprites.append(pygame.transform.scale_by(surface,2.5))

            if multidireccion:
                dict_sprite.update({"{0}_{1}".format(lista_acciones[fila],'der') : lista_sprites})
                dict_sprite.update({"{0}_{1}".format(lista_acciones[fila],'izq') : flip_sprite(lista_sprites)})
            else:
                dict_sprite.update({lista_acciones[fila]:lista_sprites})

        return dict_sprite


def flip_sprite(sprites: list):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


class Player(pygame.sprite.Sprite):

    COLOR = (255, 0, 0)
    GRAVEDAD = 1
    SPRITES = cargar_sprite_sheets("Recursos\\personajes\\tecnico.png",64,64,True)
    DELAY_ANIMACION = 10

    def __init__(self, x, y)->None:
        self.rect = pygame.Rect(x, y, TAM_X_JUGADOR, TAM_Y_JUGADOR)
        self.x_vel = 0
        self.y_vel = 0
        self.direccion = 'izq'
        self.animation_count = 0
        self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direccion != 'izq':
            self.direccion = 'izq'
            self.animation_count = 0
    
    def move_right(self, vel):
        self.x_vel = +vel
        if self.direccion != 'der':
            self.direccion = 'der'
            self.animation_count = 0

    def loop(self, fps):
        # self.y_vel+=min(1,(self.fall_count / fps) * self.GRAVEDAD)
        self.move(self.x_vel,self.y_vel)

        self.fall_count += 1
        self.update_sprite()

    def update_sprite(self):
        sprite_sheet = "espera"
        if self.x_vel != 0:
            sprite_sheet = "correr"
        
        nombre_sprite_sheet = "{0}_{1}".format(sprite_sheet,self.direccion)
        sprites = self.SPRITES[nombre_sprite_sheet]
        sprite_index = (self.animation_count // self.DELAY_ANIMACION) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count+=1

    def draw(self, display):
        # self.sprite = self.SPRITES["{0}_{1}".format('espera',self.direccion)][0]
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
            case "GO_RIGHT":
                self.move_right(VEL_JUGADOR)
            case "JUMP":
                self.rect.y -= self.speed
                if self.rect.y < 0:
                    self.rect.y = 0
            case "GO_DOWN":
                self.rect.y += self.speed
                if self.rect.y > Y_PISO_BASE:
                    self.rect.y = Y_PISO_BASE
            case _:
                pass
        print("pos: {0},{1}".format(self.rect.x,self.rect.y))




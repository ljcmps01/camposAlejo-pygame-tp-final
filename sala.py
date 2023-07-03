import pygame
from jugador import Player
from constantes import *

class Background():
    def __init__(self, image_path):
        self.background_image = pygame.image.load(image_path)
        self.background_image = scale_image(self.background_image, ALTO_VENTANA, 'height')
        self.width, self.height = self.background_image.get_size()
        self.n_surfaces = int(self.width / ANCHO_VENTANA)-1
        self.index_visible = 0 
        self.lista_rectangulos_visibles = self.split_background()
        self.visible_rect = pygame.Rect(0, 0, ANCHO_VENTANA, ALTO_VENTANA)
        self.visible_surface =self.lista_rectangulos_visibles[0]
        self.max_reached = False

    def split_background(self):
        lista_rect = []
        for x in range(0, self.n_surfaces):
            sub_rect = pygame.Rect(x*ANCHO_VENTANA, 0, ANCHO_VENTANA, ALTO_VENTANA)
            sub_surface = self.background_image.subsurface(sub_rect)
            lista_rect.append(sub_surface)

        return lista_rect
        

def shift_background(background, player_x):

    new_player_x = 0
    if player_x+OFFSET_VENTANA > ANCHO_VENTANA:
        background.index_visible += 1
    else:
        background.index_visible -= 1
        new_player_x = ANCHO_VENTANA-OFFSET_VENTANA
    
    background.index_visible = background.index_visible % (background.n_surfaces) 

    
    background.visible_surface = background.lista_rectangulos_visibles[background.index_visible]
    
    return new_player_x
        
class Objeto(pygame.sprite.Sprite):
    def __init__(self,x,y,width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x,y,width,height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, display):
        display.blit(self.image, (self.rect.x,self.rect.y))

class Bloque(Objeto):
    def __init__(self,x,y,size,escala):
        super().__init__(x,y,size,size)
        block = load_block(size,escala)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)

def load_block(size,escala=1):
    path = DIR_OBSTACULOS + "plataforma3.png"
    image = pygame.image.load(path)
    surface = pygame.Surface((size,size),pygame.SRCALPHA,32)
    rect = pygame.Rect(0,0,size,size)
    surface.blit(image, (0,0),rect)

    return pygame.transform.scale_by(surface,escala)


def scale_image(image, target_axis_size, axis='width'):
    # Determine the current dimensions of the image
    image_width, image_height = image.get_size()

    if axis == 'width':
        # Calculate the new height based on the target width
        scale_factor = target_axis_size / image_width
        new_width = target_axis_size
        new_height = int(image_height * scale_factor)
    elif axis == 'height':
        # Calculate the new width based on the target height
        scale_factor = target_axis_size / image_height
        new_height = target_axis_size
        new_width = int(image_width * scale_factor)
    else:
        raise ValueError("Invalid axis specified. Valid options are 'width' or 'height'.")

    # Scale the image using the calculated dimensions
    scaled_image = pygame.transform.scale(image, (new_width, new_height))

    return scaled_image

def manejar_colisiones_verticales(jugador:Player, objetos:list, dy:int):
    objetos_colisionados = []
    for objeto in objetos:
        if pygame.sprite.collide_mask(jugador, objeto):
            if dy > 0:
                jugador.rect.bottom = objeto.rect.centery+10
                jugador.aterrizar()

            elif dy < 0:
                jugador.rect.top = objeto.rect.bottom
                jugador.choque_cabeza()

        objetos_colisionados.append(objeto)

    return objetos_colisionados
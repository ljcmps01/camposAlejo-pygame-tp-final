import pygame
from jugador import Player
from constantes import *
from sprites import *
import json

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
        

def mover_escena(background,plataformas, player_x):

    new_player_x = 0
    if player_x+OFFSET_VENTANA > ANCHO_VENTANA:
        background.index_visible += 1
    else:
        background.index_visible -= 1
        new_player_x = ANCHO_VENTANA-OFFSET_VENTANA
    
    background.index_visible = background.index_visible % (background.n_surfaces)     
    background.visible_surface = background.lista_rectangulos_visibles[background.index_visible]
    
    return new_player_x,plataformas[background.index_visible] 
        
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
    def __init__(self,x,y,size,escala=1):
        super().__init__(x,y,size,size)
        block = load_block(size,escala)
        self.image.blit(block, (0,0))
        self.mask = pygame.mask.from_surface(self.image)
        # self.image.blit(self.mask.to_surface(), (0,0))

def gen_plataformas_from_JSON(nombre_archivo:str, nivel: str):
    lista_plataformas = []
    with open(DIR_DATA+nombre_archivo) as archivo:
        lista_escenas = json.load(archivo)[nivel]
    
    for escena in lista_escenas:
        lista_x = escena["x"]
        lista_y = escena["y"]
        tam = escena["block_size"]

        lista_plataformas.append(generar_plataformas(lista_x, lista_y,tam))

    return lista_plataformas

def generar_plataformas(coordenadas_x: list, coordenadas_y: list,size_block: int):
    lista_bloques = list()
    max_grid_x = ANCHO_VENTANA//size_block 
    max_grid_y = (ALTO_VENTANA//size_block)-OFFSET_PISO
    if len(coordenadas_x) == len(coordenadas_y):
        for i in range(len(coordenadas_x)):
            x = coordenadas_x[i]*size_block
            y = (max_grid_y-coordenadas_y[i]-OFFSET_PISO)*size_block

            if coordenadas_x[i] < max_grid_x and coordenadas_y[i] < max_grid_y:
                new_bloque = Bloque(x,y,size_block)
                lista_bloques.append(new_bloque)
            else:
                print("coordenadas ({0},{1}) fuera de rango".format(x,y))
        pass
    else:
        print("las listas de coordenadas x e y deben tener la misma cantidad de elementos")

    return lista_bloques

def load_block(size,escala=1):
    path = DIR_OBSTACULOS + "plataforma3.png"
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size,size),pygame.SRCALPHA,32)
    # surface = trim_transparent(surface)
    # surface.fill("red")
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
                jugador.rect.bottom = objeto.rect.top
                jugador.aterrizar()

            elif dy < 0:
                jugador.rect.top = objeto.rect.bottom
                jugador.choque_cabeza()

        objetos_colisionados.append(objeto)

    return objetos_colisionados

def colision(jugador:Player, objetos:list, dx:int):
    jugador.move(dx, 0)
    jugador.update()

    objeto_colisionado = None

    for objeto in objetos:
        if pygame.sprite.collide_mask(jugador,objeto):
            objeto_colisionado = objeto
            break

    jugador.move(-dx, 0)
    jugador.update()

    # print (dx)
    return objeto_colisionado

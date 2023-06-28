import pygame
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
        

    def shift_background(self, player_x):

        new_player_x = 0
        if player_x > ANCHO_VENTANA:
            self.index_visible += 1
        else:
            self.index_visible -= 1
            new_player_x = ANCHO_VENTANA
        
        self.index_visible = self.index_visible % (self.n_surfaces) 

        
        self.visible_surface = self.lista_rectangulos_visibles[self.index_visible]
        
        return new_player_x
        
        

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

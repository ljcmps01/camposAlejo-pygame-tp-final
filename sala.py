import pygame
from constantes import *

class Background():
    def __init__(self, image_path):
        self.background_image = pygame.image.load(image_path)
        self.background_image = scale_image(self.background_image, ALTO_VENTANA, 'height')
        self.width, self.height = self.background_image.get_size()
        self.visible_rect = pygame.Rect(0, 0, ANCHO_VENTANA, ALTO_VENTANA)
        self.visible_surface = pygame.Surface(self.visible_rect.size)
        self.max_reached = False

    def shift_background(self, player_x):
        
        if (self.visible_rect.left + ANCHO_VENTANA*2) > self.width:
            self.max_reached = True

        if self.max_reached:
            self.visible_rect.left = 0
            self.max_reached = False
        else:
            self.visible_rect.left += player_x


        
        self.visible_surface = pygame.Surface(self.visible_rect.size)
            
        
        

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

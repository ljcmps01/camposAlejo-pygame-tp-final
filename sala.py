import pygame
from constantes import *

class Background():
    def __init__(self, image_path, display_height):
        self.background_image = pygame.image.load(image_path)
        self.background_image = scale_image(self.background_image, display_height)
        self.height, self.width = self.background_image.get.size()
        self.x_position = 0

    
        

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

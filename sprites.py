import pygame

def trim_transparent(rect_surface):
    # Get the color of fully transparent pixels
    transparent_color = rect_surface.get_colorkey()

    # Find the non-transparent region
    left, top, width, height = rect_surface.get_rect()
    right = left + width - 1
    bottom = top + height - 1

    # Trim transparent rows from the top
    while top < bottom and all(rect_surface.get_at((x, top)) == transparent_color for x in range(left, right + 1)):
        top += 1

    # Trim transparent rows from the bottom
    while bottom >= top and all(rect_surface.get_at((x, bottom)) == transparent_color for x in range(left, right + 1)):
        bottom -= 1

    # Trim transparent columns from the left
    while left < right and all(rect_surface.get_at((left, y)) == transparent_color for y in range(top, bottom + 1)):
        left += 1

    # Trim transparent columns from the right
    while right >= left and all(rect_surface.get_at((right, y)) == transparent_color for y in range(top, bottom + 1)):
        right -= 1

    # Create a new surface with the trimmed area
    trimmed_rect_surface = rect_surface.subsurface(pygame.Rect(left, top, right - left + 1, bottom - top + 1))

    return trimmed_rect_surface
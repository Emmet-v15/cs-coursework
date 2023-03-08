import pygame
import pygame.gfxdraw
import numpy as np
from numpy import pi, sqrt, cos, sin, arctan2 as atan2

def aaPolygon(surface, points, color):
    """
    Draw antialiased polygon using supersampling.
    """
    scale = 1.75
    # Calculate minimum x and y values.
    x_coords = tuple(x for x, _ in points)
    x_min, x_max = min(x_coords), max(x_coords)
    y_coords = tuple(y for _, y in points)
    y_min, y_max = min(y_coords), max(y_coords)
    # Calculate width and height of target area.
    w = x_max - x_min + 1
    h = y_max - y_min + 1
    # Create scaled surface with properties of target surface.
    s = pygame.Surface((w * scale, h * scale), 0, surface)
    s_points = [((x - x_min) * scale, (y - y_min) * scale)
                for x, y in points]
    pygame.draw.polygon(s, color, s_points)
    # Scale down surface to target size for supersampling effect.
    s2 = pygame.transform.smoothscale(s, (w, h))
    # Paint smooth polygon on target surface.
    surface.blit(s2, (x_min, y_min))
    

def rectRotated(surface, rect, rotation, color):
    """
    Draws a rotated Rect.
    surface: pygame.Surface
    rect: pygame.Rect
    color: pygame.Color
    rotation: float (degrees)
    return: np.ndarray (vertices)
    """
    # calculate the rotation in radians
    rot_radians = -rotation * pi / 180

    # calculate the points around the center of the rectangle, taking width and height into account
    radius = sqrt((rect.width / 2) ** 2 + (rect.height / 2) ** 2)
    angle = atan2(rect.height / 2, rect.width / 2)
    angles = [angle, -angle + pi, angle + pi, -angle]

    # create a numpy array of the points, with axes rounded so that the points are on the pixel grid
    points = np.array([
        [
            round(rect.centerx + radius * cos(a + rot_radians)), 
            round(rect.centery + radius * sin(a + rot_radians))
        ] for a in angles
    ])
    
    # draw the polygon, using the antialiased polygon function
    aaPolygon(surface, points, color)
    # return the vertices of the rectangle
    return points

def tRectRotated(surface, texture, rotation, topleft):

    # calculate the rotation in radians
    rot_radians = -rotation * pi / 180
    
    rect = texture.get_rect(topleft=topleft)

    # calculate the points around the center of the rectangle, taking width and height into account
    radius = sqrt((rect.width / 2) ** 2 + (rect.height / 2) ** 2)
    angle = atan2(rect.height / 2, rect.width / 2)
    angles = [angle, -angle + pi, angle + pi, -angle]

    # create a numpy array of the points, with axes rounded so that the points are on the pixel grid
    points = np.array([
        [
            round(rect.centerx + radius * cos(a + rot_radians)), 
            round(rect.centery + radius * sin(a + rot_radians))
        ] for a in angles
    ])

    rotated_image = pygame.transform.rotate(texture, rotation)
    new_rect = rotated_image.get_rect(center = texture.get_rect(topleft=topleft).center)

    surface.blit(rotated_image, new_rect)
    return points


    


if __name__ == "__main__":
    # demonsrate the functions in action
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    texture = pygame.image.load("resources/stage_1.png").convert_alpha()
    rect = pygame.Rect(0, 0, 800, 600)
    angle = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((0, 0, 0))
        tRectRotated(screen, texture, angle, (100, 100))
        angle += 1
        pygame.display.update()
        clock.tick(60)

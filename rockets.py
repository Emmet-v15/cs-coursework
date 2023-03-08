import pygame
from pygame.locals import *
import numpy as np
from numpy import pi, sqrt, cos, sin, arctan2 as atan2
import drawinglib as dl

class BaseRocket():
    def __init__(self, rect, color, startPos, speed = 1):
        self.rect = rect
        self.color = color
        
        # to store movement
        self.speed = speed
        self.rotation = 0 # degrees
        self.pos = np.array(startPos, dtype=np.float64)
        
        # to store momentum
        self.vel = np.array([0, 0], dtype=np.float64) # velocity
        self.angularVelocity = 0 # angular momentum in degrees
        
        self.dt = 0 # time since last update
        self.texture = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        self.texture.fill(self.color)
        
    def update(self, dt):
        self.dt = dt # update dt
        keys = pygame.key.get_pressed() # get pressed keys
        
        # update position
        self.pos += self.vel * self.dt / 500
        self.rotation += self.angularVelocity * self.dt / 500 # update rotation

        # use a dictionary to map keys to functions
        keymap = {
            K_a: lambda: self.rotate(20),
            K_d: lambda: self.rotate(-20),
            K_w: lambda: self.applyThrust(),
        }

        # check if key is pressed and call function
        for key in keymap:
            if keys[key]:
                keymap[key]()

    def applyThrust(self, percentage=100):
        # caluclate direction vector
        theta = np.deg2rad(-self.rotation + 90)
        direction = np.dot(np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]]), np.array([-1, 0]))
        # move the rocket in the correct direction
        self.vel += direction * self.speed * percentage * (self.dt / 500)
        
    def rotate(self, angle):
        self.angularVelocity += angle * self.dt / 500 # rotate rocket
    
    def draw(self, surface):
        self.rotation %= 360
        dl.tRectRotated(surface, self.texture, self.rotation, self.pos)

        
    def drawDebug(self, surface):
        middle = self.pos + np.array([self.rect.width / 2, self.rect.height / 2])
        startRot = int(-self.rotation - 90) # start rotation for arc
        endRot = int(startRot - self.angularVelocity) # end rotation for arc
        
        # draw velocity vector logaritmicly
        pygame.draw.line(surface, (255, 0, 0), middle, middle + np.log10(np.linalg.norm(self.vel) + 1) * self.vel, 2)
        # draw direction vector
        pygame.draw.line(surface, (0, 255, 0), middle, middle - np.array([cos(np.deg2rad(-self.rotation + 90)), sin(np.deg2rad(-self.rotation + 90))]) * 100, 2)
        # draw angular velocity arc
        pygame.gfxdraw.arc(surface, int(middle[0]), int(middle[1]), 101, np.min([startRot, endRot]), np.max([startRot, endRot]), (255, 0, 0))
        pygame.gfxdraw.arc(surface, int(middle[0]), int(middle[1]), 100, np.min([startRot, endRot]), np.max([startRot, endRot]), (255, 0, 0))
        pygame.gfxdraw.arc(surface, int(middle[0]), int(middle[1]), 99, np.min([startRot, endRot]), np.max([startRot, endRot]), (255, 0, 0))


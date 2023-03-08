import pygame
import sys
import os
import json

abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)


class ScalableRect:
    def __init__(self, x=0, y=0, w=0, h=0):
        self.rect = pygame.Rect(x, y, w, h)
        # load scale from config.json
        with open(dname + "\config.json", "r") as f:
            self.scale = json.load(f)["gameScale"]

    def get_rect(self):
        return pygame.Rect(
            self.rect[0] * self.scale,
            self.rect[1] * self.scale,
            self.rect[2] * self.scale,
            self.rect[3] * self.scale,
        )


class BaseWindow:
    def __init__(self, width, height, drawFps=False):
        """
        Creates a window with the given width and height, used to display graphics.
        width: width of window
        height: height of window
        """
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode(
            (self.width, self.height)
        )  # create window with given width and height
        self.dt = 0  # delta time, time between frames
        self.running = True
        self.font = pygame.font.SysFont("Arial", 20)  # font used to draw text
        self.fps = 0  # frames per second
        self.clock = pygame.time.Clock()  # clock used to check fps
        self.timers = {"fpsUpdate": 0}  # timers used to time events
        self.drawFps = drawFps
        self.fps_text = self.font.render(
            f"FPS: {self.fps:.0f}", True, (255, 255, 255)
        )  # create text

        # enable anti-aliasing using GL_MULTISAMPLEBUFFERS and GL_MULTISAMPLESAMPLES
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLEBUFFERS, 1)
        pygame.display.gl_set_attribute(pygame.GL_MULTISAMPLESAMPLES, 3)
        # enable alpha blending
        pygame.display.gl_set_attribute(pygame.GL_ALPHA_SIZE, 8)
        # enable depth testing
        pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 16)
        # enable double buffering
        pygame.display.gl_set_attribute(pygame.GL_DOUBLEBUFFER, 1)

    def run(self):
        """
        Runs the game loop.
        """
        while self.running:
            start_time = pygame.time.get_ticks()  # start time of frame, used for dt

            self.events()  # handle events
            self.update()  # update game logic
            self.draw()  # draw to screen

            self.fps = self.clock.get_fps()  # update fps
            self.clock.tick()  # update clock
            self.dt = pygame.time.get_ticks() - start_time  # calculate dt

    def events(self):
        """
        Handles events.
        """
        for event in pygame.event.get():  # handle events
            if event.type == pygame.QUIT:
                self.running = False  # stop game loop
                pygame.quit()
                sys.exit()

    def update(self):
        """
        Updates game logic.
        """
        for timer in self.timers:
            self.timers[timer] += self.dt

    def draw(self):
        """
        Draws to screen.
        """

        if self.drawFps:
            if self.timers["fpsUpdate"] >= 1000:
                self.timers["fpsUpdate"] = 0
                self.fps_text = self.font.render(
                    f"FPS: {self.fps:.0f}", True, (255, 255, 255)
                )  # create text

            self.screen.blit(self.fps_text, (0, 0))  # draw text

        pygame.display.update()  # update screen


class Interval:
    def __init__(self, interval):
        self.interval = interval
        self.time = 0

    def update(self, dt):
        self.time += dt

    def check(self):
        if self.time >= self.interval:
            self.time = 0
            return True
        return False

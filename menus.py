import pygame
from pygame.locals import *
import numpy as np


class Colors:
    def __init__(self, idle, hover, press):
        """
        Used to store colors for each state of the button
        idle: tuple
        hover: tuple
        press: tuple
        """
        self.idle = idle
        self.hover = hover
        self.press = press


class ColoredText:
    def __init__(self, text, size, colors):
        """
        Used to render text with different colors for each state of the button
        text: str
        size: int
        colors: Colors
        """
        self.fontRenderer = pygame.font.Font("assets/fonts/Roboto-Regular.ttf", size)
        self.idle = self.fontRenderer.render(text, True, colors.idle)
        self.hover = self.fontRenderer.render(text, True, colors.hover)
        self.press = self.fontRenderer.render(text, True, colors.press)


class MainMenu:
    def __init__(self, rect, gameStateCallback):

        fontColors = Colors((255, 255, 255), (255, 255, 255), (0, 0, 0))
        # idle, hover, press colors for buttons
        greenButtonColors = Colors((50, 200, 50), (0, 200, 0), (100, 200, 100))
        grayButtonColors = Colors((100, 100, 100), (50, 50, 50), (150, 150, 150))
        redButtonColors = Colors((200, 50, 50), (200, 0, 0), (200, 100, 100))

        # create stars
        self.stars = StarryBackground(rect)

        # create buttons in the constructor and not in the draw function to avoid recreating them every frame
        self.buttons = []
        self.buttons.append(
            Button(
                pygame.Rect(0, 60, 200, 80),
                greenButtonColors,
                ColoredText("Play", 30, fontColors),
                lambda: gameStateCallback("play"),
            ),
        )
        self.buttons.append(
            Button(
                pygame.Rect(0, 200, 200, 80),
                grayButtonColors,
                ColoredText("Help", 30, fontColors),
                lambda: gameStateCallback("help"),
            ),
        )
        self.buttons.append(
            Button(
                pygame.Rect(0, 340, 200, 80),
                grayButtonColors,
                ColoredText("Options", 30, fontColors),
                lambda: gameStateCallback("options"),
            ),
        )
        self.buttons.append(
            Button(
                pygame.Rect(0, 480, 200, 80),
                grayButtonColors,
                ColoredText("Credits", 30, fontColors),
                lambda: gameStateCallback("credits"),
            ),
        )
        self.buttons.append(
            Button(
                pygame.Rect(rect.width - 200, 480, 200, 80),
                redButtonColors,
                ColoredText("Quit", 30, fontColors),
                lambda: gameStateCallback("quit"),
            ),
        )

    def draw(self, screen):

        # draw stars
        self.stars.draw(screen)

        # draw buttons
        for button in self.buttons:
            button.draw(screen)


class StarryBackground:
    def __init__(self, rect):
        self.starsLayered = [[], [], []]
        self.vec = np.array([0, 0], dtype=np.float32)
        self.laggedVec = np.array([0, 0], dtype=np.float32)

        # create stars for different layers of the background
        for i in range(100):
            self.starsLayered[0].append(
                [
                    np.random.randint(0, rect.width),
                    np.random.randint(0, rect.height),
                    (255, 255, 255),
                ],
            )

        for i in range(50):
            self.starsLayered[1].append(
                [
                    np.random.randint(0, rect.width),
                    np.random.randint(0, rect.height),
                    (255, 100, 100),
                ],
            )

        for i in range(25):
            self.starsLayered[2].append(
                [
                    np.random.randint(0, rect.width),
                    np.random.randint(0, rect.height),
                    (200, 200, 255),
                ],
            )

    def draw(self, screen):

        # calculate vec by mouse position
        self.vec = np.array(
            [
                pygame.mouse.get_pos()[0] - screen.get_width() / 2,
                pygame.mouse.get_pos()[1] - screen.get_height() / 2,
            ],
            dtype=np.float32,
        )

        # calculate lagged vec by tweening towards vec
        self.laggedVec += (self.vec - self.laggedVec) * 0.0001

        # normalize and scale
        drawVec = self.laggedVec
        drawVec /= np.linalg.norm(self.laggedVec)
        drawVec *= 0.5

        for star in self.starsLayered[0]:
            pygame.draw.circle(screen, (255, 255, 255), star[:2], 1)
            star[0] += drawVec[0] * 0.5
            star[1] += drawVec[1] * 0.5

            # wrap stars around the screen
            if star[0] < 0:
                star[0] = screen.get_width()
            if star[1] < 0:
                star[1] = screen.get_height()
            if star[0] > screen.get_width():
                star[0] = 0
            if star[1] > screen.get_height():
                star[1] = 0

        for star in self.starsLayered[1]:
            pygame.draw.circle(screen, (255, 255, 255), star[:2], 1)
            star[0] += drawVec[0] * 1.2
            star[1] += drawVec[1] * 1.2
            if star[0] < 0:
                star[0] = screen.get_width()
            if star[1] < 0:
                star[1] = screen.get_height()
            if star[0] > screen.get_width():
                star[0] = 0
            if star[1] > screen.get_height():
                star[1] = 0

        for star in self.starsLayered[2]:
            pygame.draw.circle(screen, (255, 255, 255), star[:2], 1)
            star[0] += drawVec[0] * 2
            star[1] += drawVec[1] * 2
            if star[0] < 0:
                star[0] = screen.get_width()
            if star[1] < 0:
                star[1] = screen.get_height()
            if star[0] > screen.get_width():
                star[0] = 0
            if star[1] > screen.get_height():
                star[1] = 0


class Button:
    def __init__(self, rect, colors, text, callback):
        """
        rect: pygame.Rect
        colors: Colors
        text: ColoredText
        callback: function
        """

        self.rect = rect
        self.text = text
        self.colors = colors
        self.callback = callback
        self.isPressed = False
        self.isHover = False
        self.debounce = False

    def draw(self, surface):

        # check if button is pressed
        if pygame.Rect(*self.rect).collidepoint(pygame.mouse.get_pos()):
            self.isHover = True
            if pygame.mouse.get_pressed()[0]:
                self.isPressed = True
            else:
                self.isPressed = False
        else:
            self.isHover = False

        if self.isHover and self.isPressed:
            pygame.draw.rect(surface, self.colors.press, self.rect)
            surface.blit(
                self.text.press,
                (
                    self.rect[0] + self.rect[2] / 2 - self.text.idle.get_width() / 2,
                    self.rect[1] + self.rect[3] / 2 - self.text.idle.get_height() / 2,
                ),
            )
            if not self.debounce:
                self.callback()
            self.debounce = True
        elif self.isHover:
            pygame.draw.rect(
                surface, self.colors.hover, pygame.Rect(*self.rect).inflate(10, 10)
            )
            surface.blit(
                self.text.hover,
                (
                    self.rect[0] + self.rect[2] / 2 - self.text.idle.get_width() / 2,
                    self.rect[1] + self.rect[3] / 2 - self.text.idle.get_height() / 2,
                ),
            )
            self.debounce = False
        else:
            pygame.draw.rect(surface, self.colors.idle, self.rect)
            surface.blit(
                self.text.idle,
                (
                    self.rect[0] + self.rect[2] / 2 - self.text.idle.get_width() / 2,
                    self.rect[1] + self.rect[3] / 2 - self.text.idle.get_height() / 2,
                ),
            )
            self.debounce = False

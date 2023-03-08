import pygame, sys
import pygame.gfxdraw
from numpy import pi, sqrt, cos, sin, arctan2 as atan2
from pygame.locals import *

from engine import BaseWindow, ScalableRect
from rockets import BaseRocket
from menus import MainMenu
import drawinglib as dl

pygame.init()


class Game(BaseWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rocket = BaseRocket(
            pygame.Rect(400 - 25, 400, 50, 90), (255, 255, 255), (400, 400), 1
        )
        self.mainMenu = MainMenu(self.screen.get_rect(), self.setGameState)
        self.state = "menu"

    def update(self):

        # using python version of switch case statement
        match self.state:
            case "menu":
                # self.mainMenu.update(self.dt)  # updating menu is not required
                pass
            case "play":

                pass
            case "help":
                pass
            case "options":
                pass
            case "credits":
                pass
            case "quit":
                sys.exit()
            case "launch":
                self.rocket.update(self.dt)  # update rocket

        super().update()  # update parent class stuff

    def draw(self):
        self.screen.fill((0, 0, 0))  # clear screen

        match self.state:
            case "menu":
                self.mainMenu.draw(self.screen)  # draw menu
            case "play":
                pass
            case "help":
                pass
            case "options":
                pass
            case "credits":
                pass
            case "quit":
                sys.exit()
            case "launch":
                self.rocket.draw(self.screen)
                # self.rocket.drawDebug(self.screen)

        super().draw()  # draw parent class stuff

    def setGameState(self, state):
        self.state = state


if __name__ == "__main__":
    game = Game(800, 600, drawFps=True)
    game.run()

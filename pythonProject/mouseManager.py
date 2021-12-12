import pygame


class MouseManager():
    def __init__(self, game):
        self.game = game

        self.mousePressed = False

    def mouseTrack(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.game.mousePressed()


        elif event.type == pygame.MOUSEBUTTONUP:
            self.mousePressed = False

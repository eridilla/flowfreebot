import copy

import pygame
import sys

import checker
import draw
import menu
import mouseManager
import algorithm


class Game:
    def __init__(self):
        self.dev = True
        self.testingMode = False
        pygame.init()
        menu.Menu(self)
        print("menu initialised")
        self.startGame = True

    def initialise(self):
        self.points = []

        self.mouseManager = mouseManager.MouseManager(self)
        self.graphicsManager = draw.GraphicsManager(self)

        self.loadLevel(self.level)
        self.selectedColour = [0, 0, 0]

        self.startGame = True

    def loadLevel(self, level):
        screen = pygame.display
        screen.set_caption("Flow")
        self.screen = screen.set_mode(level.screenSize)

        self.reloadBoard()

        if self.dev:
            print("Level loaded")
            print("Rectangles:", self.level.rectangles)
            print("Statics:", self.level.statics)
            print("Centre points:", self.level.centrePoints)

    def removeTile(self, tile):
        for array in self.level.statics:
            if array[0] == tile:
                return

        newPoints = copy.copy(self.points)

        for i, point in enumerate(self.points):
            index = newPoints.index(point)
            if point[0] == tile:
                del newPoints[index]
                self.points = newPoints

        self.reloadBoard()

    def reloadBoard(self):
        # self.buttons = self.graphicsManager.drawBoard(self.level)
        self.graphicsManager.drawBoard(self.level)

        for static in self.level.statics:
            tile, colour = static
            self.graphicsManager.drawEndStatics(tile, colour)

        for array in self.points:
            self.graphicsManager.drawEndPoint(array[0], array[1])

        if checker.checkWin(self.level.statics, self.level.rectangles, self.points):
            self.graphicsManager.drawWinScreen()

        pygame.display.update()

    def addPoint(self, tile, colour):
        self.points.append((tile, colour))
        self.reloadBoard()

    def mousePressed(self):
        pos = pygame.mouse.get_pos()
        algorithms = algorithm.Algorithms(self, self.level)

        if self.graphicsManager.rectangles[0].collidepoint(pos):
            algorithms.dfs()

        if self.graphicsManager.rectangles[1].collidepoint(pos):
            algorithms.backtrack()

        if self.graphicsManager.rectangles[3].collidepoint(pos):
            print("\nReloading game\n")
            self.points = []
            self.reloadBoard()
            return

        if self.graphicsManager.rectangles[4].collidepoint(pos):
            game.__init__()

        for i, value in enumerate(self.level.rectangles):
            if value.collidepoint(pos):
                self.lastSelectedTile = i

                for array in self.level.statics:
                    if array[0] == i:
                        self.mouseManager.mousePressed = True
                        if self.dev: print("Mouse pressed on a static tile")

                        self.selectedColour = array[1]
                        if self.dev: print("Selected colour:", self.selectedColour)

                        return

                for array in self.points:
                    if array[0] == i:
                        self.removeTile(i)
                        return

                if self.selectedColour != [0, 0, 0]:
                    self.addPoint(i, self.selectedColour)
                    return


if __name__ == "__main__":
    game = Game()

    while True:
        while game.startGame:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if game.dev: print("Exiting..")
                    sys.exit()

                game.mouseManager.mouseTrack(event)

            pygame.display.flip()

import copy
import json
import math
import pygame
import sys

import checker
import draw
import levels
import menu
import mouseManager
import algorithm


class Game():
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
            # screenWidth = self.screen.get_width()
            # screenHeight = self.screen.get_height()
            # rect = pygame.Rect(screenWidth - 200, screenHeight / 5 + 60 * 3, 100, 40)
            # self.reloadButton = pygame.draw.rect(self.screen, (255, 255, 255), rect)

            print("Level loaded")
            print("Rectangles:", self.level.rectangles)
            print("Statics:", self.level.statics)
            print("Centre points:", self.level.centrePoints)
            # print("Connections:", self.connections)

    def removeTile(self, tile):
        for array in self.level.statics:
            if array[0] == tile:
                return

        newPoints = copy.copy(self.points)
        # newConnections = copy.copy(self.connections)
        #
        # for i, connection in enumerate(self.connections):
        #     if self.dev: print("0:", connection[0], "1:", connection[1])
        #
        #     if connection[0] == tile:
        #         index = newConnections.index(connection)
        #         del newConnections[index]
        #         self.reloadBoard()
        #
        #         if self.dev: print("Deleted", connection)
        #     if connection[1] == tile:
        #         index = newConnections.index(connection)
        #         del newConnections[index]
        #         self.reloadBoard()
        #         if self.dev: print("Deleted", connection)
        #
        # self.connections = newConnections

        for i, point in enumerate(self.points):
            index = newPoints.index(point)
            del newPoints[index]
            self.reloadBoard()
        self.points = newPoints

    def reloadBoard(self):

        # self.buttons = self.graphicsManager.drawBoard(self.level)
        self.graphicsManager.drawBoard(self.level)

        for static in self.level.statics:
            tile, colour = static
            self.graphicsManager.drawEndPoint(tile, colour)

        for array in self.points:
            self.graphicsManager.drawEndPoint(array[0], array[1])

        # for array in self.connections:
        #     self.graphicsManager.drawLine(array[0], array[1], array[2])

        # self.smoothenTurns()

        # if checker.checkWin(self.level.statics, self.level.rectangles, self.findConnections):
        #     self.graphicsManager.drawWinScreen()

    def addPoint(self, tile, colour):
        self.points.append((tile, colour))
        self.reloadBoard()

    # def addConnection(self, tile1, tile2, colour):
    #     connectionsFound = 0
    #     staticTile = False
    #     connectionsFound += self.findConnections(tile1)[0]
    #     connectionsFound += self.findConnections(tile2)[0]
    #
    #     if connectionsFound > 1:
    #         falseConnection = True
    #     else:
    #         falseConnection = False
    #
    #         for static in self.level.statics:
    #
    #             if static[0] == tile1:
    #
    #                 if connectionsFound > 0:
    #                     falseConnection = True
    #                 else:
    #                     if static[1] != colour:
    #                         falseConnection = True
    #
    #             if static[0] == tile1 or static[0] == tile2:
    #                 if static[1] != colour:
    #                     falseConnection = True
    #
    #     if self.dev: print("Connections found:", connectionsFound)
    #
    #     if not falseConnection:
    #         self.connections.append((tile1, tile2, colour))
    #         self.reloadBoard()
    #         if self.dev: print("Connections:", self.connections)
    #     else:
    #         self.mouseManager.mousePressed = False
    #
    # def smoothenTurns(self):
    #     for connection in self.connections:
    #         centrePoint1 = self.level.centrePoints[connection[0]]
    #         centrePoint2 = self.level.centrePoints[connection[1]]
    #         self.graphicsManager.drawSmoothTurn(centrePoint1, connection[2])
    #         self.graphicsManager.drawSmoothTurn(centrePoint2, connection[2])
    #
    # def replaceConnection(self, tile, colour):
    #     self.removeTile(tile)
    #     self.addConnection(self.lastSelectedTile, tile, colour)

    def mousePressed(self):
        pos = pygame.mouse.get_pos()
        algorithms = algorithm.Algorithms(self, self.level)

        if self.graphicsManager.rectangles[0].collidepoint(pos):
            algorithms.dfs()

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

                # connectionsFound = self.findConnections(i)
                # if connectionsFound[0] == 1:
                #     self.mouseManager.mousePressed = True
                #     if self.dev: print("Mouse pressed on a coloured tile")
                #
                #     index = connectionsFound[1][0]
                #     self.selectedColour = self.connections[index][2]
                #     if self.dev: print("Selected colour:", self.selectedColour)
                #
                #     return
                # elif connectionsFound[0] == 2:
                #     if self.dev: print("Connections:", connectionsFound[0])
                #     self.removeTile(i)

    # def mouseMoved(self):
    #     pos = pygame.mouse.get_pos()
    #
    #     for i, rect in enumerate(self.level.rectangles):
    #         if rect.collidepoint(pos):
    #             if i != self.lastSelectedTile:
    #
    #                 neighbourTile = False
    #
    #                 if i == self.lastSelectedTile + 1:
    #                     neighbourTile = True
    #                 elif i == self.lastSelectedTile - 1:
    #                     neighbourTile = True
    #                 elif i == self.lastSelectedTile + self.level.width:
    #                     neighbourTile = True
    #                 elif i == self.lastSelectedTile - self.level.width:
    #                     neighbourTile = True
    #
    #                 if neighbourTile:
    #                     connectionsFound = self.findConnections(i)
    #                     if self.dev: print(f"Connections found: {connectionsFound[0]}")
    #
    #                     if connectionsFound[0] > 0:
    #
    #                         connectionIndex = connectionsFound[1][0]
    #                         if self.dev: print(f"Index: {connectionIndex}")
    #
    #                         colour = self.connections[connectionIndex][2]
    #                         if colour != self.selectedColour:
    #                             if self.dev: print("Replacing connection...")
    #                             self.replaceConnection(i, self.selectedColour)
    #                         else:
    #                             if self.dev: print("Backtracking, removing connection...")
    #                             self.removeTile(self.lastSelectedTile)
    #                         self.lastSelectedTile = i
    #
    #
    #                     else:
    #                         if self.dev: print("Tile changed:", i)
    #
    #                         self.addConnection(self.lastSelectedTile, i, self.selectedColour)
    #                         self.lastSelectedTile = i
    #
    #                 return

    # def findConnections(self, tile):
    #     connectionsFound = 0
    #     connectionIndex = []
    #
    #     for index, connection in enumerate(self.connections):
    #         if connection[0] == tile or connection[1] == tile:
    #             connectionsFound += 1
    #             connectionIndex.append(index)
    #
    #     return connectionsFound, connectionIndex


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

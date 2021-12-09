import math
import time

import numpy
import pygame.display
import webcolors
import random
import checker

class Algorithms:
    def __init__(self, game, level):
        self.game_board = [[0 for y in range(level.height)] for x in range(level.width)]
        self.game_board_enum = numpy.arange(level.width * level.height).reshape(level.height, level.width)
        self.colors = [0, 'r', 'g', 'b', 'c', 'y', 'm']
        self.static_coords = []
        self.game = game
        self.level = level
        self.empty_spaces = self.get_empty_spaces()

        for static in level.statics:
            counter = 0

            for i in range(level.height):
                for j in range(level.width):
                    if static[0] == counter:
                        if webcolors.rgb_to_name(static[1])[0] == 'l':
                            self.game_board[i][j] = 'G'
                            self.static_coords.append([i, j, 'G'])
                        else:
                            self.game_board[i][j] = webcolors.rgb_to_name(static[1])[0].upper()
                            self.static_coords.append([i, j, webcolors.rgb_to_name(static[1])[0].upper()])

                    counter += 1

    def dfs(self, index):
        pos = self.empty_spaces[index]
        coords = self.get_coords_from_index(pos)

        if self.game_board[coords[0]][coords[1]] == self.colors[6]:
            self.game_board[coords[0]][coords[1]] = self.colors[1]
            self.draw_board_console()
            # time.sleep(0.1)

            if index - 1 < 0:
                return

            self.dfs(index - 1)
        else:
            self.game_board[coords[0]][coords[1]] = self.colors[self.colors.index(self.game_board[coords[0]][coords[1]]) + 1]
            self.draw_board_console()
            # time.sleep(0.1)
            self.dfs(len(self.empty_spaces) - 1)

        # if delta < 36:
        #     coords = self.get_coords_from_index(delta)
        #
        #     if self.game_board[coords[0]][coords[1]] == 0:
        #         self.game.addPoint(delta, [255, 0, 0])
        #         self.game.reloadBoard()
        #
        #     delta += 1
        #     self.dfs(delta)

        # self.draw_board_console()
        #
        # for i in reversed(range(self.level.height)):
        #     for j in reversed(range(self.level.width)):
        #         if self.game_board[i][j] == 0:
        #             self.game_board[i][j] = 'A'
        #             self.draw_board_console()
        #             self.game.addPoint(self.game_board_enum[i][j], [255, 0, 0])
        #             self.game.reloadBoard()
        #             time.sleep(0.1)



        # while True:
        #     if currentpos[1]+1 < self.level.width:
        #         currentpos[1] += 1
        #         self.game_board[currentpos[0]][currentpos[1]] = static[2]
        #         self.draw_board_console()
        #     else:
        #         break

        # for x in range(5):
        #     main.Game.addConnection(self.game, x, x + 1, [255, 0, 0])
        #     main.Game.reloadBoard(self.game)

        return

    def get_empty_spaces(self):
        empty_spaces = list(range(self.level.width * self.level.height))

        for static in self.level.statics:
            empty_spaces.remove(static[0])

        return empty_spaces

    def get_coords_from_index(self, index):
        for i in range(self.level.height):
            for j in range(self.level.width):
                if index == self.game_board_enum[i][j]:
                    return [i, j]

    def draw_board_console(self):
        for x in range(self.level.height):
            for y in range(self.level.width):
                print(self.game_board[x][y], end=' ')

            print('\n', end='')

        print('\n')

    def checkNeighbours(self, point):
        tile = point[0]
        side = math.ceil(math.sqrt(len(self.level.rectangles)))
        neighbours = 0
        neighbours_array = []

        if tile + 1 < side*side and tile != side-1 and tile != side*2-1 and tile != side*3-1 and tile != side*4-1 and tile != side*5-1:
            neighbours += 1
            neighbours_array.append(tile + 1)
        if tile - 1 > -1 and tile != side and tile != side*2 and tile != side*3 and tile != side*4 and tile != side*5:
            neighbours += 1
            neighbours_array.append(tile - 1)
        if tile + side < side*side:
            neighbours += 1
            neighbours_array.append(tile + side)
        if tile - side > -1:
            neighbours += 1
            neighbours_array.append(tile - side)

        return neighbours, neighbours_array

    def makeConnection(self, point, forbiddenpoints):
        neigbours, neigbours_array = self.checkNeighbours(point)
        random.shuffle(neigbours_array)
        for x in range(neigbours):
            if not self.checkIfStatic(neigbours_array[x]) and not self.checkIfPoint(neigbours_array[x]) and not self.checkIfForbiddenPoint(point[0], neigbours_array[x], forbiddenpoints):
                self.game.addPoint(neigbours_array[x], point[1])
                pygame.display.update()
                time.sleep(0.05)
                if self.game.points:
                    return self.game.points[-1]
        return False

    def checkIfStatic(self, tile):
        for s in self.level.statics:
            if s[0] == tile:
                return True
        return False

    def checkIfPoint(self, tile):
        if self.game.points:
            for p in self.game.points:
                if p[0] == tile:
                    return True
        return False

    def checkIfForbiddenPoint(self, currentPoint, tile, forbiddenpoints):
        if forbiddenpoints:
            for p in forbiddenpoints:
                for t in p[1]:
                    if p[0] == currentPoint and t == tile:
                        return True
        return False

    def checkIfEnd(self, point, endpoint):
        neigbours, neigbours_array = self.checkNeighbours(point)
        for x in range(neigbours):
            if neigbours_array[x] == endpoint[0]:
                return True
        return False

    def checkIfEndConnected(self, endpoint):
        for p in self.game.points:
            neigbours, neigbours_array = self.checkNeighbours(p)
            for x in range(neigbours):
                if neigbours_array[x] == endpoint[0]:
                    return True
        return False

    def clearBoard(self, color):
        for p in self.game.points:
            if p[1] == color:
                self.game.removeTile(p[0])

    def clearForbiddenPoints(self, forbiddenpoints):
        newForbiddenPoints = []
        if forbiddenpoints:
            for f in forbiddenpoints:
                for p in self.game.points:
                    if p[0] == f[0]:
                        newForbiddenPoints.append(f)
        return newForbiddenPoints

    def backtrack(self):
        visitedpoints = []
        forbiddenpoints = []
        start = []
        end = []
        checkedStatics = []
        statics = self.level.statics
        totalvisitedcount = 0

        for static in statics:
            if static not in checkedStatics:
                start.append(static)
                checkedStatics.append(start)
                for static2 in statics:
                    if static2[1] == static[1] and static2[0] != static[0]:
                        end.append(static2)
                        checkedStatics.append(static2)

        while not checker.checkWin(self.level.statics, self.level.rectangles, self.game.points):
            visitedpoints.clear()
            forbiddenpoints.clear()
            iterator = 0
            self.game.points.clear()
            while iterator < len(start):
                visitedpoints.append(start[iterator])
                while not self.checkIfEnd(visitedpoints[-1], end[iterator]):
                    test = self.makeConnection(visitedpoints[-1], forbiddenpoints)
                    totalvisitedcount += 1
                    print("Total visited", totalvisitedcount)
                    if test:
                        visitedpoints.append(test)
                    else:
                        if self.checkIfEndConnected(end[iterator]) or len(visitedpoints) < 2:
                            visitedpoints.clear()
                            break
                        fp = [visitedpoints[-2][0], [visitedpoints[-1][0]]]
                        forbiddenpoints.append(fp)
                        self.game.removeTile(visitedpoints[-1][0])
                        visitedpoints.pop()
                forbiddenpoints = self.clearForbiddenPoints(forbiddenpoints)

                visitedpoints.clear()
                iterator += 1

        return

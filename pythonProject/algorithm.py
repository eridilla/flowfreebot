import math
import time
from datetime import datetime

import numpy
import webcolors
import random

from pygame import KEYDOWN, K_ESCAPE

import checker
import pygame


class Algorithms:
    def __init__(self, game, level):
        self.game_board = [[0 for y in range(level.height)] for x in range(level.width)]
        self.game_board_enum = numpy.arange(level.width * level.height).reshape(level.height, level.width)
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

        self.colors = self.get_colors_from_game()

    def dfs(self):
        index = len(self.empty_spaces) - 1
        steps = 0
        start = datetime.now()

        print("Start: ", start)

        while not checker.checkWin(self.level.statics, self.level.rectangles, self.game.points):
            pos = self.empty_spaces[index]
            coords = self.get_coords_from_index(pos)

            mousepos = pygame.mouse.get_pos()
            if self.game.graphicsManager.rectangles[4].collidepoint(mousepos):
                self.game.__init__()

            if self.game_board[coords[0]][coords[1]] == self.colors[len(self.colors) - 1]:
                self.game_board[coords[0]][coords[1]] = self.colors[1]
                steps += 1
                print(steps)
                self.draw_board_console()
                self.game.removeTile(pos)
                self.game.addPoint(pos, self.get_color_rgb(self.colors[1]))
                pygame.display.update()

                if index - 1 < 0:
                    return

                index -= 1

            else:
                self.game_board[coords[0]][coords[1]] = self.colors[
                    self.colors.index(self.game_board[coords[0]][coords[1]]) + 1]
                steps += 1
                print(steps)
                self.draw_board_console()
                self.game.removeTile(pos)
                self.game.addPoint(pos, self.get_color_rgb(
                    self.colors[self.colors.index(self.game_board[coords[0]][coords[1]])]))
                pygame.display.update()
                index = len(self.empty_spaces) - 1

        end = datetime.now()

        print("Start: ", start)
        print("End: ", end)
        print("Steps: ", steps)

        return

    def get_colors_from_game(self):
        colors = [0]

        for i, color in enumerate(self.static_coords):
            if i % 2 == 0:
                colors.append(color[2].lower())

        return colors

    def get_color_rgb(self, color):
        if color == 'r':
            return [255, 0, 0]
        elif color == 'g':
            return [0, 255, 0]
        elif color == 'b':
            return [0, 0, 255]
        elif color == 'c':
            return [0, 255, 255]
        elif color == 'y':
            return [255, 255, 0]
        elif color == 'm':
            return [255, 0, 255]

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
                self.game.points_visited += 1
                self.game.reloadBoard()
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
                if neigbours_array[x] == endpoint[0] and endpoint[1] == p[1]:
                    return True
        return False

    def clearBoard(self, colors):

        for c in colors:
            for p in self.game.points:
                if p[1] == c:
                    self.game.removeTile(p[0])

    def clearForbiddenPoints(self, forbiddenpoints):
        newForbiddenPoints = []
        if forbiddenpoints:
            for f in forbiddenpoints:
                for p in self.game.points:
                    if p[0] == f[0]:
                        newForbiddenPoints.append(f)
        return newForbiddenPoints

    def checkIfWrong(self, wrongSollutions):
        result = 0
        for points in wrongSollutions:
            count = 0
            if len(points) != len(self.game.points):
                continue
            for p1 in points:
                for p2 in self.game.points:
                    if p1[0] == p2[0] and p1[1] == p2[1]:
                        count += 1
            if count == len(points):
                result += 1
        return result

    # def checkBlockingColors(self, color):
    #     colors = []
    #     for p in self.game.points:
    #         if p[1] == color:
    #             neigbours, neighbour_lists = self.checkNeighbours(p)
    #             for n in neighbour_lists:
    #                 for p2 in self.game.points:
    #                     if p2[0] == n and p2[1] != color:
    #                         colors.append(p2[1])
    #
    #     print("Colors", colors)

    def backtrack(self):
        visitedpoints = []
        forbiddenpoints = []
        start = []
        end = []
        checkedStatics = []
        statics = self.level.statics
        wrongSollutions = []

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
                    for event in pygame.event.get():
                        if event.type == KEYDOWN:
                            if event.key == K_ESCAPE:
                                self.game.points_visited = 0
                                return
                    test = self.makeConnection(visitedpoints[-1], forbiddenpoints)
                    if test:
                        visitedpoints.append(test)
                    else:
                        if self.checkIfEndConnected(end[iterator]):
                            visitedpoints.clear()
                            break
                        if len(visitedpoints) < 2:
                            if self.checkIfWrong(wrongSollutions) > 1:
                                value = 3
                                colors = []
                                for i in reversed(range(value)):
                                    colors.append(end[iterator-i][1])
                                self.clearBoard(colors)
                                if iterator-value < -1:
                                    iterator = -1
                                else:
                                    iterator -= 3
                                #wrongSollutions.clear()
                                break
                            wrongSollutions.append(self.game.points)
                            self.clearBoard([end[iterator][1], end[iterator-1][1]])
                            if iterator-2 < -1:
                                iterator = -1
                            else:
                                iterator -= 2
                            break
                        fp = [visitedpoints[-2][0], [visitedpoints[-1][0]]]
                        forbiddenpoints.append(fp)
                        self.game.removeTile(visitedpoints[-1][0])
                        self.game.reloadBoard()
                        time.sleep(0.05)
                        visitedpoints.pop()

                forbiddenpoints = self.clearForbiddenPoints(forbiddenpoints)
                visitedpoints.clear()
                iterator += 1
        return

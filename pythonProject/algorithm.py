import time

import pygame, sys, math, json, numpy, webcolors, pyautogui, main


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
            self.game.addPoint(pos, self.get_color_rgb(self.colors[1]))
            self.game.reloadBoard()
            # time.sleep(0.5)

            if index - 1 < 0:
                return

            self.dfs(index - 1)
        else:
            self.game_board[coords[0]][coords[1]] = self.colors[self.colors.index(self.game_board[coords[0]][coords[1]]) + 1]
            self.draw_board_console()
            self.game.addPoint(pos, self.get_color_rgb(self.colors[self.colors.index(self.game_board[coords[0]][coords[1]])]))
            self.game.reloadBoard()
            # time.sleep(0.5)
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

    def get_index_from_color(self, color):
        for i, colorX in enumerate(self.colors):
            if colorX == color:
                return i

    def delta_is_static(self, delta):
        for static in self.level.statics:
            if static[0] == delta:
                return True

        return False

    def get_coords_from_index(self, index):
        for i in range(self.level.height):
            for j in range(self.level.width):
                if index == self.game_board_enum[i][j]:
                    return [i, j]

    def generate_line(self, static):
        moves_made = []
        currentpos = [static[0], static[1]]
        return

    def check_end(self, currentpos, color):
        if currentpos[1] + 1 == color:
            self.move(currentpos, 'E')
            return

        if currentpos[1] - 1 == color:
            self.move(currentpos, 'W')
            return

        if currentpos[0] + 1 == color:
            self.move(currentpos, 'S')
            return

        if currentpos[0] - 1 == color:
            self.move(currentpos, 'N')
            return

    def move(self, currentpos, direction):
        if direction == 'E':
            currentpos = [currentpos[0], currentpos[1] + 1]
            return currentpos

        if direction == 'W':
            currentpos = [currentpos[0], currentpos[1] - 1]
            return currentpos

        if direction == 'S':
            currentpos = [currentpos[0] + 1, currentpos[1]]
            return currentpos

        if direction == 'N':
            currentpos = [currentpos[0] - 1, currentpos[1]]
            return currentpos

    def check_possible_moves(self, currentpos):
        possible_moves = []

        if currentpos[1] + 1 < self.level.width:
            if self.game_board[currentpos[0]][currentpos[1] + 1] == 0:
                possible_moves.append('E')

        if currentpos[1] - 1 >= 0:
            if self.game_board[currentpos[0]][currentpos[1] - 1] == 0:
                possible_moves.append('W')

        if currentpos[0] + 1 < self.level.height:
            if self.game_board[currentpos[0] + 1][currentpos[1]] == 0:
                possible_moves.append('S')

        if currentpos[0] - 1 >= 0:
            if self.game_board[currentpos[0] - 1][currentpos[1]] == 0:
                possible_moves.append('N')

        return possible_moves

    def draw_board_console(self):
        for x in range(self.level.height):
            for y in range(self.level.width):
                print(self.game_board[x][y], end=' ')

            print('\n', end='')

        print('\n')

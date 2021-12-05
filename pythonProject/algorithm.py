import pygame, sys, math, json, numpy, webcolors, pyautogui, main


class Algorithms:
    def __init__(self, game, level):
        self.game_board = [[0 for y in range(level.height)] for x in range(level.width)]
        self.game_board_enum = numpy.arange(level.width * level.height).reshape(level.height, level.width)
        self.static_coords = []
        self.game = game
        self.level = level

        for static in level.statics:
            counter = 0

            for i in range(level.height):
                for j in range(level.width):
                    if static[0] == counter:
                        if webcolors.rgb_to_name(static[1])[0] == 'l':
                            self.game_board[i][j] = 'g'
                            self.static_coords.append([i, j, 'g'])
                        else:
                            self.game_board[i][j] = webcolors.rgb_to_name(static[1])[0]
                            self.static_coords.append([i, j, webcolors.rgb_to_name(static[1])[0]])

                    counter += 1

    def dfs(self):
        self.draw_board_console()
        static = self.static_coords[0]
        currentpos = [static[0], static[1]]

        possible_moves = self.check_possible_moves(currentpos)

        self.game.addConnection(2,3,[255,0,0])
        self.game.reloadBoard()

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

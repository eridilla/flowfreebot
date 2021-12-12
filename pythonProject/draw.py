import pygame, math

class GraphicsManager():
    def __init__(self, gameLogic):
        self.logic = gameLogic
        self.level = gameLogic.level
        self.rectangles = []

    def drawBoard(self, level, points_visited, time):

        length = level.length

        totalHeight = length * level.height
        totalWidth = length * level.width

        board = pygame.Rect(length, length, length + totalWidth, length + totalHeight)
        pygame.draw.rect(self.logic.screen, (0, 0, 0), board)

        borderColour = (64, 64, 176)

        for rectangle in level.rectangles:
            pygame.draw.rect(self.logic.screen, borderColour, rectangle, 5)

        screenWidth, screenHeight = self.logic.screen.get_size()
        font = pygame.font.SysFont("framd.ttf", 48)

        dfs_button = pygame.Rect(screenWidth - 200, screenHeight/5, 100, 40)
        dfs_surface = font.render("DFS", True, (0, 0, 0))
        pygame.draw.rect(self.logic.screen, (255,255,255), dfs_button)
        self.logic.screen.blit(dfs_surface, (screenWidth - 200, screenHeight/5))
        self.rectangles.append(dfs_button)

        bt_button = pygame.Rect(screenWidth - 200, screenHeight / 5 + 60, 100, 40)
        bt_surface = font.render("BT", True, (0, 0, 0))
        pygame.draw.rect(self.logic.screen, (255, 255, 255), bt_button)
        self.logic.screen.blit(bt_surface, (screenWidth - 200, screenHeight / 5+60))
        self.rectangles.append(bt_button)

        ft_button = pygame.Rect(screenWidth - 200, screenHeight / 5 + 60 * 2, 100, 40)
        ft_surface = font.render("FT", True, (0, 0, 0))
        pygame.draw.rect(self.logic.screen, (255, 255, 255), ft_button)
        self.logic.screen.blit(ft_surface, (screenWidth - 200, screenHeight / 5 + 60 * 2))
        self.rectangles.append(ft_button)

        reset_button = pygame.Rect(screenWidth - 200, screenHeight / 5 + 60 * 3, 100, 40)
        reset_surface = font.render("Reset", True, (0, 0, 0))
        pygame.draw.rect(self.logic.screen, (255, 255, 255), reset_button)
        self.logic.screen.blit(reset_surface, (screenWidth - 200, screenHeight / 5 + 60 * 3))
        self.rectangles.append(reset_button)

        menu_button = pygame.Rect(screenWidth - 200, screenHeight / 5 + 60 * 4, 100, 40)
        menu_surface = font.render("Menu", True, (0, 0, 0))
        pygame.draw.rect(self.logic.screen, (255, 255, 255), menu_button)
        self.logic.screen.blit(menu_surface, (screenWidth - 200, screenHeight / 5 + 60 * 4))
        self.rectangles.append(menu_button)

        stat_background = pygame.Rect(screenWidth - 200, screenHeight / 5 + 60 * 6, 300, 40)
        pygame.draw.rect(self.logic.screen, (0, 0, 0), stat_background)
        points_visited_surface = font.render("Počet uzlov: " + str(points_visited), True, (255, 255, 255))
        self.logic.screen.blit(points_visited_surface, (screenWidth - 280, screenHeight / 5 + 60 * 6))

        time_background = pygame.Rect(screenWidth - 200, screenHeight / 5 + 60 * 7, 300, 40)
        pygame.draw.rect(self.logic.screen, (0, 0, 0), time_background)
        time_surface = font.render("Čas: " + str(round((pygame.time.get_ticks()-time)/1000, 2)) + "s", True, (255, 255, 255))
        self.logic.screen.blit(time_surface, (screenWidth - 280, screenHeight / 5 + 60 * 7))

        return

    def drawEndPoint(self, tile, colour):
        centrePoint = self.level.centrePoints[tile]
        pygame.draw.circle(self.logic.screen, colour, centrePoint, math.floor(self.level.length / 3), 25)

    def drawEndStatics(self, tile, colour):
        centrePoint = self.level.centrePoints[tile]
        pygame.draw.circle(self.logic.screen, colour, centrePoint, math.floor(self.level.length / 3))

    def drawWinScreen(self):
        screenWidth, screenHeight = self.logic.screen.get_size()
        middleX = math.floor(screenWidth / 2 + 0.5)
        middleY = math.floor(screenHeight / 2 + 0.5)

        width, height = 400, 250
        left = middleX - width / 2
        top = middleY - height / 2

        winRect = pygame.Rect(left, top, width, height)

        pygame.draw.rect(self.logic.screen, (0, 0, 0), winRect)
        pygame.draw.rect(self.logic.screen, (255, 255, 255), winRect, 5)

        font = pygame.font.SysFont("framd.ttf", 48)
        textSurface = font.render("Level Complete!", True, (255, 255, 255))
        size = font.size("Level Complete!")

        left = math.floor(middleX - size[0]/2 + 0.5)
        top = math.floor(middleY - size[1]/2 + 0.5)

        self.logic.screen.blit(textSurface, (left, top))
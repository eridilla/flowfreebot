import pygame, math

class GraphicsManager():
    def __init__(self, gameLogic):
        self.logic = gameLogic
        self.level = gameLogic.level
        self.rectangles = []

    def drawBoard(self, level):

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

        # rectangles = []
        dfs_button = pygame.Rect(screenWidth - 200, screenHeight/5, 100, 40)
        dfs_surface = font.render("DFS", True, (0, 0, 0))
        #size = font.size("DFS")
        pygame.draw.rect(self.logic.screen, (255,255,255), dfs_button)
        self.logic.screen.blit(dfs_surface, (screenWidth - 200, screenHeight/5))
        self.rectangles.append(dfs_button)

        bt_button = pygame.Rect(screenWidth - 200, screenHeight / 5 + 60, 100, 40)
        bt_surface = font.render("BT", True, (0, 0, 0))
        #size = font.size("BT")
        pygame.draw.rect(self.logic.screen, (255, 255, 255), bt_button)
        self.logic.screen.blit(bt_surface, (screenWidth - 200, screenHeight / 5+60))
        self.rectangles.append(bt_button)

        ft_button = pygame.Rect(screenWidth - 200, screenHeight / 5 + 60 * 2, 100, 40)
        ft_surface = font.render("FT", True, (0, 0, 0))
        # size = font.size("FT")
        pygame.draw.rect(self.logic.screen, (255, 255, 255), ft_button)
        self.logic.screen.blit(ft_surface, (screenWidth - 200, screenHeight / 5 + 60 * 2))
        self.rectangles.append(ft_button)

        reset_button = pygame.Rect(screenWidth - 200, screenHeight / 5 + 60 * 3, 100, 40)
        reset_surface = font.render("Reset", True, (0, 0, 0))
        # size = font.size("Reset")
        pygame.draw.rect(self.logic.screen, (255, 255, 255), reset_button)
        self.logic.screen.blit(reset_surface, (screenWidth - 200, screenHeight / 5 + 60 * 3))
        self.rectangles.append(reset_button)

        menu_button = pygame.Rect(screenWidth - 200, screenHeight / 5 + 60 * 4, 100, 40)
        menu_surface = font.render("Menu", True, (0, 0, 0))
        # size = font.size("Menu")
        pygame.draw.rect(self.logic.screen, (255, 255, 255), menu_button)
        self.logic.screen.blit(menu_surface, (screenWidth - 200, screenHeight / 5 + 60 * 4))
        self.rectangles.append(menu_button)

        return

    def drawEndPoint(self, tile, colour):
        centrePoint = self.level.centrePoints[tile]
        pygame.draw.circle(self.logic.screen, colour, centrePoint, math.floor(self.level.length / 3), 25)

    def drawEndStatics(self, tile, colour):
        centrePoint = self.level.centrePoints[tile]
        pygame.draw.circle(self.logic.screen, colour, centrePoint, math.floor(self.level.length / 3))

    # def drawLine(self, tile1, tile2, colour):
    #
    #     tile1Centre = self.level.centrePoints[tile1]
    #     tile2Centre = self.level.centrePoints[tile2]
    #
    #     width = math.floor(self.level.length / 4 + 0.5)
    #
    #     if width % 2 == 0:
    #         width += 1
    #     self.radius = math.floor(width / 2)
    #
    #     rect = pygame.draw.line(self.logic.screen, colour, tile1Centre, tile2Centre, width)
    #
    # def drawSmoothTurn(self, point, colour):
    #     pygame.draw.circle(self.logic.screen, colour, point, self.radius)

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
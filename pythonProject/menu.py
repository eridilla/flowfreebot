import pygame, sys, math, json
import levels

class Menu():
    def __init__(self, main):
        self.main = main
        pygame.init()
        self.screenSize = (500, 700)
        screen = pygame.display
        self.caption = screen
        self.screen = screen.set_mode(self.screenSize)

        self.menu = "main"

        self.rectangles = self.drawMenu()
        self.eventman = EventManager()
        self.mainLoop()
        # print("Exited mainloop in menu")

    def mainLoop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # print("Exiting..")
                    sys.exit()

                response = self.eventman.processEvent(event, self.menu, self.rectangles)
                if response == "back":
                    return
                elif type(response) == type(lambda: print()):
                    # print("Trying to load level")
                    self.main.level = response()
                    self.main.initialise()
                    # print("return")
                    return

            pygame.display.flip()

    def clearScreen(self):
        self.rectangles = []
        s = pygame.Rect((0, 0), self.screenSize)
        pygame.draw.rect(self.screen, (0, 0, 0), s)

    def drawMenu(self):
        self.clearScreen()

        self.menu = "levels"
        self.caption.set_caption("Levels")
        self.rectangles = []

        font = pygame.font.SysFont("framd.ttf", 72)
        textSurface = font.render("Levels", True, (255, 255, 255))
        size = font.size("Levels")

        x = math.floor(self.screenSize[0] / 2 - size[0] / 2 + 0.5)
        y = math.floor(self.screenSize[1] / 15)

        self.screen.blit(textSurface, (x, y))

        with open("levels.json") as f:
            levels = json.loads(f.read())

        rects = []

        for i in range(len(levels)):
            rects.append(self.createLevelButton(i))

        return rects

    def createLevelButton(self, number):
        sideLength = math.floor(self.screenSize[0] / 7)
        buttonLength = sideLength * 0.8

        boxSize = (buttonLength, buttonLength)

        boxX = math.floor(sideLength * 1.1 + (((number) % 5)) * sideLength)
        boxY = math.floor(sideLength * 1.1 + (((number) // 5) + 1) * sideLength)

        levelBox = pygame.Rect((boxX, boxY), boxSize)
        pygame.draw.rect(self.screen, (0, 0, 0), levelBox)
        pygame.draw.rect(self.screen, (255, 255, 255), levelBox, 5)

        text = str(number + 1)
        font = pygame.font.SysFont("framd.ttf", 36)
        textSurface = font.render(text, True, (255, 255, 255))
        size = font.size(text)

        x = boxX + math.floor((boxSize[0] / 2 + 0.5) - size[0] / 2)
        y = boxY + math.floor((boxSize[1] / 2 + 0.5) - size[1] / 2)
        self.screen.blit(textSurface, (x, y))

        return levelBox


class EventManager():
    def __init__(self):
        pass

    def processEvent(self, event, menu, rectangles):
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            # print("Mouse pressed")
            if menu == "levels":
                for i, rectangle in enumerate(rectangles):
                    if rectangle.collidepoint(pos):
                        # print("Level nr " + str(i))

                        if i == len(rectangles):
                            return "back"
                        else:
                            return lambda: levels.getLevel(i)

            elif menu == "main":
                pass


if __name__ == "__main__":
    menu = Menu()
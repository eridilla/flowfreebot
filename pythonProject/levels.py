import random, json, math
import pygame


class Level():
    def __init__(self, points, width, height):
        self.length = self.__getSideLength(width, height)
        self.screenSize = self.length * (width + 2) + 200, self.length * (height + 2)
        self.width = width
        self.height = height
        self.statics = self.__createStatics(points)
        self.rectangles, self.centrePoints = self.__createTiles(self.length, width, height)

    def __getSideLength(self, width, height):
        with open("config.txt") as f:
            config = json.loads(f.read())

        tileWidth = config["screenWidth"]
        tileHeight = config["screenHeight"]

        tileHeight = math.floor(tileHeight / (height + 2))
        tileWidth = math.floor(tileWidth / (width + 2))

        if tileHeight > tileWidth:
            sideLength = tileWidth
        else:
            sideLength = tileHeight

        return sideLength

    def __createStatics(self, points):

        statics = []
        for array in points:
            colour = array[0]
            index1 = array[1]
            index2 = array[2]
            statics.append([index1, colour])
            statics.append([index2, colour])

        return statics

    def __createTiles(self, length, width, height):

        rectangles = []
        centrePoints = []

        totalHeight = length * height
        totalWidth = length * width

        y = length
        while y < totalHeight + length:

            x = length
            while x < totalWidth + length:
                rectangle = pygame.Rect(x, y, length, length)
                rectangles.append(rectangle)

                centrePoint = (math.floor(x + length / 2), math.floor(y + length / 2))
                centrePoints.append(centrePoint)

                x += length
            y += length

        return rectangles, centrePoints


# Colours
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
magenta = (255, 0, 255)
cyan = (0, 255, 255)
white = (255, 255, 255)
grey = (127, 127, 127)
orange = (255, 128, 0)
darkGreen = (0, 100, 0)
purple = (128, 0, 128)
darkRed = (139, 0, 0)

with open("levels.json") as f:
    levels = json.loads(f.read())


def getRandomLevel():
    level = random.randint(0, len(levels) - 1)
    return Level(levels[level]["points"], levels[level]["width"], levels[level]["height"])


def getLevel(number):
    level = Level(levels[number]["points"], levels[number]["width"], levels[number]["height"])
    return level


def getTestLevel():
    with open("tempsave.json") as f:
        level = json.loads(f.read())[0]
        return Level(level["points"], level["width"], level["height"])
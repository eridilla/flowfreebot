def checkWin(statics, rectangles, findConnections):

    size = len(rectangles)

    for i in range(size):
        staticTile = False
        for static in statics:
            if static[0] == i:
                if findConnections(i)[0] != 1:
                    return False
                staticTile = True
                break

        if not staticTile:
            if findConnections(i)[0] != 2:
                return False

    return True
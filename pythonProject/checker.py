import math


def checkWin(statics, rectangles, points):

    if len(rectangles) != len(points) + len(statics):
        return False

    for point in points:
        check, checks = checkNeighbours(rectangles, point, points, statics)
        if check < 2:
            return False

    return checkConnection(rectangles, statics, points)


def checkNeighbours(rectangles, point, points, statics):
    index = point[0]
    neighbours = 0
    side = math.ceil(math.sqrt(len(rectangles)))
    neighbours_list = []

    for p in points:
        if p[0] == index - 1 and p[0] % side != 5 and p[1] == point[1]:
            neighbours += 1
            neighbours_list.append(p)
            # print("Left p", index - 1)
        if p[0] == index + 1 and p[0] % side != 0 and p[1] == point[1]:
            neighbours += 1
            neighbours_list.append(p)
            # print("Right p", index + 1)
        if p[0] == index + side and p[1] == point[1]:
            neighbours += 1
            neighbours_list.append(p)
            # print("Down p", index+side+1)
        if p[0] == index - side and p[1] == point[1]:
            neighbours += 1
            neighbours_list.append(p)
            # print("Up p", index-side-1)

    for s in statics:
        if s[0] == index - 1 and s[0] % side != 5 and s[1] == point[1]:
            neighbours += 1
            neighbours_list.append(s)
            # print("Left s", index - 1)
        if s[0] == index + 1 and s[0] % side != 0 and s[1] == point[1]:
            neighbours += 1
            neighbours_list.append(s)
            # print("Right s", index + 1)
        if s[0] == index + side and s[1] == point[1]:
            neighbours += 1
            neighbours_list.append(s)
            # print("Down s", index + side + 1)
        if s[0] == index - side and s[1] == point[1]:
            neighbours += 1
            neighbours_list.append(s)
            # print("Up s", index - side - 1)

    # print("Neigbours for", index ,neighbours)
    return neighbours, neighbours_list


def checkConnection(rectangles, statics, points):

    sum_statics = len(statics)/2
    checkedStatics = []
    start = []
    end = []
    iterator = 0
    results = []
    result_found = False

    for static in statics:
        if static not in checkedStatics:
            start.append(static)
            checkedStatics.append(start)
            for static2 in statics:
                if static2[1] == static[1] and static2[0] != static[0]:
                    end.append(static2)
                    checkedStatics.append(static2)

    # for x in range(len(start)):
    #     print("Prvok start", x, start[x])
    # for x in range(len(end)):
    #     print("Prvok end", x, end[x])

    while 1:
        checkedPoints = []
        previousPoint = []
        currentPoint = start[iterator]
        print("Starting point",start[iterator])
        print("End point", end[iterator])
        previousPoint.append(start[iterator])

        for x in range(36):
            print("Currentpoint", currentPoint)
            check, checks = checkNeighbours(rectangles, currentPoint, points, statics)

            for c in checks:
                if c == end[iterator]:
                    results.append(1)
                    print("Added to results")
                    result_found = True
                    break

            if result_found:
                result_found = False
                break

            if check == 0:
                checkedPoints.append(currentPoint)
                if len(previousPoint) > 0:
                    currentPoint = previousPoint.pop()

            if check == 1:
                checkedPoints.append(currentPoint)
                if checks[0] not in checkedPoints:
                    previousPoint.append(currentPoint)
                    currentPoint = checks[0]
                else:
                    if len(previousPoint) > 0:
                        currentPoint = previousPoint.pop()

            if check == 2:
                checkedPoints.append(currentPoint)
                if checks[0] not in checkedPoints:
                    previousPoint.append(currentPoint)
                    currentPoint = checks[0]
                elif checks[1] not in checkedPoints:
                    previousPoint.append(currentPoint)
                    currentPoint = checks[1]
                else:
                    if len(previousPoint) > 0:
                        currentPoint = previousPoint.pop()

            if check == 3:
                checkedPoints.append(currentPoint)
                if checks[0] not in checkedPoints:
                    previousPoint.append(currentPoint)
                    currentPoint = checks[0]
                elif checks[1] not in checkedPoints:
                    previousPoint.append(currentPoint)
                    currentPoint = checks[1]
                elif checks[2] not in checkedPoints:
                    previousPoint.append(currentPoint)
                    currentPoint = checks[2]
                else:
                    if len(previousPoint)>0:
                        currentPoint = previousPoint.pop()

            if check == 4:
                checkedPoints.append(currentPoint)
                if checks[0] not in checkedPoints:
                    previousPoint.append(currentPoint)
                    currentPoint = checks[0]
                elif checks[1] not in checkedPoints:
                    previousPoint.append(currentPoint)
                    currentPoint = checks[1]
                elif checks[2] not in checkedPoints:
                    previousPoint.append(currentPoint)
                    currentPoint = checks[2]
                elif checks[3] not in checkedPoints:
                    previousPoint.append(currentPoint)
                    currentPoint = checks[3]
                else:
                    if len(previousPoint) > 0:
                        currentPoint = previousPoint.pop()

        iterator += 1
        if iterator == sum_statics:
            break

    if len(results)<sum_statics:
        return False

    return True

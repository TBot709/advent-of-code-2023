from debug import debug


def scanfill(sGrid: str, edgeChar: str, notEdgeChar: str) -> str:
    lines = sGrid.split('\n')

    for i, line in enumerate(lines):
        if len(line) < 3:
            lines.remove(line)

    emptyGridLine = []
    emptyFlagLine = []
    for c in range(len(lines[0]) + 2):
        emptyGridLine.append(notEdgeChar)
        emptyFlagLine.append(False)

    grid = []
    insideFlagGrid = []
    grid.append(emptyGridLine)
    insideFlagGrid.append(emptyFlagLine.copy())
    for line in lines:
        gridLine = []
        line = notEdgeChar + line + notEdgeChar
        for c in line:
            gridLine.append(c)
        grid.append(gridLine)
        insideFlagGrid.append(emptyFlagLine.copy())
    grid.append(emptyGridLine)
    insideFlagGrid.append(emptyFlagLine.copy())

    NORTH = 'N'
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'
    UNKNOWN = 'U'

    # horizontal scan
    for y in range(1, len(grid) - 1):
        isInside = False
        edgeTailDir = UNKNOWN
        for x in range(1, len(grid[0]) - 1):
            window = (grid[y][x - 1], grid[y][x], grid[y][x + 1])

            if window == (notEdgeChar, edgeChar, notEdgeChar):
                isInside = not isInside
            elif window == (notEdgeChar, edgeChar, edgeChar):
                if grid[y - 1][x] == edgeChar:
                    edgeTailDir = NORTH
                else:
                    edgeTailDir = SOUTH
            elif window == (edgeChar, edgeChar, notEdgeChar):
                # if head and tail are in opposite directions
                if (grid[y - 1][x] == edgeChar and edgeTailDir == SOUTH
                        or
                        grid[y + 1][x] == edgeChar and edgeTailDir == NORTH):
                    isInside = not isInside
                edgeTailDir = UNKNOWN

            if isInside:
                insideFlagGrid[y][x] = True
            # debug(f"{y} {x} {grid[y][x]} {isInside} {insideFlagGrid[y]}")

    # vertical scan
    for x in range(1, len(grid[0]) - 1):
        isInside = False
        edgeTailDir = UNKNOWN
        for y in range(1, len(grid) - 1):
            window = (grid[y - 1][x], grid[y][x], grid[y + 1][x])

            if window == (notEdgeChar, edgeChar, notEdgeChar):
                isInside = not isInside
            elif window == (notEdgeChar, edgeChar, edgeChar):
                if grid[y][x + 1] == edgeChar:
                    edgeTailDir = EAST
                else:
                    edgeTailDir = WEST
            elif window == (edgeChar, edgeChar, notEdgeChar):
                # if head and tail are in opposite directions
                if (grid[y][x + 1] == edgeChar and edgeTailDir == WEST
                        or
                        grid[y][x - 1] == edgeChar and edgeTailDir == EAST):
                    isInside = not isInside
                edgeTailDir = UNKNOWN

            if isInside:
                insideFlagGrid[y][x] = True

    s = ""
    for y, line in enumerate(insideFlagGrid):
        # debug(f"{y} {line}")
        for x, f in enumerate(line):
            # debug(f"\t{x} {f} {grid[y][x]}")
            if f is True:
                s += edgeChar
            else:
                s += grid[y][x]
        s += '\n'

    return s

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

    # horizontal scan
    for y in range(1, len(grid) - 1):
        isInside = False
        for x in range(1, len(grid[0]) - 1):
            if grid[y][x - 1] == notEdgeChar and \
                    grid[y][x] == edgeChar and \
                    grid[y][x + 1] == notEdgeChar:
                isInside = not isInside
            if isInside:
                insideFlagGrid[y][x] = True
            # debug(f"{y} {x} {grid[y][x]} {isInside} {insideFlagGrid[y]}")

    # vertical scan
    for x in range(1, len(grid[0]) - 1):
        isInside = False
        for y in range(1, len(grid) - 1):
            if grid[y - 1][x] == notEdgeChar and \
                    grid[y][x] == edgeChar and \
                    grid[y + 1][x] == notEdgeChar:
                isInside = not isInside
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

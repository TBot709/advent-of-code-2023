from debug import debug
from day18.day18_common import Direction, Edge, Corner


def scancount(corners: list[Corner], vEdges: list[Edge]) -> str:
    minX = min(corner.x for corner in corners)
    maxX = max(corner.x for corner in corners)
    minY = min(corner.y for corner in corners)
    maxY = max(corner.y for corner in corners)

    def vEdgeComp(e):
        return (e.start.x, e.start.y)
    vEdges.sort(key=vEdgeComp)
    # debug(list(map(lambda e: str(e), vEdges)))

    def cornerComp(c):
        return (c.x, c.y)
    corners.sort(key=cornerComp)
    # debug(list(map(lambda c: str(c), corners)))

    def edgeCond(e, y, x):
        isStartAbove = e.start.y < e.end.y
        if isStartAbove:
            return e.start.y < y and \
                    e.end.y > y and \
                    e.start.x >= x
        else:
            return e.end.y < y and \
                    e.start.y > y and \
                    e.start.x >= x

    def cornerCond(c, y, x):
        return c.y == y and c.x >= x

    memoComboCounts = {}  # {hashOfCombo: count}

    def hashCombo(edges, corners):
        return hash(
                str(list(map(lambda e: str(e), edges))) +
                str(list(map(lambda c: str(c), corners))))
    
    def findNextChangeY(edges, corners, currentY):
        nextChangeY = maxY + 1
        for e in edges:
            isStartAbove = e.start.y < e.end.y
            if isStartAbove:
                if e.end.y > currentY and e.end.y < nextChangeY:
                    nextChangeY = e.end.y
            else:
                if e.start.y > currentY and e.start.y < nextChangeY:
                    nextChangeY = e.start.y
        for c in corners:
            if c.y > currentY and c.y < nextChangeY:
                nextChangeY = c.y
        return nextChangeY

    count = 0

    y = minY - 1
    while y < maxY + 1:
        debug(f"y:{y}, count:{count}")
        isInside = False
        prevCornerVertDir = Direction.UNKNOWN
        countAtStartOfLine = count

        x = minX - 1
        edgesOnLine = list(filter(lambda e: edgeCond(e, y, x), vEdges))
        # debug(list(map(lambda e: str(e), edgesOnLine)))
        cornersOnLine = list(filter(lambda c: cornerCond(c, y, x), corners))
        # debug(list(map(lambda e: str(e), cornersOnLine)))
        h = hashCombo(edgesOnLine, cornersOnLine)
        # debug(h)
        if h in memoComboCounts.keys():
            debug(f"REPEAT! {memoComboCounts[h]}")
            nextChangeY = findNextChangeY(vEdges, corners, y)
            dY = nextChangeY - y
            y = nextChangeY
            count += dY * memoComboCounts[h]
            continue

        while x < maxX + 1:
            # debug(f"y:{y}, x:{x}, count:{count}")
            def getVertDir(corner):
                return corner.tail if \
                    corner.tail == Direction.UP or \
                    corner.tail == Direction.DOWN else \
                    corner.head

            edge = next((e for e in vEdges if edgeCond(e, y, x)), None)
            corner = next((c for c in corners if cornerCond(c, y, x)), None)

            # debug(f"\tedge:{edge}, corner:{corner}")

            if edge is None and corner is None:
                # debug(f"\trow {y} complete")
                x = maxX
                break

            isEdgeFirst = edge is not None and \
                (corner is None or edge.start.x < corner.x)

            dx = 0

            if isEdgeFirst:
                dx = edge.start.x - x
                x = edge.start.x
                if isInside:
                    count += dx
                isInside = not isInside
                # debug(f"\t\tedge first, dx:{dx}, x:{x}, isInside:{isInside}")
            elif corner is not None:
                # debug("\t\tcorner first")
                dx = corner.x - x
                x = corner.x
                if prevCornerVertDir != Direction.UNKNOWN:
                    vertDir = getVertDir(corner)
                    # debug(f"\t\t\tend of edge, {prevCornerVertDir.value} {vertDir.value}")
                    if vertDir == prevCornerVertDir:
                        isInside = not isInside
                    prevCornerVertDir = Direction.UNKNOWN
                else:
                    prevCornerVertDir = getVertDir(corner)
                    # debug(f"\t\t\tstart of edge, {prevCornerVertDir.value}")
                    if isInside:
                        count += dx
                x = corner.x
                # debug(f"\t\tcorner first, dx:{dx}, x:{x}, isInside:{isInside}")

            x += 1

            # debug(f"\tcount:{count}, isInside:{isInside}, x:{x}")
        # EO while x

        isInside = False

        memoComboCounts[h] = count - countAtStartOfLine

        y += 1
    # EO while y

    return count

from debug import debug
from day18.day18_common import Direction, Edge, Corner


def scancount(corners: list[Corner], vEdges: list[Edge]) -> str:
    minX = min(corner.x for corner in corners)
    maxX = max(corner.x for corner in corners)
    minY = min(corner.y for corner in corners)
    maxY = max(corner.y for corner in corners)

    count = 0

    for y in range(minY - 1, maxY + 1):
        isInside = False
        prevCornerVertDir = Direction.UNKNOWN
        x = minX - 1
        while x < maxX + 1:
            debug(f"y:{y}, x:{x}")

            def edgeCond(e):
                return e.start.y < y and \
                    e.start.y > y and \
                    e.start.x > x

            def cornerCond(c):
                return c.y == y and c.x > x

            def getVertDir(corner):
                return corner.tail if \
                    corner.tail == Direction.UP or \
                    corner.tail == Direction.DOWN else \
                    corner.head

            edge = next((e for e in vEdges if edgeCond(e)), None)
            corner = next((c for c in corners if cornerCond(c)), None)

            if edge is None and corner is None:
                debug(f"\trow {y} complete")
                x = maxX
                break

            debug(f"\tedge:{edge}, corner:{corner}")

            isEdgeFirst = edge is not None and \
                (corner is None or edge.start.x < corner.x)

            dx = 0

            if isEdgeFirst:
                isInside = not isInside
                dx = edge.start.x - x
                x = edge.start.x
            elif corner is not None:
                if prevCornerVertDir != Direction.UNKNOWN:
                    vertDir = getVertDir(corner)
                    if vertDir != prevCornerVertDir:
                        isInside = not isInside
                    prevCornerVertDir = Direction.UNKNOWN
                else:  # new corner
                    if isInside:
                        dx = corner.x - x
                        x = corner.x
                    prevCornerVertDir = getVertDir(corner)

            if isInside:
                count += dx

            x += 1

            debug(f"\tcount:{count}, isInside:{isInside}")

        isInside = False

    return count

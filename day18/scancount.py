from debug import debug
from day18.day18_common import Direction, Edge, Corner


def scancount(corners: list[Corner], vEdges: list[Edge]) -> str:
    minX = min(corner.x for corner in corners)
    maxX = max(corner.x for corner in corners)
    minY = min(corner.y for corner in corners)
    maxY = max(corner.y for corner in corners)

    def vEdgeComp(e):
        return e.start.x
    vEdges.sort(key=vEdgeComp)
    # debug(list(map(lambda e: str(e), vEdges)))

    def cornerComp(c):
        return c.x
    corners.sort(key=cornerComp)
    # debug(list(map(lambda c: str(c), corners)))

    count = 0

    for y in range(minY - 1, maxY + 1):
        isInside = False
        prevCornerVertDir = Direction.UNKNOWN
        x = minX - 1
        while x < maxX + 1:
            debug(f"y:{y}, x:{x}, count:{count}")

            def edgeCond(e):
                isStartAbove = e.start.y < e.end.y
                if isStartAbove:
                    return e.start.y < y and \
                            e.end.y > y and \
                            e.start.x >= x
                else:
                    return e.end.y < y and \
                            e.start.y > y and \
                            e.start.x >= x

            def cornerCond(c):
                return c.y == y and c.x >= x

            def getVertDir(corner):
                return corner.tail if \
                    corner.tail == Direction.UP or \
                    corner.tail == Direction.DOWN else \
                    corner.head

            edge = next((e for e in vEdges if edgeCond(e)), None)
            corner = next((c for c in corners if cornerCond(c)), None)

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

        isInside = False

    return count


from day18.scanfill import scanfill
from debug import debug, setDebug

s = "" +\
    "###.###\n" +\
    "#.#.#.#\n" +\
    "#.###.#\n" +\
    "#.....#\n" +\
    "###.###\n" +\
    "..#.#..\n" +\
    "###.###\n" +\
    "#.....#\n" +\
    "#.###.#\n" +\
    "#.#.#.#\n" +\
    "###.###"

setDebug(True)
debug('\n' + s)
debug('\n' + scanfill(s, '#', '.'))

s = "" +\
    "#######\n" +\
    "#.....#\n" +\
    "#.#####\n" +\
    "#.#....\n" +\
    "#.#####\n" +\
    "#.....#\n" +\
    "###.###\n" +\
    "..#.#..\n" +\
    "###.###\n" +\
    "#.....#\n" +\
    "#.###.#\n" +\
    "#.#.#.#\n" +\
    "###.###"

debug('\n' + s)
debug('\n' + scanfill(s, '#', '.'))

s = "" +\
    "#######\n" +\
    "#.....#\n" +\
    "#.###.#\n" +\
    "#.#.#.#\n" +\
    "#.###.#\n" +\
    "#.....#\n" +\
    "###.###\n" +\
    "..#.#..\n" +\
    "###.###\n" +\
    "#.....#\n" +\
    "#.###.#\n" +\
    "#.#.#.#\n" +\
    "###.###"

debug('\n' + s)
debug('\n' + scanfill(s, '#', '.'))

s = "" +\
    ".........\n" +\
    "...###...\n" +\
    "...#.#...\n" +\
    "...#.#...\n" +\
    ".###.###.\n" +\
    ".#.....#.\n" +\
    ".###.###.\n" +\
    "...#.#...\n" +\
    "...#.#...\n" +\
    "...###...\n" +\
    "........."

debug('\n' + s)
debug('\n' + scanfill(s, '#', '.'))

s = "" +\
    ".........\n" +\
    "..####...\n" +\
    "..#..#...\n" +\
    "..#..###.\n" +\
    ".##....#.\n" +\
    ".#.....#.\n" +\
    ".#....##.\n" +\
    ".###..#..\n" +\
    "...#..#..\n" +\
    "...####..\n" +\
    "........."

debug('\n' + s)
debug('\n' + scanfill(s, '#', '.'))

s = "" + \
    "...................................................................\n" + \
    "............................########.........########..............\n" + \
    "............................#......#.........#......#..............\n" + \
    ".............######.........#......#.........#......#..............\n" + \
    ".............#....#.........#......#.........#......#..............\n" + \
    ".............#....#.........#......#.........#......#..............\n" + \
    ".......#######....#.........#......#.........#......#..............\n" + \
    ".......#..........#......####......#.........#......########.......\n" + \
    ".......#..........#......#.........#....######.............#.......\n" + \
    ".......#..........#......#.........#....#..................#.......\n" + \
    ".......#..........#......#.........#....#..................#.......\n" + \
    ".......#..........#......#.........#....#..................#.......\n" + \
    ".......#..........###....#.........#....#..................#####...\n" + \
    ".......#............#....#.........#....#......................#...\n" + \
    ".......#............#....#.........###..#......................#...\n" + \
    ".......#............#....#...........#..#......................#...\n" + \
    ".......#............#....#...........####......................#...\n" + \
    "...#####............######.....................................#...\n" + \
    "...#...........................................................#...\n" + \
    "...#................................................############...\n" + \
    "...#................................................#..............\n" + \
    "...#................................................#..............\n" + \
    "...#................................................#..............\n" + \
    "####................................................##############.\n" + \
    "#................................................................#.\n" + \
    "#................................................................#.\n" + \
    "####.............................................................#.\n" + \
    "...#.............................................................#.\n" + \
    "...#.............................................................#.\n" + \
    "...#.............................................................#.\n" + \
    "...#.............................................................#.\n" + \
    "...#.............................................................#.\n" + \
    "...#.............................................................#.\n" + \
    "...#.............................................................#.\n" + \
    "...###...........................................................#.\n" + \
    ".....#...........................................................#.\n" + \
    ".....#...........................................................#.\n" + \
    ".....#...........................................................#.\n" + \
    ".....#...........................................................#.\n" + \
    ".....#...........................................................#.\n" + \
    ".....#...........................................................#.\n" + \
    ".....######......................................................#.\n" + \
    "..........#......................................................#.\n" + \
    "..........#......................................................#.\n" + \
    "..........########################################################.\n" + \
    "...................................................................\n" + \
    "..................................................................."

debug('\n' + s)
debug('\n' + scanfill(s, '#', '.'))

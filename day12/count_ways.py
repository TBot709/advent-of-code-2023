from debug import debug

def remainingSpaceNeeded(clues: list[int]) -> int:
  r = 0
  for clue in clues:
    r += clue
  return r

def isFit(s: str, clueString: str) -> bool:
  isFit = True
  for i, c in enumerate(s):
    clueC = clueString[i]
    if c == '?':
      continue
    if c == clueC:
      continue
    isFit = False
    break
  return isFit

def count_ways(clues: list[int], row: str) -> int:
  cache = {}
  def _count_ways(clues: list[int], row: str, level=0):
    nonlocal cache
    if str(clues) + str(row) in cache:
        debug(f"hit! {clues} {row}")
        return cache[str(clues) + str(row)]
    count = 0
    clue = clues[0]
    windowStart = 0
    windowEnd = clue
    clueString = '#'*clue
    spaceOfOtherClues = sum(clues[1::]) if len(clues) > 1 else 0
    isFillsBefore = False 
    debug(f"\t_count_ways: {'| '*(level)}{clues} {row} {spaceOfOtherClues}")
    while windowEnd <= len(row) - spaceOfOtherClues and not isFillsBefore:
      debug(f"\t     isFit?: {'| '*(level)}{row[windowStart:windowEnd:]} {clueString} {isFit(row[windowStart:windowEnd:], clueString)}")
      isFillsBefore = any(char == '#' for char in row[0:windowStart:]) if windowStart != 0 else False
      isFillImmediatelyAfter = row[windowEnd] == '#' if windowEnd < len(row) else False
      if isFit(row[windowStart:windowEnd:], clueString) and \
            not isFillsBefore and \
            not isFillImmediatelyAfter: 
        # debug(f"\t           : {'| '*(level)}fit")
        nextLevel = level + 1
        nextClues = clues[1::]
        nextRow = row[windowEnd + 1::]
        if len(nextRow) > 0 and len(nextClues) > 0:
          count += _count_ways(nextClues, nextRow, nextLevel)
        else:
          if '#' in row[windowEnd + 1::]:
            debug(f"\t           : {'| '*(level)}invalid branch")
          else:
            if len(nextClues) == 0:
              debug(f"\t           : {'| '*(level)}valid branch")
              count += 1
      # else:
        # debug(f"\t           : {'| '*(level)}no fit")
      windowStart += 1
      windowEnd += 1
    debug(f"\t           : {'| '*(level)}end branch")
    cache[str(clues) + str(row)] = count
    return count
  count = _count_ways(clues, row)
  debug(f"final count: {count}")
  debug(f"cache:{cache}")
  return count

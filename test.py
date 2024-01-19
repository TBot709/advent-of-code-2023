import math

def nonogram_possibilities(clue, row_length, filled_positions, empty_positions):
    """
    Calculate the number of possibilities for a nonogram row given the row's clue,
    the total row length, positions of filled squares, and positions of guaranteed empty squares.

    Parameters:
    - clue: List of integers representing the cluster counts for the row.
    - row_length: The total length of the row.
    - filled_positions: List of integers representing positions of filled squares.
    - empty_positions: List of integers representing positions of guaranteed empty squares.

    Returns:
    - possibilities: Number of possibilities for the row.
    """

    # Calculate the number of squares already filled in (x'd)
    x_count = len(filled_positions)

    # Calculate the total number of squares needed based on the clue
    total_squares_needed = sum(clue)

    # Calculate the number of empty squares between and around clusters
    empty_squares = len(clue) - 1

    # Calculate the total number of squares in the row
    total_squares = total_squares_needed + empty_squares

    # Calculate the number of empty squares that still need to be filled
    remaining_empty_squares = total_squares - x_count

    # Adjust remaining empty squares based on the known filled and empty positions
    remaining_empty_squares -= len(empty_positions)
    remaining_empty_squares += len(filled_positions)

    # Check if there are enough squares left for the remaining clusters
    if remaining_empty_squares < 0:
        return 0  # Not enough space for the remaining clusters

    # Check if filled positions conflict with the clue
    for i in range(len(clue)):
        if filled_positions and filled_positions[-1] >= row_length - clue[i] + 1:
            return 0  # Not enough space for the current cluster

    # Use the combination formula to calculate the possibilities
    possibilities = math.comb(remaining_empty_squares, empty_squares)

    return possibilities

# Example usage:
clue = [1, 1, 3]
row_length = 14
filled_positions = [11, 12]
empty_positions = [0, 3, 4, 7, 8, 9, 13]
possibilities = nonogram_possibilities(clue, row_length, filled_positions, empty_positions)
print(f"Number of possibilities: {possibilities}")



# 00000000001111
# 01234567890123S
# .??..??...?##. [1, 1, 3]
print(f"{nonogram_possibilities([1,1,3], 14, [11,12], [0,3,4,7,8,9,13])}")

def getHasCycle(hashList: list[int], minCycleLength: int) -> bool:
    hashSet = set()
    for i in range(len(hashList)):
        if hashList[i] in hashSet:
            if i - hashList.index(hashList[i]) >= minCycleLength:
                return True
        else:
            hashSet.add(hashList[i])
    return False
print(getHasCycle([1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4],2))
print(getHasCycle([1,2,3,4,1,2,3,4,1,2,3,4,1,2,3,4],5))

def getIsCyclingValues(l: list) -> bool:
    n = len(l)
    for cycle_length in range(1, n):
        if n % cycle_length == 0:
            segment = l[:cycle_length]
            if all(l[i:i+cycle_length] == segment for i in range(cycle_length, n, cycle_length)):
                return True
    return False
print(f"getIsCyclingValues([1,2,3,1,2,3,1,2,3]) -> {getIsCyclingValues([1,2,3,1,2,3,1,2,3])}")
print(f"getIsCyclingValues([1,2,1,2,3,1,2,3]) -> {getIsCyclingValues([1,2,1,2,3,1,2,3])}")
print(f"getIsCyclingValues([1,2,1,2,1,2]) -> {getIsCyclingValues([1,2,1,2,1,2])}")
print(f"getIsCyclingValues([1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6]) -> {getIsCyclingValues([1,2,3,4,5,6,1,2,3,4,5,6,1,2,3,4,5,6])}")

# day 12 notes

## combinatronics count formula, python

In Python, you can use the `math.comb` function to calculate combinations. This function is available in Python 3.8 and later. Here's an example:

```python
from math import comb

# Calculate the number of ways to choose 3 items from a set of 10
num_combinations = comb(10, 3)
print(num_combinations)  # Outputs: 120
```

For older versions of Python, you can define your own function to calculate combinations:

```python
import operator as op
from functools import reduce

def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer // denom

# Calculate the number of ways to choose 3 items from a set of 10
num_combinations = ncr(10, 3)
print(num_combinations)  # Outputs: 120
```

This function uses the formula for combinations, which is $$\frac{n!}{r!(n-r)!}$$ where `n` is the total number of items, and `r` is the number of items to choose¹. 

If you want to generate all combinations of `r` elements from a list, you can use the `itertools.combinations` function:

```python
import itertools

# Generate all combinations of 2 letters from 'abcd'
combinations = list(itertools.combinations('abcd', 2))
print(combinations)  # Outputs: [('a', 'b'), ('a', 'c'), ('a', 'd'), ('b', 'c'), ('b', 'd'), ('c', 'd')]
```

This will return a list of tuples, where each tuple is a combination of `r` elements¹.

Source: Conversation with Bing, 2024-01-15
(1) Is there a math nCr function in Python? - Stack Overflow. https://stackoverflow.com/questions/4941753/is-there-a-math-ncr-function-in-python.
(2) python - How to count number of combinations? - Stack Overflow. https://stackoverflow.com/questions/21648015/how-to-count-number-of-combinations.
(3) python - counting combinations and permutations efficiently - Stack .... https://stackoverflow.com/questions/2096573/counting-combinations-and-permutations-efficiently.
(4) How to count amount of combinations in a python list. https://stackoverflow.com/questions/60331716/how-to-count-amount-of-combinations-in-a-python-list.
(5) github.com. https://github.com/UCEMA-QUANt/Quant-Finance/tree/dacc589f78a1c91b666a18d4f2ded549ceed49ca/Codigo%2Fopcion_europea_bin_c.py.
(6) github.com. https://github.com/professionaljesus/kattis/tree/e1f04986cf071af61beebaaa76b1a5681b054a35/ratings%2Fsol.py.
(7) github.com. https://github.com/paulojunqueira/Evolutionary_Algorithms/tree/86b1d163cf57ee38ea0e373288fc97146dc3c177/MOEAD-TCH%2FMOEAD.py.
(8) github.com. https://github.com/VenezianoMauro/ucema_quant_2021/tree/ac0bbf8578cadd06789dafd94eff0041456a8e5a/Derivados%2Foption_pricing.py.
(9) github.com. https://github.com/wqwangchn/zipline_chn/tree/e073b31f7ecc3575ed94e816d4c39a5e5c841c48/testing%2Fcore.py.

## I want to combine the count between two combinatronic counts, say, I choose 2 from 4 out of 3 separate bags, what is the total number of combinations from all bags

If you have 3 separate bags, each with 4 items, and you want to choose 2 items from each bag, you would calculate the number of combinations for each bag separately and then multiply the results together.

The number of ways to choose 2 items from a set of 4 is given by the combination formula $$C(n, r) = \frac{n!}{r!(n-r)!}$$ where `n` is the total number of items (4 in this case), and `r` is the number of items to choose (2 in this case)¹²³.

So, the number of combinations for one bag is $$C(4, 2) = \frac{4!}{2!(4-2)!} = 6$$

Since the choices from each bag are independent, you would multiply the number of combinations for each bag together to get the total number of combinations. So, for 3 bags, the total number of combinations would be $$6 * 6 * 6 = 216$$.

This means there are 216 different ways to choose 2 items from each of the 3 bags. 

Here is the Python code that calculates this:

```python
from math import comb

# Calculate the number of combinations for one bag
num_combinations_one_bag = comb(4, 2)

# Calculate the total number of combinations for three bags
total_combinations = num_combinations_one_bag ** 3

print(total_combinations)  # Outputs: 216
```

This code uses the `math.comb` function to calculate the number of combinations for one bag, and then raises this number to the power of 3 to get the total number of combinations for three bags¹.

Source: Conversation with Bing, 2024-01-15
(1) Combination Calculator (nCr Calculator). https://www.gigacalculator.com/calculators/combination-calculator.php.
(2) Combination Calculator (nCr) | Combinations Generator. https://www.omnicalculator.com/statistics/combination.
(3) Combinations Calculator (nCr). https://www.calculatorsoup.com/calculators/discretemathematics/combinations.php.
(4) SQL: Combine Select count (*) from multiple tables. https://stackoverflow.com/questions/1279569/sql-combine-select-count-from-multiple-tables.

## explain nonogram row possibility counter

``` python
def count_ways(clue, known):
    n = len(known)
    dp = [[0]*(len(clue)+1) for _ in range(n+1)]
    dp[0][0] = 1

    for i in range(n):
        for j in range(len(clue)+1):
            debug(f"{i} {j} {dp}")
            if known[i] != 1 and j > 0 and i+1 >= clue[j-1]:
                dp[i+1][j] += dp[i+1-clue[j-1]][j-1]
            if known[i] != 0:
                if j > 0 and i > 0 and i+1 > clue[j-1] and known[i-clue[j-1]] != 1:
                    dp[i+1][j] += dp[i-clue[j-1]][j-1]
                if j == 0 or known[i-1] == 1 or i+1 <= clue[j-1]:
                    dp[i+1][j] += dp[i][j]
    debug(f"{i} {j} {dp}")
    return dp[n][len(clue)]

# debug(count_ways([2,1], [2,2,0,2,1]))
debug(count_ways([1,1,3], [2,2,2,0,1,1,1]))
# debug(count_ways([1,1,3], [0,2,2,0,0,2,2,0,0,0,2,1,1]))
```

Sure, I'd be happy to explain this method in depth. This function `count_ways` is used to solve a problem related to Nonograms, which are picture logic puzzles in which cells in a grid must be colored or left blank according to numbers at the side of the grid to reveal a hidden picture.

Here's a breakdown of the function:

1. **Function Parameters**: The function takes two parameters - `clue` and `known`. `clue` is a list of integers representing the lengths of the blocks of filled cells in the row or column. `known` is a list of integers representing the known cells in the row or column, where 0 is a blank cell, 1 is a filled cell, and 2 is an unknown cell.

2. **Initialization**: The function first initializes a two-dimensional list `dp` with dimensions `(n+1) x (len(clue)+1)`, where `n` is the length of `known`. Each cell `dp[i][j]` will represent the number of ways to fill in the first `i` cells with `j` segments.

3. **Dynamic Programming**: The function then iterates over each cell in `known` and each segment in `clue`. For each cell and segment, it checks the following conditions:
    - If the current cell is not filled and there is a segment and enough cells left for the segment, it adds the number of ways to fill in the previous cells without the segment to the number of ways to fill in the current cells with the segment.
    - If the current cell is not blank, it checks two more conditions:
        - If there is a segment and a previous cell and enough cells left for the segment and the previous cell of the segment is not filled, it adds the number of ways to fill in the previous cells of the segment without the segment to the number of ways to fill in the current cells with the segment.
        - If there is no segment or the previous cell is filled or not enough cells left for the segment, it adds the number of ways to fill in the previous cells with the segment to the number of ways to fill in the current cells with the segment.

4. **Return Value**: Finally, the function returns the number of ways to fill in all cells with all segments, which is stored in `dp[n][len(clue)]`.

This function uses dynamic programming to efficiently calculate the number of ways to fill in the cells. It breaks down the problem into smaller subproblems (filling in the first `i` cells with `j` segments), and uses the solutions to these subproblems to build up the solution to the original problem. The time complexity of this function is O(n^2 * m), where n is the number of cells and m is the number of segments. The space complexity is O(n * m), which is the size of the `dp` table. 

I hope this helps! If you have any more questions, feel free to ask. 😊
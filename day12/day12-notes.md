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
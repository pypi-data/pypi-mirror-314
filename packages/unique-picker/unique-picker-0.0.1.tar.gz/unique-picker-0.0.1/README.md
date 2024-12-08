# Unique Picker

Unique Picker is a Python package that allows you to randomly select an item from a list without repeating any item until all items in the list are covered. Once all items are selected, the list is reshuffled, and the process continues.

## Installation
You can install the package using pip:
```bash
pip install unique-picker
```

# Usage
Import the Package
```bash
import uniquePicker
```
# How to Use
Use the choice function to randomly select an item from a list:
```bash
data_list = [1, 2, 3, 4, 5]
for _ in range(10):
    print(uniquePicker.choice(data_list))

```
# Output
The choice function ensures that:
- No item is repeated until all items in the list are selected.
- After all items are used, the list is reshuffled for the next cycle.

Example Output:

```bash
css


3
5
1
4
2
(all items reshuffled)
4
3
2
5
1

```

# Features
- Random selection without immediate repetition.
- Automatic reshuffling after all items are covered.
- Easy-to-use API, just like Python’s random.choice.

# Code Example
Here’s a complete working example:
```bash
import uniquePicker

# Define your list
data_list = ['apple', 'banana', 'cherry', 'date', 'elderberry']

# Select items
print("Random selections without repeats:")
for _ in range(10):
    print(uniquePicker.choice(data_list))

```
# How It Works
- The unique_picker.choice function internally uses a class to manage the list and its current state.
- It shuffles the list when all items are exhausted, ensuring fair and unique selection in cycles.

# License
This package is distributed under the MIT License. See the LICENSE file for details.
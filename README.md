# leetcode-problems
Leetcode questions for interview preparation. Questions taken from Neetcode 150. 

## My Notes 

### Dictionaries / Hashmaps in Python
- ex. {1: "hello", 2: "world"}, 1 is the key and "hello" is the value
- Storing: `dict[key] = value`
- Retrieving: `print(dict[key])`. O(1) lookup 
- Searching: `if key in dict` (always query by key)
- Keys have to be unique

### Sets 
- Sets are like dictionaries in Python but with *KEYS ONLY*.
- No duplicate keys
- No values, just yes or no
- O(1) lookup 
- Converting a list to a set removes duplicates
- Define a set: set()
- Adding values: set.add(5)

### In-place method 
- Usable only for values in range [1, n]

### Useful algorithms 
- In-place method
- Sum of all numbers from 0 to n: n * (n + 1) / 2
- Boyer-Moore Voting Algorithm 

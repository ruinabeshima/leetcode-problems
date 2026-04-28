# leetcode-problems
Leetcode questions for interview preparation

## Topics 

### Arrays, Hashmaps 
- 1
- 121
- 169 (Boyer-Moore Voting Algorithm)
- 217
- 242
- 268 (Sum Subtraction)
- 383
- 387
- 389 (Sum Subtraction) 
- 448 (In-place method)
- 202 (Floyd's Cycle Detection)
- 349
- 350

### Two Pointers 
- 125 Valid Palidrome
- 283 Move Zeroes

## My Notes 

### Useful algorithms 
- In-place method (448 Find all numbers disappeared in an array) 
- Sum of all numbers from 0 to n: n * (n + 1) / 2 (268 Missing Number) 
- Boyer-Moore Voting Algorithm (169 Majority Element)
- Floyd's Cycle Detection (202 Happy Number) 

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

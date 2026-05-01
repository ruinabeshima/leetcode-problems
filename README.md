# leetcode-problems
Leetcode questions for interview preparation
https://docs.google.com/spreadsheets/d/1hnJ6xICrjj6thIi0UvM6driOE8BCW4pmDIwp6Ane8uo/edit?gid=0#gid=0

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

# MatchFinder
 _A Python package that finds your string's soulmates- quickly, effortlessly, and with style._
 
Welcome to **_MatchFinder_**! It's your go-to tool for finding similar strings in a list. Whether you're matching names, fixing typos, or building a search engine, MatchFinder makes it easy **no extra libraries needed, just simple and powerful Python!**\
<sub><sub>Developed primarily for fun and learning purposes.</sub></sub>

## Why MatchFinder?
**1. Simple**: No unnecessary imports and install - just good old Python.\
**2. Customizable**: Choose your output style - csv, JSON or text, with or without scores.\
**3. Speed**: Optimized to return results quickly, even for large datasets.\
**4. Fun**: Because boring tools are for boring developers.
## Installation  

You can install MatchFinder directly from PyPI:

```bash
pip install MatchFinder
```
## Usage
Here's how to get started with MatchFinder:

### Import the package
```python
from MatchFinder import get_similar
```
### Example 1: Text Output

```python

input_str = "Snake"  # Not exactly your ex, but close enough?
match_list = ["sneaky", "snake", "Snakeskin", "Slither", "your ex", "anaconda"]
n= 3

matches = get_similar(input_str, match_list, n,output_format="text")
print(matches)


```
### output 
```text
['Match: snake', 'Match: sneaky', 'Match: Snakeskin']
```


### Example 2: JSON Output
```python
# Get similar strings in JSON format, including similarity scores
result = get_similar(input_str, match_list, n=2, include_score=True, output_format="json")
print(result)

```
### output
```json
[
  {'match': 'snakes', 'score': 0.83},
  {'match': 'snack', 'score': 0.6}
]
```
### Example 3: Customizing Parameters
You can customize the Parameters


 **n** - Maximum number of matches to return.(default 1)\
**output_format** - Desired output format ("text" or "json" or "csv")\
**include_score** - Whether to include similarity scores.\
**case_insensitive** - Ignores case sensitivity of input text and match_list
```python
# Change the number of matches and disable scores
result = get_similar("Python", ["Pithon", "Phyton", "Ruby", "Pytan"], n=2, include_score=False, output_format="text")
print(result)
```
### output
```text
['Match: Pithon', 'Match: Phyton']
```

## Behind the Scenes 
MatchFinder uses a custom similarity algorithm to calculate how "close" two strings are.\
**It's like Tinder for strings but with way less drama.** 


## Contributions
Feel free to fork this project, add cool new features, or just drop by to say hi! 

## License
This project is licensed under the MIT License. 

**<ins>Get Matching Now!</ins>\
Install MatchFinder today and make your strings feel a little less lonely.**
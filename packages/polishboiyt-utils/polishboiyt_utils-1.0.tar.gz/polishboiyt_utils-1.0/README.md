# polishboiyt-utils

A library that makes your lives less miserable by adding useful stuff that took me longer than I thought.

To install, use `pip install polishboiyt-utils`.

## Like?
Text stuff!

stdout (Standard Output) stuff (basically `print()` but with more features)!

## Examples

### Text
Creating a Text() object with a string
```python
from polishboiyt_utils import Text

text = Text("Your text goes here")
```
Creating a Text() object with a file
```python
from polishboiyt_utils import Text

text = Text(file="example.txt")

# example.txt:
# Your file contents go here
```
Reversing text
```python
from polishboiyt_utils import Text

text = Text("Hello, World!")
print(text.reverse())
# Outputs "!dlroW ,olleH"
```
Altering text case.
```python
from polishboiyt_utils import Text

text = Text("Hello, World!")
print(text.alter_case())
# Outputs "hElLo, WoRlD!"
```
Shuffling the text
```python
from polishboiyt_utils import Text

text = Text("Hello, World!")

print(text.shuffle())
# Outputs something like "!rleHodl oW," (random every time!)
```
Removing duplicate spaces
```python
from polishboiyt_utils import Text

text = Text("Example text with    spaces.")
print(text.trim_spaces())
# Outputs "Example text with spaces."
```
Checking if the text is a palindrome
```python
from polishboiyt_utils import Text

palindrome = Text("racecar")
print(palindrome.is_palindrome())
# Outputs True
not_palindrome = Text("hello")
print(not_palindrome.is_palindrome())
# Outputs False
```
Removing HTML tags ("`<code><p>Example</p></code>`")
```python
from polishboiyt_utils import Text

html = Text("<p>Hello, World!</p>")
print(html.remove_html())
# Outputs "Hello, World!"
```
### stdout
Typewriting text.
```python
from polishboiyt_utils import stdout
stdout.typewrite("Your text goes here", interval=0.075)
```
Logging text
```python
from polishboiyt_utils import stdout
stdout.log(stdout.LogTypes.ERR, "Hello, World!")
```
Blinking text
```python
from polishboiyt_utils import stdout
stdout.blink_text("Hello, World!", 5, 0.5)
```
Creating a progress bar
```python
from polishboiyt_utils import stdout
maximum = 100
items = range(maximum)
total_items = len(items)

stdout.progress_bar(items, total_items, progress_interval=0.2)
# Do actions after..
print("Complete!")
```

# Adding more soon. (when i feel like it)
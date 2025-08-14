# lkj

Lightweight Kit Jumpstart. A place for useful python utils built only with pure python.

To install:	```pip install lkj```

[Documentation](https://i2mint.github.io/lkj)

Note: None of the tools here require anything else but pure python.
Additionally, things are organized in such a way that these can be 
easily copy-pasted into other projects. 
That is, modules are all self contained (so can easily be copy-paste-vendored 
(do be nice and mention the source!))
Further, many functions will contain their own imports: Those functions can even be 
copy-paste-vendored by just copying the function body.

# Examples of utils

## Find and replace

`FindReplaceTool` is a general-purpose find-and-replace tool that can treat the input text as a continuous sequence of characters, 
even if operations such as viewing context are performed line by line.

The basic usage is 

```python
FindReplaceTool("apple banana apple").find_and_print_matches(r'apple')
```
    
    Match 0 (around line 1):
    apple banana apple
    ^^^^^
    ----------------------------------------
    Match 1 (around line 1):
    apple banana apple
                 ^^^^^
    ----------------------------------------

```python
FindReplaceTool("apple banana apple").find_and_replace(r'apple', "orange")
```

    'orange banana orange'

[See more examples in documentation](https://i2mint.github.io/lkj/module_docs/lkj/strings.html#lkj.strings.FindReplaceTool)

[See here a example of how I used this to edit my CI yamls](https://github.com/i2mint/lkj/discussions/4#discussioncomment-12104547)

## loggers

### clog

Conditional log

```python
>>> clog(False, "logging this")
>>> clog(True, "logging this")
logging this
```

One common usage is when there's a verbose flag that allows the user to specify
whether they want to log or not. Instead of having to litter your code with
`if verbose:` statements you can just do this:

```python
>>> verbose = True  # say versbose is True
>>> _clog = clog(verbose)  # makes a clog with a fixed condition
>>> _clog("logging this")
logging this
```

You can also choose a different log function.
Usually you'd want to use a logger object from the logging module,
but for this example we'll just use `print` with some modification:

```python
>>> _clog = clog(verbose, log_func=lambda x: print(f"hello {x}"))
>>> _clog("logging this")
hello logging this
```

### print_with_timestamp

Prints with a timestamp and optional refresh.
- input: message, and possibly args (to be placed in the message string, sprintf-style
- output: Displays the time (HH:MM:SS), and the message
- use: To be able to track processes (and the time they take)

```python
>>> print_with_timestamp('processing element X')
(29)09:56:36 - processing element X
```

### return_error_info_on_error

Decorator that returns traceback and local variables on error.

This decorator is useful for debugging. It will catch any exceptions that occur
in the decorated function, and return an ErrorInfo object with the traceback and
local variables at the time of the error.
- `func`: The function to decorate.
- `caught_error_types`: The types of errors to catch.
- `error_info_processor`: A function that processes the ErrorInfo object.

Tip: To parametrize this decorator, you can use a functools.partial function.

Tip: You can have your error_info_processor persist the error info to a file or
database, or send it to a logging service.

```python
>>> from lkj import return_error_info_on_error, ErrorInfo
>>> @return_error_info_on_error
... def foo(x, y=2):
...     return x / y
...
>>> t = foo(1, 2)
>>> assert t == 0.5
>>> t = foo(1, y=0)
Exiting from foo with error: division by zero
>>> if isinstance(t, ErrorInfo):
...     assert isinstance(t.error, ZeroDivisionError)
...     hasattr(t, 'traceback')
...     assert t.locals['args'] == (1,)
...     assert t.locals['kwargs'] == {'y': 0}
```

## Miscellaneous

### chunker

Chunk an iterable into non-overlapping chunks of size chk_size.

```python
chunker(a, chk_size, *, include_tail=True)
```

```python
>>> from lkj import chunker
>>> list(chunker(range(8), 3))
[(0, 1, 2), (3, 4, 5), (6, 7)]
>>> list(chunker(range(8), 3, include_tail=False))
[(0, 1, 2), (3, 4, 5)]
```

### import_object

Import and return an object from a dot string path.

```python
import_object(dot_path: str)
```

```python 
>>> f = import_object('os.path.join')
>>> from os.path import join
>>> f is join
True
```

## Pretty Printing Lists

The `print_list` function provides flexible, human-friendly ways to display lists and collections. It supports multiple display styles and can be used in several ways.

### Basic Usage

```python
from lkj.strings import print_list

items = ['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig']

# Different display styles
print_list(items, style='wrapped')      # Automatic line wrapping
print_list(items, style='columns')      # Column format
print_list(items, style='numbered')     # Numbered list
print_list(items, style='bullet')       # Bullet points
print_list(items, style='compact')      # All on one line
print_list(items, style='table')        # Table format
```

### Direct Usage with Customization

```python
# Customize width, separators, and formatting
print_list(items, style='wrapped', max_width=40, sep=' | ')
print_list(items, style='columns', items_per_line=3)
print_list(items, style='numbered', line_prefix='  ')
print_list(items, style='bullet', show_count=False)

# Return string instead of printing
result = print_list(items, style='numbered', print_func=None)
print(result)
```

### Partial Function Factory

When you don't specify the `items` parameter, `print_list` returns a partial function that you can reuse:

```python
# Create specialized printers
numbered_printer = print_list(style='numbered', show_count=False)
bullet_printer = print_list(style='bullet', print_func=None)
compact_printer = print_list(style='compact', max_width=60)

# Reuse with different data
numbered_printer(['a', 'b', 'c'])        # Prints: 1. a\n2. b\n3. c
result = bullet_printer(['x', 'y', 'z']) # Returns: '• x\n• y\n• z'
compact_printer(['item1', 'item2'])      # Prints: item1, item2
```

### Convenience Methods

The `print_list` object provides convenient pre-configured methods:

```python
# Quick access to common styles
print_list.compact(items)    # Compact format, no count
print_list.wrapped(items)    # Wrapped format, no count  
print_list.columns(items)    # Column format, no count
print_list.numbered(items)   # Numbered format, no count
print_list.bullets(items)    # Bullet format, no count

# Specialized methods
print_list.as_table(data)    # Table with headers
print_list.summary(items)    # Summary for long lists
```

### Advanced Examples

```python
# Table with custom data
data = [['Name', 'Age', 'City'], ['Alice', 25, 'NYC'], ['Bob', 30, 'LA']]
print_list.as_table(data)

# Summary for long lists
long_list = list(range(100))
print_list.summary(long_list, max_items=6)  # Shows: [0, 1, 2, ..., 97, 98, 99]

# Custom print function (e.g., for logging)
def my_logger(msg):
    print(f"[LOG] {msg}")

print_list(items, style='bullet', print_func=my_logger)

# Combine partial with custom parameters
custom_compact = print_list(style='compact', sep=' | ')
custom_compact(items)  # Prints: apple | banana | cherry | date | elderberry | fig
```

### Key Features

- **Multiple Styles**: `wrapped`, `columns`, `numbered`, `bullet`, `compact`, `table`
- **Flexible Output**: Print directly or return strings with `print_func=None`
- **Partial Functions**: Create reusable printers with pre-configured settings
- **Customizable**: Control width, separators, line prefixes, and more
- **Type Safe**: Uses `Literal` types for style validation
- **Self-Contained**: No external dependencies beyond Python standard library

The `print_list` function is perfect for debugging, logging, user interfaces, and any situation where you need to display lists in a readable format.

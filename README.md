# lkj

Lightweight Kit Jumpstart. A place for useful python utils built only with pure python.

To install:	```pip install lkj```

None of the tools here require anything else but pure python.
Additionally, things are organized in such a way that these can be 
easily copy-pasted into other projects. 
That is, modules are all self contained (so can easily be copy-paste-vendored 
(do be nice and mention the source!))
Further, many functions will contain their own imports: Those functions can even be 
copy-paste-vendored by just copying the function body.


# Examples of utils

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

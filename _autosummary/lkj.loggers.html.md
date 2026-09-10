# lkj.loggers

Utils for logging.

### Functions

| [`clog`](#lkj.loggers.clog)(condition, \*args[, log_func])             | Conditional log                                                                                                             |
|--------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| `dflt_error_info_processor`(error_info, \*[, ...])                                               |                                                                                                                             |
| [`instance_flag_is_set`](#lkj.loggers.instance_flag_is_set)(func, args, kwargs[, ...]) | Check if the log flag is set to True in the instance.                                                                       |
| [`log_calls`](#lkj.loggers.log_calls)([func, logger, ingress_msg, ...])     | Decorator that adds logging before and after the function's call.                                                           |
| [`print_progress`](#lkj.loggers.print_progress)(msg, \*[, refresh, ...])         | Prints with a timestamp and optional refresh.                                                                               |
| [`print_with_timestamp`](#lkj.loggers.print_with_timestamp)(msg, \*[, refresh, ...])   | Prints with a timestamp and optional refresh.                                                                               |
| [`return_error_info_on_error`](#lkj.loggers.return_error_info_on_error)(func, \*[, ...])     | Decorator that returns traceback and local variables on error.                                                              |
| [`wrap_text_with_exact_spacing`](#lkj.loggers.wrap_text_with_exact_spacing)(text, \*[, ...])   | Prints a string with word-wrapping to a maximum line length, while preserving all existing newlines exactly as they appear. |
| [`wrapped_print`](#lkj.loggers.wrapped_print)(items[, sep, max_width, ...])     | Prints a string or list ensuring the total line width does not exceed `max_width`.                                          |

### Classes

| [`CallOnError`](#lkj.loggers.CallOnError)(\*exceptions[, on_error])     | An extension of the suppress context manager that enables the user to issue a warning message when an import error occurs.   |
|--------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------|
| [`ErrorInfo`](#lkj.loggers.ErrorInfo)(func, error, traceback, locals) |                                                                                                                              |

### *class* lkj.loggers.CallOnError(\*exceptions, on_error=<built-in function print>)

Bases: `suppress`

An extension of the suppress context manager that enables the user to issue a warning
message when an import error occurs.

```pycon
>>> warn_about_import_errors = CallOnError(ImportError, on_error=lambda err: print(f"Warning: {err}"))
>>> with warn_about_import_errors:
...     import this_package_surely_does_not_exist
Warning: No module named 'this_package_surely_does_not_exist'
>>> with warn_about_import_errors:
...     from os.this_module_does_not_exist import this_function_does_not_exist
Warning: No module named 'os.this_module_does_not_exist'; 'os' is not a package
```

### *class* lkj.loggers.ErrorInfo(func, error, traceback, locals)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

### lkj.loggers.clog(condition, \*args, log_func=<built-in function print>, \*\*kwargs)

Conditional log

```pycon
>>> clog(False, "logging this")
>>> clog(True, "logging this")
logging this
```

One common usage is when there’s a verbose flag that allows the user to specify
whether they want to log or not. Instead of having to litter your code with
`if verbose:` statements you can just do this:

```pycon
>>> verbose = True  # say versbose is True
>>> _clog = clog(verbose)  # makes a clog with a fixed condition
>>> _clog("logging this")
logging this
```

You can also choose a different log function.
Usually you’d want to use a logger object from the logging module,
but for this example we’ll just use `print` with some modification:

```pycon
>>> _clog = clog(verbose, log_func=lambda x: print(f"hello {x}"))
>>> _clog("logging this")
hello logging this
```

### lkj.loggers.instance_flag_is_set(func, args, kwargs, flag_attr='verbose')

Check if the log flag is set to True in the instance.

### lkj.loggers.log_calls(func=None, \*, logger=<built-in function print>, ingress_msg=<function \_calling_name>, egress_msg=<function \_done_calling_name>, func_name=operator.attrgetter('_\_name_\_'), log_condition=<function \_always_log>)

Decorator that adds logging before and after the function’s call.

* **Parameters:**
  * **logger** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`str`](https://docs.python.org/3/library/stdtypes.html#str)], [`None`](https://docs.python.org/3/library/constants.html#None)]) – The logger function to use. Default is print.
  * **ingress_msg** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`str`](https://docs.python.org/3/library/stdtypes.html#str), [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple), [`dict`](https://docs.python.org/3/library/stdtypes.html#dict)], [`str`](https://docs.python.org/3/library/stdtypes.html#str)]) – The message to log before calling the function.
    If it returns None, no message is logged.
    Default is “Calling {name}…” where name is the name of the function.
  * **egress_msg** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`str`](https://docs.python.org/3/library/stdtypes.html#str), [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple), [`dict`](https://docs.python.org/3/library/stdtypes.html#dict), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)], [`str`](https://docs.python.org/3/library/stdtypes.html#str)]) – The message to log after the function call.
    If it returns None, no message is logged.
    Default is “…. Done”.
  * **func_name** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)], [`str`](https://docs.python.org/3/library/stdtypes.html#str)]) – The function to use to get the function’s name.
  * **log_condition** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable), [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple), [`dict`](https://docs.python.org/3/library/stdtypes.html#dict)], [`bool`](https://docs.python.org/3/library/functions.html#bool)]) – The condition for logging.
    Should be a callable that takes a function, args, and kwargs,
    and return a bool. If log_condition returns False, no logging is done.
    Default is \_always_log.
* **Return type:**
  [*Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)

Tips:

```default
Use `logger=print_with_timestamp` to get timestamps in your logs.
Use `lambda *args: None` as the ingress_msg or egress_msg to suppress logging.
Use `logger=lambda x: None` to suppress all logging.
```

* **Return type:**
  [`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)
* **Returns:**
  The decorated function.

### Example

```pycon
>>> @log_calls
... def add(a, b):
...     return a + b
...
>>> add(2, 3)
Calling add...
.... Done calling add
5
```

```pycon
>>> @log_calls(
...     logger=lambda x: print(f"LOG: {x}"),
...     ingress_msg=lambda name, *args: f"Start {name}!",
...     egress_msg=lambda *args: "End"
... )
... def multiply(a, b):
...     return a * b
...
>>> multiply(2, 3)
LOG: Start multiply!
LOG: End
6
```

Sometimes, you want to dynamically control whether to log or not.
This is what the `log_condition` parameter is for.
One common use case is to log only if a flag is set in an instance.
Since this is a common use case, we provide the `log_calls.instance_flag_is_set`
helper function for this. You can use partial to set the flag attribute:

```pycon
>>> import functools
>>> log_if_verbose_set_to_true = functools.partial(
...     log_calls.instance_flag_is_set, flag_attr='verbose'
... )
```

Now if you have a class with a `verbose` attribute, you can use this helper function
to log only if `verbose` is set:

```pycon
>>> class MyClass:
...     def __init__(self, verbose=False):
...         self.verbose = verbose
...
...     @log_calls(log_condition=log_if_verbose_set_to_true)
...     def foo(self):
...         print("Executing foo")
...
>>> # Example usage
>>> obj = MyClass(verbose=True)
>>> obj.foo()  # This will log
Calling foo...
Executing foo
.... Done calling foo
```

But if verbose is set to `False`, no logging will be done:

```pycon
>>> obj = MyClass(verbose=False)
>>> obj.foo()  # This will not log
Executing foo
```

### lkj.loggers.print_progress(msg, \*, refresh=None, display_time=True, print_func=<built-in function print>)

Prints with a timestamp and optional refresh.

input: message, and possibly args (to be placed in the message string, sprintf-style

output: Displays the time (HH:MM:SS), and the message

use: To be able to track processes (and the time they take)

### lkj.loggers.print_with_timestamp(msg, \*, refresh=None, display_time=True, print_func=<built-in function print>)

Prints with a timestamp and optional refresh.

input: message, and possibly args (to be placed in the message string, sprintf-style

output: Displays the time (HH:MM:SS), and the message

use: To be able to track processes (and the time they take)

### lkj.loggers.return_error_info_on_error(func, \*, caught_error_types=(<class 'Exception'>, ), error_info_processor=<function dflt_error_info_processor>)

Decorator that returns traceback and local variables on error.

This decorator is useful for debugging. It will catch any exceptions that occur
in the decorated function, and return an ErrorInfo object with the traceback and
local variables at the time of the error.

* **Parameters:**
  * **func** – The function to decorate.
  * **caught_error_types** ([`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple)[[`Exception`](https://docs.python.org/3/library/exceptions.html#Exception)]) – The types of errors to catch.
  * **error_info_processor** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`ErrorInfo`](#lkj.loggers.ErrorInfo)], [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]) – A function that processes the ErrorInfo object.

#### TIP
To parametrize this decorator, you can use a functools.partial function.

#### TIP
You can have your error_info_processor persist the error info to a file or
database, or send it to a logging service.

```pycon
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

### lkj.loggers.wrap_text_with_exact_spacing(text, \*, max_width=80, print_func=<built-in function print>, line_prefix='')

Prints a string with word-wrapping to a maximum line length, while preserving all existing newlines
exactly as they appear.

### Args

- text (str): The text to wrap and print.
- max_width (int): The maximum width of each line (default is 88).

### lkj.loggers.wrapped_print(items, sep=', ', max_width=80, \*, print_func=<built-in function print>, line_prefix='')

Prints a string or list ensuring the total line width does not exceed `max_width`.

If adding a new item would exceed this width, it starts a new line.

* **Parameters:**
  * **items** ([`str`](https://docs.python.org/3/library/stdtypes.html#str) | [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)) – String or list of items to print.
  * **sep** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The separator to use between items.
  * **max_width** ([*int*](https://docs.python.org/3/library/functions.html#int)) – The maximum width of each line. Default is 80.

### Example

```pycon
>>> items = [
...     "item1", "item2", "item3", "item4", "item5", "item6", "item7", "item8",
...     "item9", "item10"
... ]
>>> sep = ", "
>>> wrapped_print(items, sep, max_width=30)
item1, item2, item3, item4,
item5, item6, item7, item8,
item9, item10
```

```pycon
>>> items = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]
>>> sep = " - "
>>> wrapped_print(items, sep, max_width=10)
a - b - c
- d - e -
f - g - h
- i - j
```

Note that you have control over the `print_func`.
This, for example, allows you to just return the string instead of printing it.

```pycon
>>> wrapped_print(items, sep, max_width=10, print_func=lambda x: x)
'a - b - c\n- d - e -\nf - g - h\n- i - j'
```

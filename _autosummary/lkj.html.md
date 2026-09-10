# lkj

Lightweight Kit Jumpstart

### Functions

| [`add_as_attribute_of`](#lkj.add_as_attribute_of)(obj[, name])     | Decorator that adds a function as an attribute of a container object `obj`.   |
|---------------------------------------------------------------------------------------|-------------------------------------------------------------------------------|
| [`add_attr`](#lkj.add_attr)(attr_name[, attr_val, obj]) | Add an attribute to an object.                                                |
| `ddir`(obj)                                                                           |                                                                               |
| [`get_caller_package_name`](#lkj.get_caller_package_name)([default])   | Return package name of caller                                                 |
| [`user_machine_id`](#lkj.user_machine_id)()                    | Get an ID for the current computer/user that calls this function.             |

### lkj.add_as_attribute_of(obj, name=None)

Decorator that adds a function as an attribute of a container object `obj`.

If no `name` is given, the `__name__` of the function will be used, with a
leading underscore removed. This is useful for adding helper functions to main
“container” functions without polluting the namespace of the module, at least
from the point of view of imports and tab completion.

```pycon
>>> def foo():
...    pass
>>>
>>> @add_as_attribute_of(foo)
... def helper():
...    pass
>>> hasattr(foo, 'helper')
True
>>> callable(foo.helper)
True
```

In reality, any object that has a `__name__` can be added to the attribute of
`obj`, but the intention is to add helper functions to main “container” functions.

Note that if the name of the function starts with an underscore, it will be removed
before adding it as an attribute of `obj`.

```pycon
>>> @add_as_attribute_of(foo)
... def _helper():
...    pass
>>> hasattr(foo, 'helper')
True
```

This is useful for adding helper functions to main “container” functions without
polluting the namespace of the module, at least from the point of view of imports
and tab completion. But if you really want to add a function with a leading
underscore, you can do so by specifying the name explicitly:

```pycon
>>> @add_as_attribute_of(foo, name='_helper')
... def _helper():
...    pass
>>> hasattr(foo, '_helper')
True
```

Of course, you can give any name you want to the attribute:

```pycon
>>> @add_as_attribute_of(foo, name='bar')
... def _helper():
...    pass
>>> hasattr(foo, 'bar')
True
```

* **Parameters:**
  * **obj** – The object to which the function will be added as an attribute
  * **name** – The name of the attribute to add the function to. If not given, the

### lkj.add_attr(attr_name, attr_val=None, obj=None)

Add an attribute to an object.

If no object is provided, return a partial function that takes an object as its
argument.
If no attribute value is provided, return a partial function that takes an
attribute value as its argument.
If no object or attribute value is provided, return a partial function that takes
both an object and an attribute value as its arguments.
If all arguments are provided, add the attribute to the object and return the
object.

* **Parameters:**
  * **attr_name** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) – The name of the attribute to add.
  * **attr_val** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) – The value of the attribute to add.
  * **obj** – The object to which to add the attribute.
* **Returns:**
  The object with the attribute added, or a partial function that takes an
  object and/or an attribute value as its argument(s).

```pycon
>>> def generic_func(*args, **kwargs):
...     return args, kwargs
...
>>> generic_func.__name__
'generic_func'
>>>
>>> _ = add_attr('__name__', 'my_func', generic_func);
>>> generic_func.__name__
'my_func'
>>>
>>>
>>> add_name = add_attr('__name__')
>>> add_doc = add_attr('__doc__')
>>>
>>> @add_name('my_func')
... @add_doc('This is my function.')
... def f(*args, **kwargs):
...     return args, kwargs
...
>>> f.__name__
'my_func'
>>> f.__doc__
'This is my function.'
```

### lkj.get_caller_package_name(default=None)

Return package name of caller

See: [https://github.com/i2mint/i2mint/issues/1#issuecomment-1479416085](https://github.com/i2mint/i2mint/issues/1#issuecomment-1479416085)

### lkj.user_machine_id()

Get an ID for the current computer/user that calls this function.

### Modules

| [`chunking`](lkj.chunking.html.md#module-lkj.chunking)   | Tools for chunking (segumentation, batching, slicing, etc.)   |
|---------------------------------------------------------------------------------|---------------------------------------------------------------|
| [`dicts`](lkj.dicts.html.md#module-lkj.dicts)         | Tools for working with dictionaries (and other Mappings).     |
| [`filesys`](lkj.filesys.html.md#module-lkj.filesys)     | File system utils                                             |
| [`funcs`](lkj.funcs.html.md#module-lkj.funcs)         | Tools for working with functions.                             |
| [`importing`](lkj.importing.html.md#module-lkj.importing) | Tools for importing                                           |
| [`iterables`](lkj.iterables.html.md#module-lkj.iterables) | Tools with iterables (dicts, lists, tuples, sets, etc.).      |
| [`loggers`](lkj.loggers.html.md#module-lkj.loggers)     | Utils for logging.                                            |
| [`misc`](lkj.misc.html.md#module-lkj.misc)           | Miscellaneous tools.                                          |
| [`strings`](lkj.strings.html.md#module-lkj.strings)     | String Utilities Module                                       |

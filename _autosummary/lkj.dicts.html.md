# lkj.dicts

Tools for working with dictionaries (and other Mappings).

If you are looking for more, check out the `lkj.iterables` module too
(after all, dicts are iterables).

### Functions

| [`compare_field_values`](#lkj.dicts.compare_field_values)(dict1, dict2, \*[, ...])     | Compare two dictionaries' values field by field                                                                                     |
|----------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|
| [`exclusive_subdict`](#lkj.dicts.exclusive_subdict)(d, exclude)                     | Returns a new dictionary with only the keys not in `exclude`.                                                                       |
| [`inclusive_subdict`](#lkj.dicts.inclusive_subdict)(d, include)                     | Returns a new dictionary with only the keys in `include`.                                                                           |
| [`merge_dicts`](#lkj.dicts.merge_dicts)(\*mappings[, ...])                    | Merge multiple mappings into a single mapping, recursively if needed, with customizable conflict resolution for non-mapping values. |
| [`truncate_dict_values`](#lkj.dicts.truncate_dict_values)(d, \*[, max_list_size, ...]) | Returns a new dictionary with the same nested keys structure, where:                                                                |

### lkj.dicts.compare_field_values(dict1, dict2, \*, field_comparators={}, default_comparator=<built-in function eq>, aggregator=<function <lambda>>, get_comparison_fields=<function \_common_keys_list>)

Compare two dictionaries’ values field by field

* **Parameters:**
  * **dict1** – The first dictionary.
  * **dict2** – The second dictionary.
  * **field_comparators** ([`dict`](https://docs.python.org/3/library/stdtypes.html#dict)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`KT`), [`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`dict`](https://docs.python.org/3/library/stdtypes.html#dict), [`dict`](https://docs.python.org/3/library/stdtypes.html#dict)], [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]]) – A dictionary where keys are field names and values are comparator functions.
  * **default_comparator** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`dict`](https://docs.python.org/3/library/stdtypes.html#dict), [`dict`](https://docs.python.org/3/library/stdtypes.html#dict)], [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]) – A default comparator function to use if no specific comparator is provided for a field.
  * **aggregator** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`dict`](https://docs.python.org/3/library/stdtypes.html#dict)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`KT`), [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]], [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]) – A function to aggregate the comparison results into a final comparison object.
* **Returns:**
  A final score based on the comparison results.

```pycon
>>> dict1 = {"color": "brown", "animal": "dog"}
>>> dict2 = {"color": "brown", "animal": "cat"}
>>> dict3 = {"color": "brown", "animal": "bird"}
>>> field_comparators = {
...     "color": lambda x, y: 1 if x == y else 0,
...     "animal": lambda x, y: 1 if len(x) == len(y) else 0
... }
>>> compare_field_values(dict1, dict2, field_comparators=field_comparators)
{'color': 1, 'animal': 1}
>>> compare_field_values(dict1, dict3, field_comparators=field_comparators)
{'color': 1, 'animal': 0}
>>> import functools, statistics
>>> aggregator = lambda d: statistics.mean(d.values())
>>> mean_of_values = functools.partial(
...     compare_field_values, field_comparators=field_comparators, aggregator=aggregator
... )
>>> mean_of_values(dict1, dict2)
1
>>> mean_of_values(dict1, dict3)
0.5
```

### lkj.dicts.exclusive_subdict(d, exclude)

Returns a new dictionary with only the keys not in `exclude`.

### Parameters

d (dict): The input dictionary.
exclude (set): The set of keys to exclude from the new dictionary.

### Example

```pycon
>>> exclusive_subdict({'a': 1, 'b': 2, 'c': 3}, {'a', 'c'})
{'b': 2}
```

### lkj.dicts.inclusive_subdict(d, include)

Returns a new dictionary with only the keys in `include`.

### Parameters

d (dict): The input dictionary.
include (set): The set of keys to include in the new dictionary.

### Example

```pycon
>>> assert inclusive_subdict({'a': 1, 'b': 2, 'c': 3}, {'a', 'c'}) == {'a': 1, 'c': 3}
```

### lkj.dicts.merge_dicts(\*mappings, recursive_condition=<function <lambda>>, conflict_resolver=<function <lambda>>, mapping_constructor=<class 'dict'>)

Merge multiple mappings into a single mapping, recursively if needed,
with customizable conflict resolution for non-mapping values.

This function generalizes the normal `dict.update()` method, which takes the union
of the keys and resolves conflicting values by overriding them with the last value.
While `dict.update()` performs a single-level merge, `merge_dicts` provides additional
flexibility to handle nested mappings. With `merge_dicts`, you can:

- Control when to recurse (e.g., based on whether a value is a `Mapping`).
- Specify how to resolve value conflicts (e.g., override, add, or accumulate in a list).
- Choose the type of mapping (e.g., `dict`, `defaultdict`) to use as the container.

* **Parameters:**
  * **mappings** ([`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`KT`), [`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`VT`)]) – The mappings to merge.
  * **recursive_condition** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`VT`)], [`bool`](https://docs.python.org/3/library/functions.html#bool)]) – A callable to determine if values should be merged recursively.
    By default, checks if the value is a `Mapping`.
  * **conflict_resolver** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`VT`), [`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`VT`)], [`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`VT`)]) – A callable that resolves conflicts between two values.
    By default, overrides with the last seen value (`lambda x, y: y`).
  * **mapping_constructor** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`KT`), [`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`VT`)]]], [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`KT`), [`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`VT`)]]) – A callable to construct the resulting mapping.
    Defaults to the standard `dict` constructor.
* **Return type:**
  [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`KT`), [`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`VT`)]
* **Returns:**
  A merged mapping that combines all the input mappings.

### Examples

Basic usage with single-level merge (override behavior):

```pycon
>>> dict1 = {"a": 1}
>>> dict2 = {"a": 2, "b": 3}
>>> merge_dicts(dict1, dict2)
{'a': 2, 'b': 3}
```

Handling nested mappings with default behavior (override conflicts):

```pycon
>>> dict1 = {"a": 1, "b": {"x": 10, "y": 20}}
>>> dict2 = {"b": {"y": 30, "z": 40}, "c": 3}
>>> dict3 = {"b": {"x": 50}, "d": 4}
>>> merge_dicts(dict1, dict2, dict3)
{'a': 1, 'b': {'x': 50, 'y': 30, 'z': 40}, 'c': 3, 'd': 4}
```

Resolving conflicts by summing values:

```pycon
>>> dict1 = {"a": 1}
>>> dict2 = {"a": 2}
>>> merge_dicts(dict1, dict2, conflict_resolver=lambda x, y: x + y)
{'a': 3}
```

Accumulating conflicting values into a list:

```pycon
>>> dict1 = {"a": 1, "b": [1, 2]}
>>> dict2 = {"b": [3, 4]}
>>> merge_dicts(dict1, dict2, conflict_resolver=lambda x, y: x + y if isinstance(x, list) else [x, y])
{'a': 1, 'b': [1, 2, 3, 4]}
```

Recursing only on specific conditions:

```pycon
>>> dict1 = {"a": {"nested": 1}}
>>> dict2 = {"a": {"nested": 2, "new": 3}}
>>> merge_dicts(dict1, dict2)
{'a': {'nested': 2, 'new': 3}}
```

```pycon
>>> dict1 = {"a": {"nested": [1, 2]}}
>>> dict2 = {"a": {"nested": [3, 4]}}
>>> merge_dicts(dict1, dict2, recursive_condition=lambda v: isinstance(v, dict))
{'a': {'nested': [3, 4]}}
```

Using a custom mapping type (`defaultdict`):

```pycon
>>> from collections import defaultdict
>>> merge_dicts(
...     dict1, dict2, mapping_constructor=lambda items: defaultdict(int, items)
... )
defaultdict(<class 'int'>, {'a': defaultdict(<class 'int'>, {'nested': [3, 4]})})
```

### lkj.dicts.truncate_dict_values(d, \*, max_list_size=2, max_string_size=66, middle_marker='...', d_ingress=<function <lambda>>)

Returns a new dictionary with the same nested keys structure, where:

- List values are reduced to a maximum size of max_list_size.
- String values longer than max_string_size are truncated in the middle.
- Values are preprocessed with d_ingress before type checking.

### Parameters

d (dict): The input dictionary.
max_list_size (int, optional): Maximum size for lists. Defaults to 2.
max_string_size (int, optional): Maximum length for strings. Defaults to None (no truncation).
middle_marker (str, optional): String to insert in the middle of truncated strings. Defaults to ‘…’.
d_ingress (callable, optional): Function applied to each value before type checking.

> Defaults to identity function. Useful for handling special types like pandas Series.

### Returns

dict: A new dictionary with truncated lists and strings.

This can be useful when you have a large dictionary that you want to investigate,
but printing/logging it takes too much space.

### Example

```pycon
>>> large_dict = {'a': [1, 2, 3, 4, 5], 'b': {'c': [6, 7, 8, 9], 'd': 'A string like this that is too long'}, 'e': [10, 11]}
>>> truncate_dict_values(large_dict, max_list_size=3, max_string_size=20)
{'a': [1, 2, 3], 'b': {'c': [6, 7, 8], 'd': 'A string...too long'}, 'e': [10, 11]}
```

You can use `None` to indicate “no max”:

```pycon
>>> assert (
...     truncate_dict_values(large_dict, max_list_size=None, max_string_size=None)
...     == large_dict
... )
```

For handling special types like pandas Series:

```pycon
>>> def handle_pandas(obj):
...     if hasattr(obj, 'head'):  # pandas Series/DataFrame
...         return f"<{type(obj).__name__}: {len(obj)} items>"
...     return obj
>>> # truncate_dict_values(data_with_pandas, d_ingress=handle_pandas)
```

* **Return type:**
  [`dict`](https://docs.python.org/3/library/stdtypes.html#dict)

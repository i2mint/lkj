# lkj.iterables

Tools with iterables (dicts, lists, tuples, sets, etc.).

### Functions

| [`compare_sets`](#lkj.iterables.compare_sets)(left, right)                 | Compares two iterables and returns a named tuple with:         |
|--------------------------------------------------------------------------------------------|----------------------------------------------------------------|
| [`get_by_value`](#lkj.iterables.get_by_value)(list_of_dicts, value, field) | Get a dictionary from a list of dictionaries by a field value. |
| [`index_of`](#lkj.iterables.index_of)(iterable, value)                 | List list.index but for any iterable.                          |

### Classes

| [`SetsComparisonResult`](#lkj.iterables.SetsComparisonResult)(common, left_only, ...)   |    |
|-------------------------------------------------------------------------------------------------|----|

### *class* lkj.iterables.SetsComparisonResult(common, left_only, right_only)

Bases: [`NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple)

#### common *: [set](https://docs.python.org/3/library/stdtypes.html#set)*

Alias for field number 0

#### left_only *: [set](https://docs.python.org/3/library/stdtypes.html#set)*

Alias for field number 1

#### right_only *: [set](https://docs.python.org/3/library/stdtypes.html#set)*

Alias for field number 2

### lkj.iterables.compare_sets(left, right)

Compares two iterables and returns a named tuple with:

- Elements in both iterables.
- Elements only in the left iterable.
- Elements only in the right iterable.

#### NOTE
When applied to dicts, the comparison is done on the keys.
If you want a comparison on the values, use `compare_iterables(left.values(), right.values())`.

* **Parameters:**
  * **left** ([`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)) – The first iterable.
  * **right** ([`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)) – The second iterable.
* **Returns:**
  A namedtuple with fields `common`,
  `left_only`, and `right_only`.
* **Return type:**
  [`SetsComparisonResult`](#lkj.iterables.SetsComparisonResult)

### Examples

```pycon
>>> left = ['a', 'b', 'c']
>>> right = ['b', 'c', 'd']
>>> result = compare_sets(left, right)
>>> assert result.common == {'b', 'c'}  # asserting because order is not guaranteed
>>> result.left_only
{'a'}
>>> result.right_only
{'d'}
```

### lkj.iterables.get_by_value(list_of_dicts, value, field)

Get a dictionary from a list of dictionaries by a field value.

* **Return type:**
  [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`KT`), [`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`VT`)]

```pycon
>>> data = [{'id': 1, 'value': 'A'}, {'id': 2, 'value': 'B'}]
>>> get_by_value(data, 2, 'id')
{'id': 2, 'value': 'B'}
```

This function just WANTS to be `functools.partial`-ized!!

```pycon
>>> from functools import partial
>>> get_by_id = partial(get_by_value, field='id')
>>> get_by_id(data, 1)
{'id': 1, 'value': 'A'}
>>> get_value_of_B = partial(get_by_value, value='B', field='value')
>>> get_value_of_B(data)
{'id': 2, 'value': 'B'}
```

### lkj.iterables.index_of(iterable, value)

List list.index but for any iterable.

* **Return type:**
  [`int`](https://docs.python.org/3/library/functions.html#int)

```pycon
>>> index_of(iter('abc'), 'b')
1
>>> index_of(iter(range(5)), 3)
3
>>> index_of(iter('abc'), 'z')
Traceback (most recent call last):
...
ValueError: 'z' is not in iterable
```

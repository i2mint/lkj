# lkj.chunking

Tools for chunking (segumentation, batching, slicing, etc.)

### Functions

| [`chunk_iterable`](#lkj.chunking.chunk_iterable)(iterable, chk_size, \*[, ...])   | Divide an iterable into chunks/batches of a specific size.         |
|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| [`chunker`](#lkj.chunking.chunker)(a, chk_size, \*[, include_tail])        | Chunks an iterable into non-overlapping chunks of size `chk_size`. |

### lkj.chunking.chunk_iterable(iterable, chk_size, , chunk_type=None)

Divide an iterable into chunks/batches of a specific size.

Handles both mappings (e.g. dicts) and non-mappings (lists, tuples, sets…)
as you probably expect it to (if you give a dict input, it will chunk on the
(key, value) items and return dicts of these).
Thought note that you always can control the type of the chunks with the
`chunk_type` argument.

* **Parameters:**
  * **iterable** ([`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`T`)] | [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`KT`), [`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`VT`)]) – The iterable or mapping to divide.
  * **chk_size** ([`int`](https://docs.python.org/3/library/functions.html#int)) – The size of each chunk.
  * **chunk_type** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[`...`](https://docs.python.org/3/library/constants.html#Ellipsis), [`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`T`)] | [`Mapping`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Mapping)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`KT`), [`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`VT`)]] | [`None`](https://docs.python.org/3/library/constants.html#None)) – The type of the chunks (list, tuple, set, dict…).
* **Return type:**
  [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator)[[`list`](https://docs.python.org/3/library/stdtypes.html#list)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`T`)] | [`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`T`), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis)] | [`dict`](https://docs.python.org/3/library/stdtypes.html#dict)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`KT`), [`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`VT`)]]
* **Returns:**
  An iterator of dicts if the input is a Mapping, otherwise an iterator
  of collections (list, tuple, set…).

### Examples

```pycon
>>> list(chunk_iterable([1, 2, 3, 4, 5], 2))
[[1, 2], [3, 4], [5]]
```

```pycon
>>> list(chunk_iterable((1, 2, 3, 4, 5), 3, chunk_type=tuple))
[(1, 2, 3), (4, 5)]
```

```pycon
>>> list(chunk_iterable({"a": 1, "b": 2, "c": 3}, 2))
[{'a': 1, 'b': 2}, {'c': 3}]
```

```pycon
>>> list(chunk_iterable({"x": 1, "y": 2, "z": 3}, 1, chunk_type=dict))
[{'x': 1}, {'y': 2}, {'z': 3}]
```

### lkj.chunking.chunker(a, chk_size, , include_tail=True)

Chunks an iterable into non-overlapping chunks of size `chk_size`.

#### NOTE
This chunker is simpler, but also less efficient than `chunk_iterable`.
It does have the extra `include_tail` argument, though.
Though note that you can get the effect of `include_tail=False` in `chunk_iterable`
by using `filter(lambda x: len(x) == chk_size, chunk_iterable(...))`.

* **Parameters:**
  * **a** ([`Iterable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterable)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`T`)]) – The iterable to be chunked.
  * **chk_size** ([`int`](https://docs.python.org/3/library/functions.html#int)) – The size of each chunk.
  * **include_tail** ([`bool`](https://docs.python.org/3/library/functions.html#bool)) – If True, includes the remaining elements as the last chunk
    even if they are fewer than `chk_size`. Defaults to True.
* **Return type:**
  [`Iterator`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Iterator)[[`tuple`](https://docs.python.org/3/library/stdtypes.html#tuple)[[`TypeVar`](https://docs.python.org/3/library/typing.html#typing.TypeVar)(`T`), [`...`](https://docs.python.org/3/library/constants.html#Ellipsis)]]
* **Returns:**
  An iterator of tuples, where each tuple is a chunk of size `chk_size`
  (or fewer elements if `include_tail` is True).

### Examples

```pycon
>>> list(chunker(range(8), 3))
[(0, 1, 2), (3, 4, 5), (6, 7)]
>>> list(chunker(range(8), 3, include_tail=False))
[(0, 1, 2), (3, 4, 5)]
```

# lkj.misc

Miscellaneous tools.

### Functions

| `identity`(x)                                                                                  |    |
|------------------------------------------------------------------------------------------------|----|
| [`value_in_interval`](#lkj.misc.value_in_interval)([x, get_val, min_val, ...]) |    |

### lkj.misc.value_in_interval(x=None, /, \*, get_val=<function identity>, min_val=None, max_val=None, is_minimum=<built-in function ge>, is_maximum=<built-in function lt>)

```pycon
>>> from operator import itemgetter, le
>>> f = value_in_interval(get_val=itemgetter('date'), min_val=2, max_val=8)
>>> d = [{'date': 1}, {'date': 2}, {'date': 3, 'x': 7}, {'date': 8}, {'date': 9}]
>>> list(map(f, d))
[False, True, True, False, False]
```

The default `is_maximum` is `lt` (i.e. lambda x: x < max_val). If you want to
use `le` (i.e. lambda x: x <= max_val) you can change the is_maximum argument:

```pycon
>>> ff = value_in_interval(
...     get_val=itemgetter('date'), min_val=2, max_val=8, is_maximum=le
... )
>>> list(map(ff, d))
[False, True, True, True, False]
```

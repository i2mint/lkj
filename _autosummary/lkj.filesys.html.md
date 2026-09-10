# lkj.filesys

File system utils

### Functions

| [`do_nothing`](#lkj.filesys.do_nothing)(\*args, \*\*kwargs)                  | Function that does nothing.                                                               |
|--------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| [`enable_sourcing_from_file`](#lkj.filesys.enable_sourcing_from_file)([func, write_output]) | Decorator for functions enables the decorated function to source from a file.             |
| [`get_app_data_dir`](#lkj.filesys.get_app_data_dir)([dirname, if_exists, ...])     | Returns the full path of a directory suitable for storing application-specific data.      |
| [`get_watermarked_dir`](#lkj.filesys.get_watermarked_dir)(dirname[, watermark, ...])  | Get a watermarked directory.                                                              |
| [`has_watermark`](#lkj.filesys.has_watermark)(dirpath[, watermark])             | Check if a directory has a watermark.                                                     |
| [`rename_file`](#lkj.filesys.rename_file)(file, renamer_function, \*[, ...])  | This function takes a list of files and renames them using the provided renamer function. |
| [`search_folder_fast`](#lkj.filesys.search_folder_fast)(search_term[, ...])          | Executes a fast, recursive search using ripgrep and processes the results.                |
| `simple_jsonl_parser`(string)                                                                    |                                                                                           |
| [`watermark_dir`](#lkj.filesys.watermark_dir)(dirpath[, watermark])             | Watermark.                                                                                |

### lkj.filesys.do_nothing(\*args, \*\*kwargs)

Function that does nothing.

* **Return type:**
  [`None`](https://docs.python.org/3/library/constants.html#None)

### lkj.filesys.enable_sourcing_from_file(func=None, , write_output=False)

Decorator for functions enables the decorated function to source from a file.

It is to be applied to functions that take a string or bytes as their first
argument. Decorating the function will enable it to detect if the first argument
is a file path, read the file content, call the function with the file content
as the first argument. Optionally, the decorated function can write the result
back to the file, or another file if specified.

* **Parameters:**
  **write_output** ([*bool*](https://docs.python.org/3/library/functions.html#bool) *or* [*str*](https://docs.python.org/3/library/stdtypes.html#str)) – If True, write the output back to the file. If a
  string, write the output to the specified file path. Default is False.

### lkj.filesys.get_app_data_dir(dirname='', \*, if_exists=<function do_nothing>, if_does_not_exist=<built-in function mkdir>, rootdir='/home/runner/.config/')

Returns the full path of a directory suitable for storing application-specific data.

It’s a mini-framework for creating a directories: It allows us to specify what to do
if the directory already exists, and what to do if it doesn’t exist.

Typical use case: We want to create a directory for storing application-specific
data, but we don’t want to write in a directory whose name is already taken if
it’s not “our” directory. To achieve this, we can specify `if_exists` to be a
function that verifies, through some condition on the content (example, watermark
or subdirectory structure), that the directory was indeed create by our
application, and 

```
``
```

if_does_not_exist\`\`to be a function that creates the directory
and populates it with a watermark or otherwise recognizable content.

* **Parameters:**
  * **dirname** – The name of the directory to create.
  * **if_exists** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`str`](https://docs.python.org/3/library/stdtypes.html#str)], [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]) – A function to call if the directory already exists.
    By default, it does nothing. The main non-default use case is to validate the
    contents of the directory, and/or populate it.
    If you write a custome `if_exists` function, it is your responsibility to
    return the full path of the directory (unless your use case doesn’t actually
    need that!)
  * **if_does_not_exist** ([`Callable`](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[[`str`](https://docs.python.org/3/library/stdtypes.html#str)], [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]) – A function to call if the directory does not exist.
    By default, it creates the directory with `os.mkdir`. If you need to also
    create subdirectories, you can use `os.makedirs`. You can also choose to
    raise an error, telling the user to create the directory manually.
  * **rootdir** ([`str`](https://docs.python.org/3/library/stdtypes.html#str))
* **Returns:**

If you specify nothing else, you’ll just get the system-dependent root directory for
storing application-specific data:

```pycon
>>> app_data_dir = get_app_data_dir()
>>> app_data_dir == APP_DATA_ROOTDIR
True
```

You can control what happens if the directory already exists, or if it doesn’t.
The callbacks take the full path of the directory as an argument, and usually return
the path after doing something with it.

```pycon
>>> import os
>>> def notify_user_that_path_does_not_exist(path):
...     print(f"The '{os.path.basename(path)}' subdirectory doesn't exist")
...     return path
>>> dirpath = get_app_data_dir(
...     'nonexistent_dir',
...     if_does_not_exist=notify_user_that_path_does_not_exist
... )
The 'nonexistent_dir' subdirectory doesn't exist
```

For an example of how to use this function as a framework to make custom directory
factories, see [`get_watermarked_dir()`](#lkj.filesys.get_watermarked_dir).

### lkj.filesys.get_watermarked_dir(dirname, watermark='.lkj', \*, if_watermark_validation_fails=<function \_raise_watermark_error>, make_dir=<built-in function mkdir>, rootdir='/home/runner/.config/')

Get a watermarked directory.

```pycon
>>> from functools import partial
>>> import tempfile, os, shutil
>>> testdir = os.path.join(tempfile.gettempdir(), 'watermark_testdir')
>>> shutil.rmtree(testdir, ignore_errors=True)  # delete
>>> os.makedirs(testdir, exist_ok=True)  # and recreate afresh
>>> # Make a
>>> f = partial(get_watermarked_dir, rootdir=testdir)
>>> mytestdir = f('mytestdir', '.my_watermark')
>>> os.listdir(testdir)
['mytestdir']
>>> os.listdir(mytestdir)
['.my_watermark']
>>> another_testdir = f('another_testdir')
>>> os.listdir(another_testdir)
['.lkj']
```

### lkj.filesys.has_watermark(dirpath, watermark='.lkj')

Check if a directory has a watermark.

### lkj.filesys.rename_file(file, renamer_function, , dry_run=True, verbose=True)

This function takes a list of files and renames them using the provided renamer function.

### lkj.filesys.search_folder_fast(search_term, path_to_search='.', \*, egress=<function \_ripgrep_json_parser>)

Executes a fast, recursive search using ripgrep and processes the results.

* **Parameters:**
  * **search_term** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) – The regex pattern or text string to search for.
  * **path_to_search** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) – The folder path to start searching from. Defaults to current directory.
  * **egress** ([`Optional`](https://docs.python.org/3/library/typing.html#typing.Optional)[[`Callable`](https://docs.python.org/3/library/typing.html#typing.Callable)[[[`str`](https://docs.python.org/3/library/stdtypes.html#str)], [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)]]) – A callable function to process the raw ripgrep output string.
    Defaults to a parser that returns a list of dictionaries for matches.
    If set to None, it defaults to a lambda returning the raw output (string).
    You can also give it simple_jsonl_parser to get a list of all JSON objects in the output.
* **Return type:**
  [`Any`](https://docs.python.org/3/library/typing.html#typing.Any)
* **Returns:**
  The output of the ‘egress’ function.

## Example usage:

```pycon
>>> results = search_folder_fast("my_function_name", path_to_search='/path/to/project')
>>> for match in results:
...     print(f"Found in {match['path']} at line {match['line_number']}: {match['line_text']}")
```

### lkj.filesys.watermark_dir(dirpath, watermark='.lkj')

Watermark.

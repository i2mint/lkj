# lkj.funcs

Tools for working with functions.

### Functions

| [`filter_greater_than`](#lkj.funcs.filter_greater_than)(threshold, data)   | Filter elements in data that are greater than the threshold.                              |
|-----------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| [`full_path_maker`](#lkj.funcs.full_path_maker)(base_directory)        | Create a function that generates full file paths given filenames.                         |
| [`zip_with_filenames`](#lkj.funcs.zip_with_filenames)([start_idx])        | Create a function that zips an iterable with file names like 'file_001', 'file_002', etc. |

### lkj.funcs.filter_greater_than(threshold, data)

Filter elements in data that are greater than the threshold.

### Example

```pycon
>>> filter_greater_than_5 = filter_greater_than(5, range(10))
>>> list(filter_greater_than_5)
[6, 7, 8, 9]
```

### lkj.funcs.full_path_maker(base_directory)

Create a function that generates full file paths given filenames.

### Example

```pycon
>>> full_path = full_path_maker('/base/directory')
>>> list(full_path(['file1', 'file2']))
['/base/directory/file1', '/base/directory/file2']
```

### lkj.funcs.zip_with_filenames(start_idx=1)

Create a function that zips an iterable with file names like ‘file_001’, ‘file_002’, etc.

### Example

```pycon
>>> zip_files = zip_with_filenames()
>>> dict(zip_files([1, 2]))
{'file_001': 1, 'file_002': 2}
>>> dict(zip_files(['never', 'say', 'never']))
{'file_004': 'never', 'file_005': 'say', 'file_006': 'never'}
```

Using count ensures that each label is unique and ordered sequentially.

# lkj.importing

Tools for importing

### Functions

| [`import_from_path`](#lkj.importing.import_from_path)([pkg_path, rootdir, ...])      | Import a package from a specified path.                            |
|--------------------------------------------------------------------------------------------------|--------------------------------------------------------------------|
| [`import_object`](#lkj.importing.import_object)(dot_path)                         | Imports and returns an object from a dot string path.              |
| [`parent_dir_of_module`](#lkj.importing.parent_dir_of_module)(module_obj, \*[, ...])     | Get the parent directory of a given module object.                 |
| [`register_namespace_forwarding`](#lkj.importing.register_namespace_forwarding)(source_base, ...) | Register the namespace forwarding from source_base to target_base. |

### Classes

| [`NamespaceForwardingFinder`](#lkj.importing.NamespaceForwardingFinder)(source_base, ...)   | A custom finder that detects when a module in the source namespace is being imported and forwards it to the target namespace.   |
|------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------|
| [`NamespaceForwardingLoader`](#lkj.importing.NamespaceForwardingLoader)(fullname, ...)      | A custom loader that forwards the import from a source namespace to a target namespace.                                         |

### *class* lkj.importing.NamespaceForwardingFinder(source_base, target_base)

Bases: [`MetaPathFinder`](https://docs.python.org/3/library/importlib.html#importlib.abc.MetaPathFinder)

A custom finder that detects when a module in the source namespace is being imported
and forwards it to the target namespace.

#### source_base

The source namespace to detect and forward.

* **Type:**
  [*str*](https://docs.python.org/3/library/stdtypes.html#str)

#### target_base

The target namespace to forward the import to.

* **Type:**
  [*str*](https://docs.python.org/3/library/stdtypes.html#str)

### find_spec(fullname, path, target=None)::

Finds and returns the spec for the target module corresponding to the source module name.

### *class* lkj.importing.NamespaceForwardingLoader(fullname, source_base, target_base)

Bases: `Loader`

A custom loader that forwards the import from a source namespace to a target namespace.

#### fullname

The full name of the module being imported.

* **Type:**
  [*str*](https://docs.python.org/3/library/stdtypes.html#str)

#### source_base

The base namespace to detect and forward from.

* **Type:**
  [*str*](https://docs.python.org/3/library/stdtypes.html#str)

#### target_base

The base namespace to forward the import to.

* **Type:**
  [*str*](https://docs.python.org/3/library/stdtypes.html#str)

### load_module(fullname)::

Loads and returns the target module corresponding to the source module name.

#### load_module(fullname)

Return the loaded module.

The module must be added to sys.modules and have import-related
attributes set properly.  The fullname is a str.

ImportError is raised on failure.

This method is deprecated in favor of loader.exec_module(). If
exec_module() exists then it is used to provide a backwards-compatible
functionality for this method.

### lkj.importing.import_from_path(pkg_path=None, , rootdir='', insert_in_globals=False)

Import a package from a specified path.

* **Parameters:**
  * **pkg_path** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) – The path to the package to import. If None, returns a partial function.
  * **rootdir** ([`str`](https://docs.python.org/3/library/stdtypes.html#str)) – The root directory from which to resolve the package path.
  * **insert_in_globals** ([`bool`](https://docs.python.org/3/library/functions.html#bool)) – If True, insert the imported package into the global namespace.
* **Returns:**
  The imported package or a partial function for deferred import.
* **Return type:**
  module or functools.partial
* **Raises:**
  [**ImportError**](https://docs.python.org/3/library/exceptions.html#ImportError) – If the package cannot be found or imported.

```pycon
>>> import os, inspect  # standard library modules (that are surely installed)
>>> rootdir = parent_dir_of_module(os)  # get the parent directory of os module
>>> os_module = import_from_path('os', rootdir=rootdir)
>>> os_module == os
True
```

```pycon
>>> import lkj  # a third-party module (that is surely installed)
>>> parent_dir_of_lkj = parent_dir_of_module(lkj, parent_levels=2)  # get the great-grandma directory of lkj module
```

Make a partial function to import lkj from its parent directory:

```pycon
>>> my_import_from_path = import_from_path(rootdir=parent_dir_of_lkj, insert_in_globals=True)
>>> lkj_module = my_import_from_path('lkj')
>>> assert 'lkj' in globals(), "Module 'lkj' should be imported into globals"
>>> lkj_module == lkj
True
```

### lkj.importing.import_object(dot_path)

Imports and returns an object from a dot string path.

```pycon
>>> f = import_object('os.path.join')
>>> from os.path import join
>>> f is join
True
```

### lkj.importing.parent_dir_of_module(module_obj, , parent_levels=0)

Get the parent directory of a given module object.

* **Parameters:**
  **module_obj** – The module object for which to find the parent directory.
* **Returns:**
  The parent directory of the module as a string.

```pycon
>>> import os  # a standard library module
>>> parent_dir_of_module(os)
'...python...'
>>> import lkj # a third-party module
>>> parent_dir_of_module(lkj)
'.../lkj'
```

### lkj.importing.register_namespace_forwarding(source_base, target_base)

Register the namespace forwarding from source_base to target_base.

* **Parameters:**
  * **source_base** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The source namespace to forward.
  * **target_base** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The target namespace to forward to.

Usage:

> If you put this code in the imbed.mdat package (say, containing a hcp module),

> ```pycon
> >>> register_namespace_forwarding('imbed.mdat', 'imbed_data_prep')
> ```

> Then when you do

> ```pycon
> >>> import imbed.mdat.hcp
> ```

> You’ll get the imbed_data_prep.hcp module.

This function inserts the custom finder into sys.meta_path, enabling the
dynamic import forwarding.

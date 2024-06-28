"""Tools for importing"""


def import_object(dot_path: str):
    """Imports and returns an object from a dot string path.

    >>> f = import_object('os.path.join')
    >>> from os.path import join
    >>> f is join
    True

    """
    from importlib import import_module

    module_path, _, object_name = dot_path.rpartition('.')
    if not module_path:
        raise ImportError(f'{dot_path} does not contain a module path')
    module = import_module(module_path)
    try:
        return getattr(module, object_name)
    except AttributeError:
        raise ImportError(f'{object_name} is not found in {module_path}')


import sys
import importlib.util
import importlib.abc


class NamespaceForwardingLoader(importlib.abc.Loader):
    """
    A custom loader that forwards the import from a source namespace to a target namespace.

    Attributes:
        fullname (str): The full name of the module being imported.
        source_base (str): The base namespace to detect and forward from.
        target_base (str): The base namespace to forward the import to.

    Methods:
        load_module(fullname):
            Loads and returns the target module corresponding to the source module name.
    """

    def __init__(self, fullname, source_base, target_base):
        self.fullname = fullname
        self.source_base = source_base
        self.target_base = target_base

    def load_module(self, fullname):
        target_name = fullname.replace(self.source_base, self.target_base)

        # If the target module is already loaded, return it
        if target_name in sys.modules:
            return sys.modules[target_name]

        # Find the spec of the target module
        spec = importlib.util.find_spec(target_name)
        if spec is None:
            raise ImportError(f"No module named '{target_name}'")

        # Create and load the target module
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[fullname] = module
        return module


class NamespaceForwardingFinder(importlib.abc.MetaPathFinder):
    """
    A custom finder that detects when a module in the source namespace is being imported
    and forwards it to the target namespace.

    Attributes:
        source_base (str): The source namespace to detect and forward.
        target_base (str): The target namespace to forward the import to.

    Methods:
        find_spec(fullname, path, target=None):
            Finds and returns the spec for the target module corresponding to the source module name.
    """

    def __init__(self, source_base, target_base):
        self.source_base = source_base
        self.target_base = target_base

    def find_spec(self, fullname, path, target=None):
        if fullname.startswith(self.source_base):
            return importlib.util.spec_from_loader(
                fullname,
                NamespaceForwardingLoader(fullname, self.source_base, self.target_base),
            )
        return None


def register_namespace_forwarding(source_base, target_base):
    """
    Register the namespace forwarding from source_base to target_base.

    Args:
        source_base (str): The source namespace to forward.
        target_base (str): The target namespace to forward to.

    Usage:

        # if you put this code in the imbed.mdat package (say, containing a hcp module),
        >>> register_namespace_forwarding('imbed.mdat', 'imbed_data_prep')  # doctest: +SKIP

        # Then when you do

        >>> import imbed.mdat.hcp  # doctest: +SKIP

        You'll get the imbed_data_prep.hcp module.

    This function inserts the custom finder into sys.meta_path, enabling the
    dynamic import forwarding.
    """
    sys.meta_path.insert(0, NamespaceForwardingFinder(source_base, target_base))

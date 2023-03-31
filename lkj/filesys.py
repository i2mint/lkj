"""File system utils"""

import os
from typing import Callable, Any
from pathlib import Path


def do_nothing(*args, **kwargs) -> None:
    """Function that does nothing."""
    pass


def _app_data_rootdir():
    """
    Returns the full path of a directory suitable for storing application-specific data.

    On Windows, this is typically %APPDATA%.
    On macOS, this is typically ~/.config.
    On Linux, this is typically ~/.config.

    Returns:
        str: The full path of the app data folder.

    See https://github.com/i2mint/i2mint/issues/1.
    """
    if os.name == "nt":
        # Windows
        APP_DATA_ROOTDIR = os.getenv("APPDATA")
        if not APP_DATA_ROOTDIR:
            raise RuntimeError("APPDATA environment variable is not set")
    else:
        # macOS and Linux/Unix
        APP_DATA_ROOTDIR = os.path.expanduser("~/.config")

    if not os.path.isdir(APP_DATA_ROOTDIR):
        os.mkdir(APP_DATA_ROOTDIR)

    return APP_DATA_ROOTDIR


APP_DATA_ROOTDIR = _app_data_rootdir()


def get_app_data_dir(
    dirname="",
    *,
    if_exists: Callable[[str], Any] = do_nothing,
    if_does_not_exist: Callable[[str], Any] = os.mkdir,
    rootdir: str = APP_DATA_ROOTDIR,
):
    """
    Returns the full path of a directory suitable for storing application-specific data.

    It's a mini-framework for creating a directories: It allows us to specify what to do
    if the directory already exists, and what to do if it doesn't exist.

    Typical use case: We want to create a directory for storing application-specific
    data, but we don't want to write in a directory whose name is already taken if
    it's not "our" directory. To achieve this, we can specify ``if_exists`` to be a
    function that verifies, through some condition on the content (example, watermark
    or subdirectory structure), that the directory was indeed create by our
    application, and ``if_does_not_exist``to be a function that creates the directory
    and populates it with a watermark or otherwise recognizable content.

    :param dirname: The name of the directory to create.
    :param if_exists: A function to call if the directory already exists.

    :param if_does_not_exist: A function to call if the directory does not exist.
        By default, it creates the directory with ``os.mkdir``. If you need to also
        create subdirectories, you can use ``os.makedirs``. You can also chose to
        raise an error, telling the user to create the directory manually.
    :param rootdir:
    :return:

    If you specify nothing else, you'll just get the system-dependent root directory for
    storing application-specific data:

    >>> app_data_dir = get_app_data_dir()
    >>> app_data_dir == APP_DATA_ROOTDIR

    >>> from pathlib import Path
    >>> from functools import partial
    >>> watermark_dir = lambda dirpath, watermark: (Path(dirpath) / watermark).touch()
    >>> has_watermark = lambda dirpath, watermark: (Path(dirpath) / watermark).exists()

    >>> get_app_data_dir(
    ...     '.config2py',
    ...     if_exists=partial(watermark_dir, watermark='myapp')
    ... )
    """
    dirpath = os.path.join(rootdir, dirname)
    if os.path.isdir(dirpath):
        if if_exists is not None:
            if_exists(dirpath)
    else:
        if if_does_not_exist is not None:
            if_does_not_exist(dirpath)
    return dirpath


DFLT_WATERMARK = ".config2py"


def watermark_dir(dirpath: str, watermark: str = DFLT_WATERMARK):
    """Watermark."""
    (Path(dirpath) / watermark).touch()


def has_watermark(dirpath: str, watermark: str = DFLT_WATERMARK):
    """Check if a directory has a watermark."""
    return (Path(dirpath) / watermark).exists()


def _raise_watermark_error(dirpath, watermark):
    raise ValueError(
        f"Directory {dirpath} is not watermarked with {watermark}. "
        f"Perhaps you deleted the watermark file? If so, create the file and all will "
        f"be good. For example, you could do:\n"
        f"    import pathlib; (pathlib.Path('{dirpath}') / '{watermark}').touch()"
    )


def get_watermarked_dir(
    dirname: str,
    watermark: str = DFLT_WATERMARK,
    *,
    rootdir: str = APP_DATA_ROOTDIR,
    if_watermark_validation_fails: Callable[[str, str], Any] = _raise_watermark_error,
):
    """Get a watermarked directory.

    >>> from functools import partial
    >>> import tempfile, os, shutil
    >>> testdir = os.path.join(tempfile.gettempdir(), 'watermark_testdir')
    >>> shutil.rmtree(testdir)  # delete
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
    ['.config2py']

    """

    def create_and_watermark(dirpath):
        os.mkdir(dirpath)
        watermark_dir(dirpath, watermark=watermark)

    def validate_watermark(dirpath):
        if not has_watermark(dirpath, watermark):
            return if_watermark_validation_fails(dirpath, watermark)

    return get_app_data_dir(
        dirname,
        if_exists=validate_watermark,
        if_does_not_exist=create_and_watermark,
        rootdir=rootdir,
    )

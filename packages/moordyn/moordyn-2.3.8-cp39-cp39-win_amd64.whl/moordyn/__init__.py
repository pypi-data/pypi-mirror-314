"""moordyn is a Python wrapper for the MoorDyn v2 C library

It is used in the same way than the regular MoorDyn C API:

.. code-block:: python

    import moordyn
    system = moordyn.Create(filepath="Mooring/lines.txt")
    moordyn.SetVerbosity(system, moordyn.LEVEL_MSG)
    moordyn.SetLogFile(system, "Mooring/lines.log")
    moordyn.SetLogLevel(system, moordyn.LEVEL_MSG)
    moordyn.Log(system, "We are ready to work!")
    x = [5.2, 0.0, -70.0,
         -2.6, 4.5, -70.0,
         -2.6, -4.5, -70.0]
    v = [0, ] * 9
    moordyn.Init(system, x, v)
    dt = 0.1
    moordyn.Step(system, x, v, 0.0, dt)
    moordyn.Close(system)

The majority of functions are returning error codes, exactly the same way the
MoorDyn v2 C API is doing
"""


# start delvewheel patch
def _delvewheel_patch_1_9_0():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, '.'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-moordyn-2.3.8')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-moordyn-2.3.8')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_9_0()
del _delvewheel_patch_1_9_0
# end delvewheel patch

from .moordyn import *
from .moorpyic import *
from . import Generator
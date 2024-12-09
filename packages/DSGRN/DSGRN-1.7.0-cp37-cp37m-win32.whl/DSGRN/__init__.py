### __init__.py
### MIT LICENSE 2018 Shaun Harker
### MIT LICENSE 2024 Marcio Gameiro


# start delvewheel patch
def _delvewheel_patch_1_8_2():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'DSGRN.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-DSGRN-1.7.0')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-DSGRN-1.7.0')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_8_2()
del _delvewheel_patch_1_8_2
# end delvewheel patch

from DSGRN._dsgrn import *
from DSGRN.SubdomainGraph import *
from DSGRN.BlowupGraph import *
from DSGRN.Graphics import *
from DSGRN.Query.Graph import *
from DSGRN.Query.Database import *
from DSGRN.Query.Hexcodes import *
from DSGRN.Query.MonostableQuery import *
from DSGRN.Query.BistableQuery import *
from DSGRN.Query.MultistableQuery import *
from DSGRN.Query.NstableQuery import *
from DSGRN.Query.SingleFixedPointQuery import *
from DSGRN.Query.DoubleFixedPointQuery import *
from DSGRN.Query.MonostableFixedPointQuery import *
from DSGRN.Query.SingleGeneQuery import *
from DSGRN.Query.InducibilityQuery import *
from DSGRN.Query.HysteresisQuery import *
from DSGRN.Query.PhenotypeQuery import *
from DSGRN.Query.PosetOfExtrema import *
from DSGRN.Query.Logging import *
from DSGRN.Query.StableFCQuery import *
from DSGRN.Query.ComputeSingleGeneQuery import *
from DSGRN.EssentialParameterNeighbors import *
from DSGRN.BooleanParameterNeighbors import *
from DSGRN.ParameterPartialOrders import *
from DSGRN.ParameterFromSample import *
from DSGRN.SaveDatabaseJSON import *
from DSGRN.EquilibriumCells import *
from DSGRN.MorseGraphIsomorphism import *
from DSGRN.DrawParameterGraph import *
from DSGRN.IsomorphismQuery import *

import sys
import os
import pickle

configuration().set_path(os.path.dirname(__file__) + '/Resources')

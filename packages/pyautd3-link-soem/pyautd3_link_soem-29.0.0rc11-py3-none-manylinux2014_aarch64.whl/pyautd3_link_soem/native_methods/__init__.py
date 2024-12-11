import os
import os.path
import platform

from .autd3capi_link_soem import NativeMethods as LinkSOEM

_PLATFORM = platform.system()
_PREFIX = ""
_BIN_EXT = ""
if _PLATFORM == "Windows":
    _BIN_EXT = ".dll"
elif _PLATFORM == "Darwin":
    _PREFIX = "lib"
    _BIN_EXT = ".dylib"
elif _PLATFORM == "Linux":
    _PREFIX = "lib"
    _BIN_EXT = ".so"
else:
    raise ImportError("Not supported OS")

_LIB_PATH = os.path.join(os.path.dirname(__file__), "..", "bin")

LinkSOEM().init_dll(_LIB_PATH, _PREFIX, _BIN_EXT)

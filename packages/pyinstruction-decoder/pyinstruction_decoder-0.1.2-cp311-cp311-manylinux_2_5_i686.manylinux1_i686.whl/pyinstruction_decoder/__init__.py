from ._pyinstruction_decoder import *
import pathlib as _pathlib
import sysconfig as _sysconfig
import os as _os

_os.environ["PYINSTRUCTION_DECODER_TOMLPATH"] = str(_pathlib.Path(_sysconfig.get_path("data")).joinpath('toml/'))
__doc__ = _pyinstruction_decoder.__doc__
if hasattr(_pyinstruction_decoder, "__all__"):
    __all__ = _pyinstruction_decoder.__all__
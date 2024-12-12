from ._pyinstruction_decoder import *
import importlib.resources as _resources
import os as _os

_os.environ["PYINSTRUCTION_DECODER_TOMLPATH"] = str(_resources.files(_pyinstruction_decoder).joinpath('toml/'))
__doc__ = _pyinstruction_decoder.__doc__
if hasattr(_pyinstruction_decoder, "__all__"):
    __all__ = _pyinstruction_decoder.__all__
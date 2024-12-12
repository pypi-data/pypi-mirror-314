from ._pyinstruction_decoder import *
import importlib.resources as _resources
import os as _os
import argparse as _argparse
import sys as _sys


_os.environ["PYINSTRUCTION_DECODER_TOMLPATH"] = str(_resources.files(_pyinstruction_decoder).joinpath('toml/'))
__doc__ = _pyinstruction_decoder.__doc__
if hasattr(_pyinstruction_decoder, "__all__"):
    __all__ = _pyinstruction_decoder.__all__

def _rvdecode():
    parser = _argparse.ArgumentParser(prog="rvdecode", description="""This program decodes RISC-V instructions.""")
    parser.add_argument("-s", "--specification", default="RV32I", help="RISC-V specification to use, default value is RV32I. To use all extensions, simply use RV32All or RV64All for 64 bit RISC-V")
    parser.add_argument("-f", "--format", default="string", choices=["string", "binary"], help="format to use, supported are: binary or string, string is default")
    parser.add_argument("-b", "--base", default=0, help="base of input string, default is base 0 for auto detecting number from prefix, ignored in binary mode", type=int)
    parser.add_argument("-e", "--endianness", default="little", choices=["little", "big"], help="byteorder of input, default is little endian, since that is what RISC-V uses, but big endian is supported in case of weird input data, ignored in string mode")

    args = parser.parse_args()
    spec = args.specification
    fmt = args.format
    base = args.base
    endianness = args.endianness

    dec = get_riscvdecoder(spec)
    try:
        if fmt == "string":
            for line in _sys.stdin:
                inp = int(line.strip(), base=base)
                try:
                    inst = dec.decode(inp, 32)
                    print(inst)
                except ValueError as ve:
                    print(ve)
        else:
            while True:
                data = _sys.stdin.buffer.read(4)
                if len(data) != 4:
                    break
                inp = int.from_bytes(data, endianness)
                try:
                    inst = dec.decode(inp, 32)
                    print(inst)
                except ValueError as ve:
                    print(ve)
    except KeyboardInterrupt:
        pass
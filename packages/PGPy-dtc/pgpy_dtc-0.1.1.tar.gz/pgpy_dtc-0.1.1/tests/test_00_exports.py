""" check the export list to ensure only the public API is exported by pgpy.__init__
"""
import pytest

import importlib
import inspect


modules = ['pgpy_dtc.constants',
           'pgpy_dtc.decorators',
           'pgpy_dtc.errors',
           'pgpy_dtc.pgp',
           'pgpy_dtc.symenc',
           'pgpy_dtc.types',
           'pgpy_dtc.packet.fields',
           'pgpy_dtc.packet.packets',
           'pgpy_dtc.packet.types',
           'pgpy_dtc.packet.subpackets.signature',
           'pgpy_dtc.packet.subpackets.types',
           'pgpy_dtc.packet.subpackets.userattribute']


def get_module_objs(module):
    # return a set of strings that represent the names of objects defined in that module
    return { n for n, o in inspect.getmembers(module, lambda m: inspect.getmodule(m) is module) } | ({'FlagEnum',} if module is importlib.import_module('pgpy_dtc.types') else set())  # dirty workaround until six fixes metaclass stuff to support EnumMeta in Python >= 3.6


def get_module_all(module):
    return set(getattr(module, '__all__', set()))


def test_pgpy_all():
    import pgpy_dtc
    # just check that everything in pgpy.__all__ is actually there
    assert set(pgpy_dtc.__all__) <= {n for n, _ in inspect.getmembers(pgpy_dtc)}


@pytest.mark.parametrize('modname', modules)
def test_exports(modname):
    module = importlib.import_module(modname)

    assert get_module_all(module) == get_module_objs(module)

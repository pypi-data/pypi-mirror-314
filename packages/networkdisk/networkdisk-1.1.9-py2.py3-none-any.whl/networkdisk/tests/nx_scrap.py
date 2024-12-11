import importlib
import sys
import os
import inspect
from pytest import skip
from types import FunctionType


def get_test_classes_nx(module):
    """
    It is ugly, I know. But how to do
    that correctly?
    """
    L = os.listdir(list(module.__path__)[0])
    submodules = []
    for e in L:
        try:
            submodules.append(importlib.import_module(f"{module.__name__}.{e[:-3]}"))
        except (ImportError, skip.Exception):
            pass
    classes = list(
        map(
            lambda T: list(
                filter(inspect.isclass, map(lambda e: getattr(T, e), dir(T)))
            ),
            submodules,
        )
    )
    return list(filter(lambda e: e.__name__.startswith("Test"), sum(classes, [])))


def get_test_module_nx(module_name):
    try:
        module = importlib.import_module(f"{module_name}.tests")
        return module
    except ModuleNotFoundError:
        return False


def get_nx_tests():
    tests_modules = []
    for mod in list(sys.modules.keys()):
        if not mod.startswith("networkx."):
            continue
        module = get_test_module_nx(mod)
        if module:
            tests_modules.extend(get_test_classes_nx(module))
    return tests_modules

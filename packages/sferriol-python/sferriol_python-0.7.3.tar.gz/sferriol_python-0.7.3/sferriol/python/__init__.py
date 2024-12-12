import importlib.util
import pathlib
import time
import types
from typing import Any, Callable


def load_module_from_file(fpath):
    """
    Load a module from a python file. 
    The module name is the file name without file extension. 
    """
    name = module_name_from_file(fpath)
    spec = importlib.util.spec_from_file_location(name, fpath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def loop_until(fct: Callable, ret: Any, every: float, timeout: float | int):
    """Loops the execution of the function until it returns ret parameter
    
    It raises TimeoutError if the expected value is not returned by the function
 
    Args:
      fct: Function to be called
      ret: The expected return value
      every: Number of seconds to wait at the end of each loop
      timeout: Timeout duration
    """
    start_time = time.perf_counter()
    while True:
        if fct() == ret:
            return
        time.sleep(every)
        if time.perf_counter() - start_time >= timeout:
            raise TimeoutError()


def method(obj):
    """
    Decorator used to define a function as a new method of the object obj.
    The method name is the function name.
    """

    def _(func):
        name = func.__name__
        setattr(obj, name, types.MethodType(func, obj))
        return getattr(obj, name)

    return _


def module_name_from_file(fpath):
    """
    Return The module name of the associated python file.
    """
    return pathlib.Path(fpath).stem


def update_methods(obj, functions):
    """
    Update object methods by bounding new functions to instance obj
    """
    for func in functions:
        name = func.__name__
        setattr(obj, name, types.MethodType(func, obj))

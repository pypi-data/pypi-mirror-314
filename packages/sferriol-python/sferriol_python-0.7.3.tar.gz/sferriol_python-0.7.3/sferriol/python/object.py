# -*- coding: utf-8 -*-
import types


class Attribute:
    def __init__(self, ns):
        self.__sf__ns__ = ns

    def __call__(self, fct):
        setattr(self, fct.__name__, fct)

    def __setattr__(self, name, value):
        if hasattr(self, '__sf__ns__'):
            ns = self.__sf__ns__
            ns.__sf__obj_attributes__[name] = value
            setattr(ns, name, value)
        else:
            object.__setattr__(self, name, value)


def attribute(ns):
    return Attribute(ns)


class Object:
    def __init__(self):
        self.__sf__namespaces = dict()

    def __set_ns__(self, ns):
        for name, value in ns.__sf__obj_attributes__.items():
            if callable(value):
                value = types.MethodType(value, self)
            setattr(self, name, value)
        self.__sf__namespaces[ns.__sf__name__] = ns


class Namespace:
    def __init__(self, name):
        self.__sf__name__ = name
        self.__sf__obj_attributes__ = dict()

    def __call__(self, obj=None):
        if obj is None:
            obj = Object()
        obj.__set_ns__(self)
        return obj


def namespace():
    def wrapper(fct):
        ns = Namespace(fct.__name__)
        fct(ns)
        return ns

    return wrapper

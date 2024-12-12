#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Copyright 2020 sferriol <sferriol@ipnl.in2p3.fr>


class adict(dict):
    """Attribute dictionary
    """
    def __delattr__(self, name):
        self.__delitem__(name)

    def __getattr__(self, name):
        try:
            ret = getattr(adict, name)
        except AttributeError as e:
            try:
                ret = self.__getitem__(name)
            except KeyError:
                # if nothing is found, raise AttributeError instead of KeyError
                raise e
        return ret

    def __setattr__(self, name, value):
        self.__setitem__(name, value)


def as_adict(elt):
    return dict_to_adict(elt)


class cdict(adict):
    """Config dictionary.
    c = cdict()
    c['a.b'] = 2 # is equivalent to c['a'] = {'b':2}
    assert c['a.b'] == c['a']['b']
    assert c['a.b'] == c.a.b
    """
    def __getitem__(self, key):
        di = self
        l = key.split('.')
        for k in l[:-1]:
            di = di[k]
        return adict.__getitem__(di, l[-1])

    def __setitem__(self, key, value):
        di = self
        l = key.split('.')
        for k in l[:-1]:
            di.setdefault(k, adict())
            di = di[k]
        adict.__setitem__(di, l[-1], value)


def dict_merge(di_1, di_2):
    def _dict(di_1, di_2):
        for key, value in di_2.items():
            if isinstance(value, dict):
                if key not in di_1:
                    di_1[key] = {}
                _dict(di_1[key], di_2[key])
            else:
                di_1[key] = value

    _dict(di_1, di_2)
    return di_1


def dict_to_adict(di):
    # build an adict from a dictionary
    # and all sub dictionary will be trannform in Attribute_Dict too
    def _di2adi(elt):
        if isinstance(elt, list):
            return [_di2adi(e) for e in elt]
        if isinstance(elt, dict):
            adi = adict()
            for k, v in elt.items():
                adi[k] = _di2adi(v)
            return adi
        return elt

    return _di2adi(di)

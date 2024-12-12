# -*- coding: utf-8 -*-
#
#  Copyright 2023 sferriol <s.ferriol@ip2i.in2p3.fr>

import json
import tempfile


def dump_temporary(obj, prefix=None, dir=None):
    """
    Serialize obj as a JSON formatted stream to a temporary file and returns its file path. The file is created securely, using the same rules as mkstemp().  The user is responsible for deleting the temporary file when done with it.
    """
    _, fpath = tempfile.mkstemp(prefix=prefix, suffix='.json', dir=dir)
    with open(fpath, 'w') as f:
        json.dump(obj, f)
    return fpath

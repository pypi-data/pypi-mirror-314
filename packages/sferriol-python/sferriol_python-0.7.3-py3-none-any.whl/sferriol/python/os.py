# -*- coding: utf-8 -*-
#
#  Copyright 2023 sferriol <s.ferriol@ip2i.in2p3.fr>

import contextlib
import os


def remove_if_exists(fpath):
    with contextlib.suppress(FileNotFoundError):
        os.remove(fpath)

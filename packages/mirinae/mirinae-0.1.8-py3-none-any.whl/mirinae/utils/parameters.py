#!/usr/bin/env python
# encoding: utf-8
# Copyright (c) 2022 SATURN
# AUTHORS
# Sukbong Kwon (Galois)

from functools import reduce
from typing import Text
from argparse import Namespace
from type_docopt import docopt

def args2params(args):
    repls =  {'--' : '', '<': '', '>' : '', '-': '_'}
    params = {}
    for key, val in args.items():
        params[reduce(lambda a, kv: a.replace(*kv), repls.items(), key)] = val
    return params

def arg2kwargs(args):
    return reduce(lambda a, kv: a.update(kv) or a, args2params(args).items(), {})


def get_params(
    __doc__,
)-> Namespace:
    args = docopt(__doc__)
    return Namespace(**args2params(args))
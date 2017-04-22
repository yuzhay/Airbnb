#!/usr/bin/env python3

from common import *
from sync import Sync

sync = Sync(db)

sync.run()

# def f(**params):
#     print(params)
#
# f(a=1,b=2)
#
# a = {'a': 1, 'b': 2}
# f(c = 3, **a)

# -*- coding: utf-8 -*-

try:
    dict = {}
    print(dict['a'])
except KeyError as e:
    print(e.__traceback__)


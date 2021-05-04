# -*- coding: utf-8 -*-
"""
@date Tue May  4 12:06:32 2021

@brief Information about this Module

@author: aweis
"""

try: # try to import useful extended dictionary implementation
    from WeissTools.Dict import WDict as FolioDict
except ModuleNotFoundError:
    from collections import OrderedDict as FolioDict
# -*- coding: utf-8 -*-
"""
@date Tue May  4 12:08:42 2021

@brief Tax core module

@author: aweis
"""

from datetime import timedelta

from pyfolio.core import FolioDict

TAX_STATUS_ALIASES = {
    'regular':[None],
    'exempt':['roth'],
    'deferred':[]
    }

ACCOUNT_TYPE_ALIASES = {
    'regular':[None],
    'ira':['retirement'],
    '401k':[]}

def get_gain_type(hold_duration):
    '''@brief get type of capital gain from a time duration'''
    if hold_duration<timedelta(days=365):type='short'
    else: type='long'
    return type 


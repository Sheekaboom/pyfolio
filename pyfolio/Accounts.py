# -*- coding: utf-8 -*-
"""
@date Tue May  4 12:32:59 2021

@brief Module to deal with accounts (and likely tax status)

@author: aweis
"""

from pyfolio.Securities.core import SecurityGroup,Security

class Account(SecurityGroup):
    '''@brief class to hold account info'''
    def __init__(self,*args,**kwargs):
        '''@brief constructor'''
        super().__init__(*args,**kwargs)
        # assume all children are securities
        self['children'] = [Security(**c) for c in self['children']]
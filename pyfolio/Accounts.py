# -*- coding: utf-8 -*-
"""
@date Tue May  4 12:32:59 2021

@brief Module to deal with accounts.

@author: aweis
"""

from pyfolio.Securities.core import SecurityGroup,Security

class Account(SecurityGroup):
    '''@brief class to hold account info'''
    def __init__(self,*args,**kwargs):
        '''@brief constructor'''
        super().__init__(*args,**kwargs)
        # assume all children are securities
        self['children'] = {cid:Security(**cv) for cid,cv in self['children'].items()}
        self['gains'] = [] # list of gains for a given period
        
    def sell(self,security,count='all',sellfor='cash'):
        '''
        @brief sell a given amount of a security.
        @param[in] security - id of security to sell (from Security().get_id)
        @param[in] count - how much to sell. If 'all' sell self['count']
        @return dictionary with deltas of securities (e.g. -count, +count)
        '''
        sec = self['children'][security]
        sec_count = sec['count']
        if count=='all':
            count = sec_count 
        elif count>sec_count:
            raise Exception("Cannot sell {} shares when only {} are available".format(count,sec_count))
        # now lets actually calculate the delta and get our gains
        gains = sec.get_gains(count=count)
        
    def deposit(self,count):
        '''@brief deposit an amount of money in cash into the account'''
        self['children']['cash']['count']+=count   
    
    def withdraw(self,count):
        self.deposit(-count)
        
    def _add_gains(self,gains):
        '''@brief add a list of gains to our list. should AT LEAST have keys 'type' and 'count' '''
        self['gains']+=sgains
        
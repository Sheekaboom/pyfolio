# -*- coding: utf-8 -*-
"""
@date Tue May  4 11:54:25 2021

@brief Classes for securities and groups. It's imporatnt to know, this currently
    CANNOT handle calculating gains with different buy/sell dates of the same security

@author: aweis
"""

from pyfolio.core import FolioDict
from pyfolio.core.Ticker import Ticker
from pyfolio.Taxes import get_gain_type

from datetime import datetime,timedelta
import numpy as np
import os,re

#%% Templates for default inputs
    
BASE_TEMPLATE = { # template for all things
    'name':None, # name for object
    'currency':'USD',
    'category':None, # category or list of categories to filter by
    'risk':None, # risk level (0-1) with 1 being SUPER HIGH RISK
    'tax_status':None # None/'regular'|'exempt'/'roth'|'deferred'
    }

SECURITY_TEMPLATE = {
    'ticker':None,
    'value':1, # default value (e.g. cash)
    # these next two are used to calculate gains/losses and tax info
    'buy_date':datetime.now(),
    }
SECURITY_TEMPLATE.update(BASE_TEMPLATE)

SECURITY_GROUP_TEMPLATE = {
    'children':{},
    'gains': 0 # gains/losses from buys/sells in the group
    }
SECURITY_GROUP_TEMPLATE.update(BASE_TEMPLATE)

#%% Classes for securities

class Security(FolioDict):
    '''
    @brief a class to hold a security
    @note this is utilizes input data and yfinance to get data
    @param[in] get_ticker - whether or not to try and retrieve ticker data (default true)
    @param[in] kwargs - see SECURITY_TEMPLATE
    '''
    def __init__(self,ticker=None,get_ticker=True,**kwargs):
        '''@brief constructor'''
        kwargs_out = SECURITY_TEMPLATE
        kwargs_out.update(ticker=ticker,**kwargs)
        super().__init__(**kwargs_out) # initalize the dict
        # Try and get ticker if its a thing
        self._ticker = None #yfinance ticker object            
        if get_ticker and  ticker is not None and ticker.lower()!='cash':
            self._update_ticker()
        # verify the configuration
        self._verify()
            
    def _verify(self):
        '''@brief verify we have things we need'''
        # verify we have a count
        count = self.get('count',None)
        if count is None: raise Exception("Name:{}, Ticker:{}, has invalid 'count' {}".format(self['name'],self['ticker'],count))
        
    def _update_ticker(self):
        '''@brief get ticker info with yfinance and set to self._ticker'''
        ticker = self.get('ticker',None) # try and get tick
        if ticker is not None: self._ticker = Ticker(ticker)
        
    def get_id(self):
        '''@brief get an id label for the security'''
        # first see if we have a ticker
        if self['ticker'] is not None:
            id = self['ticker']
        elif self['name'] is not None:
            id = self['name']
        else:
            raise Exception("Can't get ID. Neither 'ticker' or 'name' are defined.")
        # now clean the id
        id = id.lower() # make lowercase 
        id = re.sub('[ ]+','_',id) # clean some characters
        return id
        
    def get_value(self,**kwargs):
        '''@brief return the current value of the security'''
        self._verify()
        if self._ticker is not None: # if its a ticker
            tval = np.asarray(self._ticker.get_value(**kwargs))
        else: # otherwise use whatever self['value'] is set to
            tval = self['value']
        return tval*self['count']
    
    def get_cost_basis(self):
        '''@brief get the cost basis of the security (total amount invested)'''
        return self.get_value(self['buy_date'])
    
    def get_gains(self,**kwargs):
        '''
        @brief get the gain at current market price to date of purchase
        @note this is currently naiively calculated as the current value - initial value
        @todo add reinvested dividends and tax by year
        '''
        # calculate owned duration (for tax reasons)
        now = datetime.now()
        duration = now-self['buy_date']
        gain_type = get_gain_type(duration)
        change = self.get_value()-self.get_cost_basis() # current value - start 
        return {'type':gain_type,'count':change}
        
        

#%% Inherit from security group to make accounts/portfolios
class SecurityGroup(FolioDict):
    '''
    @brief calculate information on groups of securities (can be nested)
    @param[in] children - list of securities (or SecurityGroups)
    @param[in/OPT] tax_status - None/'regular'|'exempt'|'deferred'
    '''
    def __init__(self,children=[],tax_status=None,**kwargs):
        '''@brief constructor'''
        super().__init__(children=children,tax_status=tax_status,**kwargs)
        # try to load from file if str is provided
        if isinstance(children,str): 
            data = FolioDict(); data.load(children)
            self.update(**data)
        
    def get_value(self,**kwargs):
        '''@brief get value of all securities'''
        val = np.sum([c.get_value(**kwargs) for c in self['children'].values()],axis=0)
        return val
        
    
#%% Some testing

if __name__=='__main__':
    
    symbols = ['T','VOO','INTC']
    counts =  [ 10,20,100 ]
    mysecs  = [Security(sym,count=c) for sym,c in zip(symbols,counts)]
    mysg = SecurityGroup(mysecs)
    
    dates = [datetime.now()-timedelta(days=i) for i in range(0,100,3)] # get last 100 days of values
    
    sg_vals=mysg.get_value(date=dates)


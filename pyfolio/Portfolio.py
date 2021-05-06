# -*- coding: utf-8 -*-
"""
@date Tue May  4 11:51:41 2021

@brief Base tools for designing a portfolio. All values are in USD currently

@author: aweiss
"""

from pyfolio.Securities.core import SecurityGroup
from pyfolio.Accounts import Account
    
#%% Class to hold a full portfolio (list of accounts)
class Portfolio(SecurityGroup):
    '''@brief a grouping of accounts'''
    def __init__(self,*args,**kwargs):
        '''@brief constructor'''
        super().__init__(*args,**kwargs)
        # assume all children are securities
        self['children'] = {cid:Account(**cv) for cid,cv in self['children'].items()}


#%% Some testing

if __name__=='__main__':
    
    from pyfolio.core import FolioDict
    
    test_folio = '../examples/example_portfolio.json'
    
    myfolio = Portfolio(test_folio)
    val = myfolio.get_value()
    
    fd = FolioDict()
    fd.load(test_folio)
    


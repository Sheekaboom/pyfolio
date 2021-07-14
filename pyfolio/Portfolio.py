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
    from pyfolio.Distributions import Distribution
    
    test_folio = '../examples/example_portfolio.json'
    test_folio = '/home/alec/Documents/portfolio_7-14-2021.json'
    
    myfolio = Portfolio(test_folio)
    val = myfolio.get_value()
    
    edge_acct = myfolio['children']['edge']
    
    fd = FolioDict()
    fd.load(test_folio)
    
    mydist = Distribution({
    #'cash': {'name':'cash','count':10000},
    'low_risk':{
        'percent': 0.25,
        'children':{
            'vtip':{'ticker':'VTIP','percent':0.4,'description':'TIPS ETF'},
            'bnd' :{'ticker':'BND','percent':0.6,'description':'Total bond ETF'}
                }
            },
    'medium_risk':{ 
        'percent':0.15,
        'children':{
            'usrt':{'ticker':'USRT','percent':0.65,'description':'broad REIT diversification'},
            #'eqi':{'ticker':'INDS','percent':0.30,'description':'industrial'},
            #'o'  :{'ticker':'O','percent':0.15,'description':'commercial real estate'},
            'old':{'ticker':'OLD','percent':0.35,'description':'long term care'},
            #'rez':{'ticker':'REZ','percent':0.10,'description':'residential real estate'}
                }
            },
    'high_risk':{
        'percent':0.60,
        'children':{
            'vb' :{'ticker':'VB','percent':0.30,'description':'small cap'},
            'vo' :{'ticker':'VO','percent':0.30,'description':'medium cap'},
            'vv' :{'ticker':'VV','percent':0.15,'description':'large cap'},
            'voo':{'ticker':'VOO','percent':0.25,'description':'S&P 500'}
            }
        }
    })
    
    orders = edge_acct.balance(mydist,print_flg=True)
    


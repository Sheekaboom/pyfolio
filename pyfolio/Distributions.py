# -*- coding: utf-8 -*-
"""
@date Sat May  8 15:54:01 2021

@brief Calculate portfolio distributions for creation and rebalancing

@author: aweis
"""

from pyfolio.core import FolioDict
from pyfolio.Securities import Security
import copy
import numpy as np

#%% some useful functions
def unpack_securities(mydict,parent_percent=100):
    '''
    @brief unpack nested values and get list of securities with associated percentages
    @param[in] mydict - dictionary to unpack from
    @return dictionary of securities with correct percentages
    '''
    unpacked = {}
    for k,v in mydict.items(): # go through each item in dictionary
        children = v.get('children',None) # try and get children
        
        if children is not None: # assume we have a nested dict
            percent = v.get('percent',100) # if not specified assume child specifies
            unpacked.update(unpack_securities(children,percent))
            
        else: # otherwise assume its a security
            cur_perc = v.get('percent',-1) # assume if its not specified count is specified
            sec = copy.deepcopy(v)
            sec['percent'] = cur_perc*parent_percent
            unpacked[k] = sec
            
    return unpacked

def print_orders(orders):
    '''@brief print out orders as instructions'''
    if not isinstance(orders,list):
        orders = [orders] # make sure its a list
    # now print
    order_fmt = '{buysell} {count} of {ticker} at {value}'
    ostrings = [] # strings for orders
    cost = 0
    for order in orders:
        order_info = {
            'buysell': 'BUY ' if order['count']>0 else 'SELL',
            'count'  : np.abs(order['count']),
            'ticker' : order['ticker'],
            'value'  : order['value']
            }
        ostrings.append(order_fmt.format(**order_info))
        cost += order['value']*order['count'] # update total cost
    print('--------------------------------')
    print('---           ORDERS         ---')
    print('--------------------------------')
    print('\n'.join(ostrings))
    print('--------------------------------')
    print('---  Total = {:8.2f}  ---'.format(cost))   
    print('--------------------------------')
    return ostrings
            

#%% Class to hold tihs
class Distribution(FolioDict):
    '''
    @brief class to specify a distribution of a portfolio
    @note all init args passed to folio dict
    '''
    def get_orders(self,cash):
        '''@brief get buy orders for each security needed to hit provided distribution. given available cash'''
        orders = []
        # first lets make all of our values securities
        unpacked = unpack_securities(self)
       
        # first lets remove anything specified by count
        count_secs = {k:Security(**v) for k,v in unpacked.items() if v.get('count',None) is not None}
        orders += [v for v in count_secs.values()] # add all count securities to orders
        cash -= np.sum([v.get_value() for v in count_secs.values()]) # remove the value of all our count specieifd securities
        # now lets calculate max cash per percent security
        ## First lets get the value of each security
        non_count_vals = {k:v for k,v in unpacked.items() if v.get('count',None) is None}
        values = {k:Security(**v,count=1).get_value() for k,v in non_count_vals.items()}
        ## maximum allowed cash per security
        max_cash = {k:cash*v.get('percent',None) for k,v in non_count_vals.items()} 
        ## now calculate how many shares that is and make securities out of it
        orders += [Security(**v,value=values[k],count=int(np.floor(max_cash[k]/values[k]))) for k,v in non_count_vals.items()]
        # and return all orders
        return orders
    
    
        
        


#%% Some testing
if __name__=='__main__':
    
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
                'eqi':{'ticker':'INDS','percent':0.30,'description':'industrial'},
                'o'  :{'ticker':'O','percent':0.15,'description':'commercial real estate'},
                'old':{'ticker':'OLD','percent':0.35,'description':'long term care'},
                'rez':{'ticker':'REZ','percent':0.10,'description':'residential real estate'}
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
    
    orders = mydist.get_orders(15000)
    print_orders(orders)
    

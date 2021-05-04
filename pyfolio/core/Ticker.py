# -*- coding: utf-8 -*-
"""
@date Tue May  4 12:53:58 2021

@brief Some custom extensions of Stock tickers

@author: aweis
"""

import yfinance
import urllib
import re
from datetime import datetime

#%% Custom ticker

class Ticker(yfinance.Ticker):
    '''
    @brief extension to add some functionality and common interfacing
    '''
    def get_url(self):
        '''@brief get the url webpage to pull further info from'''
        url = "https://finance.yahoo.com/quote/{}/profile?ltr=1".format(self.ticker)
        return url
    
    def get_page_data(self):
        '''@brief get the webpage data from self.get_url'''
        with urllib.request.urlopen(self.get_url()) as page:
            page_data = page.read().decode() # read and decode to str
        return page_data
        
    def get_expense_ratio(self,page_data=None):
        '''
        @brief retreive the net expense ratio (yfinance cant seem to do this...)
        @note this is VERY hardcoded right now
        @return expense ratio out of 1 (NOT 100 so NOT percentage)
        '''
        # get the page data if none provided
        if page_data is None: page_data = self.get_page_data()
        # and parse
        row = re.findall('expense.*?%</span>',pd.lower())
        if not row: raise Exception("Did not seem to find anything at for expense ratio when parsing the webpage...",
                                    " Likely there has been an update that we have not accounted for. Its pretty hardcoded right now")
        er = float(re.findall('[0-9]+.[0-9]+(?=%)',row[0])[0])/100 # divide by 100 to give decimal ratio
        return er
    
    def get_value(self,date=datetime.now()):
        '''
        @brief get the value of the security at a given date. 
                 If none provided get current value
        @note a iterable of dates is also acceptable
        '''
        # first get the historical data
        hist = self.history()
        # now clean input
        _date_isscalar = False
        if date=='all': # if all is provided
            date = hist.index
        elif not hasattr(date,'__iter__'): 
            _date_isscalar=True
            date = [date]
        # now get the data
        values = []
        for d in date:
            idx = hist.index.get_loc(d,method='nearest')
            hv = hist.iloc[idx]
            values.append(hv['Close'])
        if _date_isscalar: values = values[0]
        return values
    
        
        
#%% testing


if __name__=='__main__':
    
    mytick = Ticker('VOO')
    pd = mytick.get_page_data()
    #er = mytick.get_expense_ratio()
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 16:31:09 2021

@author: alec
"""
import xml.dom.minidom as mdom
#import lxml
import re
import bs4

#from ofxparse import OfxParser

#%% Things for ofx parser. Some of this is taken from
OFX_TAG_RE = { # currently according to standard, but downloaded file si different
    'root':'<[oO][fF][xX]>',
    'message':'msg[sr]*sv',
    'synchronization':None}
OFX_ALIAS = { # aliases to unload tag names into a more easily accessed structure
             'signon':{'tag':'signonmsgsrsv1'}
    }

def preprocess_ofx(ofx_str:str,lower=True):
        '''
        @brief take in a loaded ofx string and make it xml compliant
        @param[in] ofx_str - string with laoded ofx data
        @cite https://pypi.org/project/ofxparse/
        @return xml compatable string, dict of header values
        '''

        # find all closing tags as hints
        closing_tags = [t.upper() for t in re.findall(r'(?i)</([a-z0-9_\.]+)>',ofx_str)]

        # close all tags that don't have closing tags and
        # leave all other data intact
        # This was taken from ofxparse library, but could likely be written better... later maybe
        last_open_tag = None
        tokens = re.split(r'(?i)(</?[a-z0-9_\.]+>)', ofx_str)
        str_out = ''
        for token in tokens:
            is_closing_tag = token.startswith('</')
            is_processing_tag = token.startswith('<?')
            is_cdata = token.startswith('<!')
            is_tag = token.startswith('<') and not is_cdata
            is_open_tag = is_tag and not is_closing_tag \
                and not is_processing_tag
            if is_tag:
                if last_open_tag is not None:
                    str_out += ("</%s>" % last_open_tag)
                    last_open_tag = None
            if is_open_tag:
                tag_name = re.findall(r'(?i)<([a-z0-9_\.]+)>', token)[0]
                if tag_name.upper() not in closing_tags:
                    last_open_tag = tag_name
            str_out += token
            
        # lower the string unless requested otherwise
        if lower: str_out = str_out.lower()
            
        # now get the header assume the non-header portion starts with <ofx>
        head_end = str_out.lower().find('<ofx>')
        ## now split the strings
        head_str = str_out[:head_end]
        str_out = str_out[head_end:]
        ## and finally parse the header
        header = {hv.split(':')[0]:hv.split(':')[1] for hv in head_str.split() if hv}
        
        # finally clean a few things up
        str_out = re.sub('\n +','',str_out)
        
        return str_out,header
    
class OfxFile():
    '''
    @brief class to parse and contain an ofx file. parsed file stored in self.document
    @note much of this class is based off the levels defined in the ofx structure defintion
    '''
    def __init__(self,fpath,*args,**kwargs):
        '''@brief constructor'''
        # load the file into a string
        with open(fpath) as fp:
            self.raw_str = fp.read()
        # preprocess to xml compliance
        pp_str,header = preprocess_ofx(self.raw_str)
        self.header = header 
        # now load into our etree
        self.document = mdom.parseString(pp_str)
        #self.document = lxml.etree.fromstring(pp_str)
        
    def get_root(self): 
        return self.document.firstChild
        
    def get_messages(self):
        '''@brief get children (messages), but omit weird textnode strangeness'''
        return [c for c in self.get_root().childNodes if not isinstance(c,mdom.Text)]
    

#%% Some testing

if __name__=='__main__':
    
    import glob
    
    fpath = glob.glob('/home/alec/Downloads/*.ofx')[0]
    
    #with open(fpath) as fp:
    #    ofx = OfxParser().parse(fp)
    with open(fpath) as fp:
        ofx_str = fp.read()
    
    # lets just load a file
    myofx = OfxFile(fpath)
    msgs = myofx.get_messages()
    
    # now lets preprocess
    pp_str,hdata = preprocess_ofx(ofx_str)
    
    # and load in with dom
    #mydom = mdom.parseString(pp_str)
    # load in with beautiful soup
    #mysoup = bs4.BeautifulSoup(pp_str)
    
    
    
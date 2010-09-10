#!/usr/bin/python
#encoding: utf-8
"""
Author: Hsiao-Ting Wang
Date: 2010.5
Version: 1.0
File Name: Receive.py
"""
### for time evaluation
from time import time                                                 


### for AES                                                                                                                                   
from Crypto.Cipher import AES

# for plurk usage
import urllib,urllib2,cookielib
import simplejson as json
import Image,stepic
import os

# --- login Plurk----------------------------------------------
def login_plurk(apikey):
        lp = opener.open(get_api_url('/Users/login'),
                     encode({'username': 'martensite',
                             'password': '1123',
                             'api_key': apikey}))
        return lp.read()


# --- add Plurk----------------------------------------------
def add_plurk(addstr, apikey):
    ap = opener.open(get_api_url('/Timeline/plurkAdd'),
                     encode({'content': addstr,
                             'qualifier': 'shares',
                             'lang': 'tr_ch',
                             'api_key': apikey}))
    return ap.read()

# --- Plurk  response ----------------------------------------------
def response_plurk(resstr, plurkid, apikey):
    rp = opener.open(get_api_url('/Responses/responseAdd'),
                     encode({'content': resstr,
                             'qualifier': 'shares',
                             'lang': 'tr_ch',
                             'plurk_id': plurkid,
                             'api_key': apikey}))
    return rp.read()


#Clear the screen
os.system("clear")

### Plurk Setup
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
api_key = '0ZygrfNtpK5Von4w0xXXzbGBvdRQmJBt'
#api_key = 'F5u9WwGjNK16iiMYPlU18wPqLNnX6ZrX'
get_api_url = lambda x: 'http://www.plurk.com/API%s' % x
encode = urllib.urlencode

#### login    
login_plurk(api_key)

#### pooling timeline

#extract msg from PNG image
#open the secret image(PNG)

### add timestamp of starting to  extract encrypted data from image
t=time()
im2=Image.open('output.png')

print "Decoding the file output.png....."
#Stepic decode

s=stepic.Steganographer(im2)
rev_msg=s.decode()

#print "\nUndecrypted message:\n %r" % rev_msg 
extract_time=time()-t
print ("\nExtracting data from image taken: %f" % extract_time)

### add timestamp of starting decoding data
t=time()

###AES object
obj=AES.new('abcdefghijklmnds',AES.MODE_CBC)
# AES decode
dec_msg=obj.decrypt(rev_msg)


decode_time=time()-t
print ("Time of decoding data taken: %f" % decode_time)
print "\nYou got message: %r" % dec_msg

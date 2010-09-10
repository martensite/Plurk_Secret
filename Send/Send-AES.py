#!/usr/bin/env python
#encoding: utf-8

"""
Author: Hsiao-Ting Wang
Date: 2010.5
Version: 1.0
File Name: Send-AES.py
"""
### for AES
from Crypto.Cipher import AES

import random
#for Plurk usage
import urllib,urllib2,cookielib
#import simplejson as json
import json
#import cryptopng
#for the usage of hiding encrypted msg into image 
import Image,stepic
#for file processing(ex: file open)
import os
import random
#for establish a simple server
import BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from time import time
import subprocess
import socket
import twitpic

api_key = 'F5u9WwGjNK16iiMYPlU18wPqLNnX6ZrX'
##api_key = '0ZygrfNtpK5Von4w0xXXzbGBvdRQmJBt'

### Get IP addr
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("www.google.com",80))
IP_addr,port= s.getsockname()

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
## Print your IP address
print "\nYour are at:\t",IP_addr

#Print the menu for user
### Choose what service
print "Please choose which the social network service you want to use:\n"
try:
	service=int(raw_input( "\
        (1) Plurk \n  \
	(2) Twitter \n \
	(3) Facebook \n \
	\n  \
	>> ")) 
except(ValueError):
	##print "\nPlease enter the correct option again.\n"
	sys.exit()

print "Please choose the usage you want below:\n"
try:
	opt=int(raw_input( "\
        (1) Just test... \n  \
	(2) Message input: from user input (CLI) \n \
	(3) Message input: Open a file. \n \
	\n  \
	>> ")) 
except(ValueError):
	##print "\nPlease enter the correct option again.\n"
	sys.exit()

if opt== 1:
	#set up msg (fixed msg)
	msg='HAHA, YOU ARE SMART!'
if opt== 2:
	#(2)Message input:from user input (CLI) 
	msg=raw_input("\nPlease input your message:")
	print "Your message:",msg 


if opt== 3:
#(3)Message input: Open a file
	#filename=input("Please input filename:")
	filename='rfc4772.txt'
	fp=open(filename,"r")
	#fp=open("rfc4772.txt","rb")
	#print ("\nThe file size: ",fp.size())
	#fp_content=fp.read()
	msg=fp.read()
	print "File Content:",msg
	fp.close()

###start to record time, timestamp of starting encryption
t=time()
### Deal with msg length
len=len(msg)
append=16-(len%16)
#print 'Append'+str(append)+' X to your message.'
while append!=0:
    msg=msg+'X'
    append=append-1

#os.system("clear")
### AES encryption
obj=AES.new('abcdefghijklmnds',AES.MODE_CBC)
en_data=obj.encrypt(msg)
#print en_data
enc_time=time()-t
print ("Encryption time taken: %f \n" % enc_time )

### add timestamp to hiding data to image
t=time()
#Hiding in the PNG
im=Image.open('Screenshot.png')
"""
if not os.path.exists(im):
	print "Image not found."
"""
s=stepic.Steganographer(im)
#im2=s.encode(d)
im2=s.encode(en_data)
#im2=s.encode(fp_content)
append=str(random.randrange(1000))
#pic_name='output'+append+'.png'
pic_name='output.png'
im2.save(pic_name,'PNG')
#im2.save('output.png','PNG')
hiding_time=time()-t
print ("\n\nTime of hiding encrypted data to image: %f \n" % hiding_time)

#Plurk Setup
if service==1:
    ### timestamp of plurk start
    t=time()

    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    #api_key = '0ZygrfNtpK5Von4w0xXXzbGBvdRQmJBt'
    get_api_url = lambda x: 'http://www.plurk.com/API%s' % x
    encode = urllib.urlencode

    #### Plurk login    
    login_plurk(api_key)

    #### add Plurk
    ###Need add random words to prevent flood block...

    add_str='haha'
    fp = open("good_words.txt", "r")
    for line in fp.readlines():
        if line==random.randint(1,9):
            print line
            add_str=line

    ###  slogan
    #add_str = '[ISSUE'+ str(random.randint(0,99))+']'+'Please follow the below picture to operate...'
    #add_str = '[ISSUE'+ str(random.randint(0,99))+']'+'I do not know what happened.... Please Help Me!'
    add_str = '[ISSUE'+ str(random.randint(0,99))+']'+'Please review these items......'
    #add_str = '[ISSUE'+ str(random.randint(0,99))+']'+'Want to introduce you a new method...'

    str = add_plurk(add_str, api_key)

    fp.close()

    #### get the plurk_id
    p_str = '\"plurk_id\":'
    left_num = str.find(p_str)
    p_id = str[left_num+12:left_num+21]
    print "Plurk id: "+p_id+" post has been updated."

    ### response to the plurk
    if IP_addr==0:
        resstr= 'http://localhost:8888/output.png' 
    else:
        resstr= 'http://%s:8888/output.png' % IP_addr

    #resstr='http://'+os.system("ifconfig eth1 | grep '192.168' | awk '{print $3}' | sed -e s/.*://")+':8888/output.png'
    #print "Plurk %s" % resstr
    response_plurk(resstr, p_id, api_key)

    # Logout from Plurk
    fp = opener.open(get_api_url('/Users/logout'),
                    encode({'api_key': api_key}))
    print "Logout from Plurk..."

    plurk_time=time()-t
    print ("Time of processing Plurk post taken: %f \n" % plurk_time)

    #JSON of Plurk reply
    #if Plurk sucess, Setup the SimpleHTTPServer
    #using est evaluate the  reply



    HandlerClass = SimpleHTTPRequestHandler
    ServerClass  = BaseHTTPServer.HTTPServer
    Protocol     = "HTTP/1.0"

    port=8888
    server_address = (IP_addr, port)

    HandlerClass.protocol_version = Protocol
    httpd = ServerClass(server_address, HandlerClass)

    sa = httpd.socket.getsockname()
    os.system("clear")
    print "Serving HTTP on", sa[0], "port", sa[1], "..."
    httpd.serve_forever()

## Twitter (twitpic ) upload photos
if service==2:
       twit = twitpic.TwitPicAPI('rfc4340', '06111123')
       #twitpic_url = twit.upload('Screenshot.png') 
       # Post to Twitter 
       #twitpic_url = twit.upload('Screenshot.png', post_to_twitter=True) 
       twitpic_url = twit.upload('Screenshot.png', message='Guess what? I am smart~ haha', post_to_twitter=True) 
       print "Your picture with the secret message has been uploaded to "+ twitpic_url

if service3:

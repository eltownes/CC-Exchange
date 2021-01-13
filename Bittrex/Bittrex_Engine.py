import mod_MakeSignature
import mod_ParseJSON
import mod_JsonToCsv
import sys
import os
import csv
import time
import hashlib
import json
import requests
import urllib.parse

# https://docs.python.org/3.9/contents.html
# [] == list  ;  {} == object

# passed argument
option = int( sys.argv[1] )

# working directory
wd = os.path.dirname(__file__)

# bittrex keys
api_url_base = "https://api.bittrex.com/v3"
fileObject = open(wd + "\Bittrex API.txt", "r")
api_key = fileObject.read()
fileObject.close()
fileObject = open(wd + "\Bittrex Secret.txt", "r")
secret_key = fileObject.read()
fileObject.close()

# begin defs

def CurrTime():
    return str( int(round(time.time() * 1000)) )

def BuildBaseSignature():
    return api_timestamp + api_url + method + request_body_hash + ""

def CreateSignature( secret_key , baseSignature ):
    return mod_MakeSignature.MS(secret_key, baseSignature)

def BuildHeaders():
    return {
        "Api-Key": api_key,
        "Api-Timestamp": api_timestamp,
        "Api-Content-Hash": request_body_hash,
        "Api-Signature": signature
    }

def RequestGet( wd , symbol , fileName ):
    response = requests.get( api_url, headers=headers )
    print( response.json() )

    filePath = wd + "\\" + symbol + "\\" + fileName + ".txt"

    with open( filePath, 'w') as outfile:
        json.dump(response.json(), outfile)

    return response

def ParseJSON( wd , symbol , fileName , option):
    mod_JsonToCsv.JTC( wd , symbol , fileName , option )

def WhichMarket():
    fullPath = wd + "\Market.txt"
    fileObject = open( fullPath , "r" )
    marketStr = fileObject.read()
    marketStr = marketStr.strip('\n')
    return( marketStr )

# begin options

if option == 1: # GET ticker
    symbol = WhichMarket()
    api_timestamp = CurrTime()
    api_url = api_url_base + "/markets/" + symbol + "/ticker"
    method = 'GET'
    request_body = ''
    request_body_hash = hashlib.sha512( bytes(request_body, 'UTF-8') ).hexdigest()
    baseSignature = BuildBaseSignature()
    signature = CreateSignature(secret_key, baseSignature)
    headers = BuildHeaders()
    fileName = "Get Ticker"
    response = RequestGet( wd , symbol , fileName )
    ParseJSON( wd , symbol , fileName , "Get Ticker - bid" )
    ParseJSON( wd , symbol , fileName , "Get Ticker - ask" )

#
if option == 2: # GET order book
    symbol = WhichMarket()
    api_timestamp = CurrTime()
    api_url = api_url_base + "/markets/" + symbol + "/orderbook?"
    getParams = {'depth': '25'}
    api_url = api_url + urllib.parse.urlencode(getParams).replace('%3A',':')
    method = 'GET'
    request_body = ''
    request_body_hash = hashlib.sha512( bytes(request_body, 'UTF-8') ).hexdigest()
    baseSignature = BuildBaseSignature()
    signature = CreateSignature(secret_key, baseSignature)
    headers = BuildHeaders()
    fileName = "Get Orderbook"
    response = RequestGet( wd , symbol , fileName )
    ParseJSON( wd , symbol , fileName , "Get Orderbook - bid" )
    ParseJSON( wd , symbol , fileName , "Get Orderbook - ask" )


#

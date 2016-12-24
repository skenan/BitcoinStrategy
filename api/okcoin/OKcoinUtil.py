#!/usr/bin/python
# -*- coding: utf-8 -*-
#用于进行http请求，以及MD5加密，生成签名的工具类

import http.client
import urllib
import json
import hashlib
from urllib.parse import urljoin

import requests
def buildMySign(params,secretKey):
    sign = ''
    for key in sorted(params.keys()):
        sign += key + '=' + str(params[key]) +'&'
    data = sign+'secret_key='+secretKey
    return  hashlib.md5(data.encode("utf8")).hexdigest().upper()

def httpGet(url,resource,params=''):
    fullURL = urljoin(url, resource + "?" + params)
    response = requests.get(fullURL, timeout=20)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def httpPost(url,resource,params):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
    }
    fullURL = urljoin(url, resource)
    temp_params = urllib.parse.urlencode(params)
    response = requests.post(fullURL, temp_params, headers=headers, timeout=20)
    if response.status_code == 200:
        return response.json()
    else:
        return None


        
     

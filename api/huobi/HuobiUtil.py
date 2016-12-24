#coding=utf-8
import hashlib
import time
import urllib
import urllib.parse  
import urllib.request  
from api.api_key import Key
import json
import requests

#在此输入您的Key
ACCESS_KEY = Key['huobi']['ACCESS_KEY']
SECRET_KEY = Key['huobi']['SECRET_KEY']


HUOBI_SERVICE_API="https://api.huobi.com/apiv3"


'''
发送信息到api
'''
def send2api(pParams, extra):
	pParams['access_key'] = ACCESS_KEY
	pParams['created'] = int(time.time())
	pParams['sign'] = createSign(pParams)
	if(extra) :
		for k in extra:
			v = extra.get(k)
			if(v != None):
				pParams[k] = v
		#pParams.update(extra)
	tResult = httpRequest(HUOBI_SERVICE_API, pParams)
	return tResult

'''
生成签名
'''
def createSign(params):
	params['secret_key'] = SECRET_KEY;
	params = sorted(params.items(), key=lambda d:d[0], reverse=False)
	message = urllib.parse.urlencode(params)
	message=message.encode(encoding='UTF8')
	m = hashlib.md5()
	m.update(message)
	m.digest()
	sig=m.hexdigest()
	return sig

'''
request
'''
def httpRequest(url, params):
	headers = {
		"Content-type": "application/x-www-form-urlencoded",
	}

	postdata = urllib.parse.urlencode(params)
	# postdata = postdata.encode('utf-8')
	response = requests.post(url, postdata, headers=headers, timeout=20)
	if response.status_code == 200:
		return response.json()
	else:
		return None




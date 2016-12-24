#!/usr/bin/python
# -*- coding: utf-8 -*-
# encoding: utf-8
#客户端调用，用于查看API返回结果

from api.okcoin.OKcoinService import OKcoinService
import time


MAX_WAITING_TIME = 2

service = OKcoinService('BTC')


id = service.sell("7000", 0.01)

if id:
    order_info = service.getOrderInfo(id)
    print(order_info)
    if order_info.status != 2:
        print(service.cancelOrder(id))

'''
print (u' 现货深度 ')
print (OkcoinService.getDepth('btc_cny'))
print (OkcoinService.getTicker('btc_cny'))
print (OkcoinService.getAccountInfo())
'''
'''
print (OkcoinService.sell("btc_cny", "5900", 1))

#print (okcoinService.getOrderInfo("btc_cny", 7159839787))
print (OkcoinService.buy("btc_cny", "5000", 1))
#print(okcoinService.cancelOrder("btc_cny", 7159839787))

#print (u' 现货历史交易信息 ')
#print (okcoinSpot.trades())

#print (u' 用户现货账户信息 ')
#print (okcoinSpot.userinfo())

#print (u' 现货下单 ')
#print (okcoinSpot.trade('ltc_usd','buy','0.1','0.2'))

#print (u' 现货批量下单 ')
#print (okcoinSpot.batchTrade('ltc_usd','buy','[{price:0.1,amount:0.2},{price:0.1,amount:0.2}]'))

#print (u' 现货取消订单 ')
#print (okcoinSpot.cancelOrder('ltc_usd','18243073'))

#print (u' 现货订单信息查询 ')
#print (okcoinSpot.orderinfo('ltc_usd','18243644'))

#print (u' 现货批量订单信息查询 ')
#print (okcoinSpot.ordersinfo('ltc_usd','18243800,18243801,18243644','0'))

#print (u' 现货历史订单信息查询 ')
#print (okcoinSpot.orderHistory('ltc_usd','0','1','2'))
'''

   

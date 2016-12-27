#!/usr/bin/python
# -*- coding: utf-8 -*-
# 用于访问OKCOIN 现货REST API
from api.okcoin.OKcoinUtil import buildMySign, httpGet, httpPost
from api.api_key import Key
from model.account import Account
from model.depth import Depth
from model.order import Order
from tools.Format import *

URL = "https://www.okcoin.cn"
APIKEY = Key['okcoin']['ACCESS_KEY']
SECRETKEY = Key['okcoin']['SECRET_KEY']


class OKcoinService:
    def __init__(self, coinType):
        if coinType == 'BTC':
            self.symbol = 'btc_cny'
        elif coinType == 'LTC':
            self.symbol = 'ltc_cny'

    # 获取OKCOIN现货行情信息
    def getTicker(self):
        TICKER_RESOURCE = "/api/v1/ticker.do"
        params = ''
        if self.symbol:
            params = 'symbol=%(symbol)s' % {'symbol': self.symbol}
        return httpGet(URL, TICKER_RESOURCE, params)

    # 获取OKCOIN现货市场深度信息
    def getDepth(self, depth_size=5):
        DEPTH_RESOURCE = "/api/v1/depth.do"
        params = ''
        if self.symbol:
            params = 'symbol=%(symbol)s' % {'symbol': self.symbol}
        if depth_size:
            params += '&size=%s' % depth_size
        response = httpGet(URL, DEPTH_RESOURCE, params)
        if response:
            bids = sort_and_format(response['bids'], True)
            asks = sort_and_format(response['asks'], False)
            depth = Depth()
            depth.buy_price = bids[0]['price']
            depth.buy_amount = bids[0]['amount']
            depth.sell_price = asks[0]['price']
            depth.sell_amount = asks[0]['amount']
            return depth
        return None

    # 获取OKCOIN现货历史交易信息
    def trades(self):
        TRADES_RESOURCE = "/api/v1/trades.do"
        params = ''
        if self.symbol:
            params = 'symbol=%(symbol)s' % {'symbol': self.symbol}
        return httpGet(URL, TRADES_RESOURCE, params)

    # 获取用户现货账户信息
    def getAccountInfo(self):
        USERINFO_RESOURCE = "/api/v1/userinfo.do"
        params = {}
        params['api_key'] = APIKEY
        params['sign'] = buildMySign(params, SECRETKEY)
        response = httpPost(URL, USERINFO_RESOURCE, params)
        if response and response['result']:
            account = Account()
            account.btc_balance = float(response['info']['funds']['free']['btc'])
            account.cny_balance = float(response['info']['funds']['free']['cny'])
            account.btc_frozen = float(response['info']['funds']['freezed']['btc'])
            account.cny_frozen = float(response['info']['funds']['freezed']['cny'])
            return account
        return None

    # 市价买单
    def buyMarket(self, price):
        TRADE_RESOURCE = "/api/v1/trade.do"
        params = {
            'api_key': APIKEY,
            'symbol': self.symbol,
            'type': 'buy_market'
        }
        params['price'] = price
        params['sign'] = buildMySign(params, SECRETKEY)
        res = httpPost(URL, TRADE_RESOURCE, params)
        if res and res['result']:
            return res['order_id']
        return None

    # 市价卖单
    def sellMarket(self, amount):
        TRADE_RESOURCE = "/api/v1/trade.do"
        params = {
            'api_key': APIKEY,
            'symbol': self.symbol,
            'type': 'sell_market'
        }
        params['price'] = amount
        params['sign'] = buildMySign(params, SECRETKEY)
        res = httpPost(URL, TRADE_RESOURCE, params)
        if res and res['result']:
            return res['order_id']
        return None

    # 限价买单
    def buy(self, price, amount):
        TRADE_RESOURCE = "/api/v1/trade.do"
        params = {
            'api_key': APIKEY,
            'symbol': self.symbol,
            'type': "buy"
        }
        params['price'] = price
        params['amount'] = amount
        params['sign'] = buildMySign(params, SECRETKEY)
        res = httpPost(URL, TRADE_RESOURCE, params)
        if res and res['result']:
            return res['order_id']
        return None

    # 限价卖单
    def sell(self, price, amount):
        TRADE_RESOURCE = "/api/v1/trade.do"
        params = {
            'api_key': APIKEY,
            'symbol': self.symbol,
            'type': "sell"
        }
        params['price'] = price
        params['amount'] = amount
        params['sign'] = buildMySign(params, SECRETKEY)
        res = httpPost(URL, TRADE_RESOURCE, params)
        if res and res['result']:
            return res['order_id']
        return None

    # 现货取消订单
    def cancelOrder(self, orderId):
        CANCEL_ORDER_RESOURCE = "/api/v1/cancel_order.do"
        params = {
            'api_key': APIKEY,
            'symbol': self.symbol,
            'order_id': orderId
        }
        params['sign'] = buildMySign(params, SECRETKEY)
        res = httpPost(URL, CANCEL_ORDER_RESOURCE, params)
        if res and res['result']:
            return True
        return False

    # 现货订单信息查询
    def getOrderInfo(self, orderId):
        ORDER_INFO_RESOURCE = "/api/v1/order_info.do"
        params = {
            'api_key': APIKEY,
            'symbol': self.symbol,
            'order_id': orderId
        }
        params['sign'] = buildMySign(params, SECRETKEY)
        res = httpPost(URL, ORDER_INFO_RESOURCE, params)

        if res and res['result']:
            order_info = Order()
            order_info.order_id = res["orders"][0]["order_id"]
            order_info.price = res["orders"][0]["price"]
            order_info.avg_price = res["orders"][0]['avg_price']
            order_info.deal_amount = res["orders"][0]['deal_amount']
            order_info.status = res["orders"][0]["status"]
            return order_info
        return None

    # 现货获得历史订单信息
    def getNewDealOrders(self, status, currentPage=1, pageLength=10):
        ORDER_HISTORY_RESOURCE = "/api/v1/order_history.do"
        params = {
            'api_key': APIKEY,
            'symbol': self.symbol,
            'status': status,
            'current_page': currentPage,
            'page_length': pageLength
        }
        params['sign'] = buildMySign(params, SECRETKEY)
        return httpPost(URL, ORDER_HISTORY_RESOURCE, params)

    # 现货批量订单信息查询
    def ordersinfo(self, orderId, tradeType):
        ORDERS_INFO_RESOURCE = "/api/v1/orders_info.do"
        params = {
            'api_key': APIKEY,
            'symbol': self.symbol,
            'order_id': orderId,
            'type': tradeType
        }
        params['sign'] = buildMySign(params, SECRETKEY)
        return httpPost(URL, ORDERS_INFO_RESOURCE, params)

    # 现货批量下单
    def batchTrade(self, tradeType, orders_data):
        BATCH_TRADE_RESOURCE = "/api/v1/batch_trade.do"
        params = {
            'api_key': APIKEY,
            'symbol': self.symbol,
            'type': tradeType,
            'orders_data': orders_data
        }
        params['sign'] = buildMySign(params, SECRETKEY)
        return httpPost(URL, BATCH_TRADE_RESOURCE, params)

    @property
    def name(self):
        return "Okcoin"
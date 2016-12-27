# coding=utf-8
from api.huobi.HuobiUtil import *
from tools.Format import *
from model.account import Account
from model.depth import Depth
from model.order import Order
from tools import Utils
import json

ACCOUNT_INFO = "get_account_info"
GET_ORDERS = "get_orders"
ORDER_INFO = "order_info"
BUY = "buy"
BUY_MARKET = "buy_market"
CANCEL_ORDER = "cancel_order"
NEW_DEAL_ORDERS = "get_new_deal_orders"
ORDER_ID_BY_TRADE_ID = "get_order_id_by_trade_id"
SELL = "sell"
SELL_MARKET = "sell_market"


class HuobiService():
    def __init__(self, coinType):
        if coinType == 'BTC':
            self.coinType = 1
        elif coinType == 'LTC':
            self.coinType = 2

    '''
    获取账号详情
    '''

    def getAccountInfo(self):
        params = {"method": ACCOUNT_INFO}
        extra = {}
        response = send2api(params, extra)
        if response and "code" not in response:
            account = Account()
            account.btc_balance = float(response["available_btc_display"])
            account.cny_balance = float(response["available_cny_display"])
            account.btc_frozen = float(response["frozen_btc_display"])
            account.cny_frozen = float(response["frozen_cny_display"])
            return account
        return None

    '''
    获取所有正在进行的委托
    '''

    def getOrders(self):
        params = {"method": GET_ORDERS}
        params['coin_type'] = self.coinType
        extra = {}
        res = send2api(params, extra)
        return res

    '''
    获取订单详情
    @param coinType
    @param id


    状态　0未成交　1部分成交　2已完成　3已取消 4废弃（该状态已不再使用） 5异常 6部分成交已取消 7队列中
    '''

    def getOrderInfo(self, orderId):
        params = {"method": "order_info"}
        params['coin_type'] = self.coinType
        params['id'] = orderId
        extra = {}
        res = send2api(params, extra)
        if res and "code" not in res:
            order_info = Order()
            order_info.order_id = res['id']
            order_info.status = res['status']
            order_info.price = float(res['order_price'])
            order_info.deal_amount = float(res['processed_amount'])
            order_info.avg_price = float(res['processed_price'])
            return order_info
        return None

    '''
    限价买入
    @param coinType
    @param price
    @param amount
    @param tradePassword
    @param tradeid
    @param method
    '''

    def buy(self, price, amount):
        params = {"method": BUY}
        params['coin_type'] = self.coinType
        params['price'] = price
        params['amount'] = amount
        extra = {}
        extra['trade_password'] = None
        extra['trade_id'] = None
        res = send2api(params, extra)
        if res and "code" not in res:
            return res['id']
        return None

    '''
    限价卖出
    @param coinType
    @param price
    @param amount
    @param tradePassword
    @param tradeid
    '''

    def sell(self, price, amount):
        params = {"method": SELL}
        params['coin_type'] = self.coinType
        params['price'] = price
        params['amount'] = amount
        extra = {}
        extra['trade_password'] = None
        extra['trade_id'] = None
        res = send2api(params, extra)
        if res and "code" not in res:
            return res['id']
        return None

    '''
    市价买
    @param coinType
    @param amount
    @param tradePassword
    @param tradeid
    '''

    def buyMarket(self, amount):
        params = {"method": BUY_MARKET}
        params['coin_type'] = self.coinType
        params['amount'] = amount
        extra = {}
        extra['trade_password'] = None
        extra['trade_id'] = None
        res = send2api(params, extra)
        if res and "code" not in res:
            return res['id']
        return None

    '''
    市价卖出
    @param coinType
    @param amount
    @param tradePassword
    @param tradeid
    '''

    def sellMarket(self, qty):
        params = {"method": SELL_MARKET}
        params['coin_type'] = self.coinType
        params['amount'] = qty
        extra = {}
        extra['trade_password'] = None
        extra['trade_id'] = None
        res = send2api(params, extra)
        if res and "code" not in res:
            return res['id']
        return None

    '''
    查询个人最新10条成交订单
    @param coinType
    '''

    def getNewDealOrders(self):
        params = {"method": NEW_DEAL_ORDERS}
        params['coin_type'] = self.coinType
        extra = {}
        res = send2api(params, extra)
        return res

    '''
    根据trade_id查询oder_id
    @param coinType
    @param tradeid
    '''

    def getOrderIdByTradeId(self, tradeid):
        params = {"method": ORDER_ID_BY_TRADE_ID}
        params['coin_type'] = self.coinType
        params['trade_id'] = tradeid
        extra = {}
        res = send2api(params, extra)
        return res

    '''
    撤销订单
    @param coinType
    @param id
    '''

    def cancelOrder(self, orderId):
        params = {"method": CANCEL_ORDER}
        params['coin_type'] = self.coinType
        params['id'] = orderId
        extra = {}
        res = send2api(params, extra)
        if res and 'code' not in res:
            return True
        return False

    '''
    获取实时行情
    @param coinType #币种 1 比特币 2 莱特币
    '''

    def getTicker(self):
        if self.coinType == 1:
            url = "http://api.huobi.com/staticmarket/ticker_btc_json.js"
        else:
            url = "http://api.huobi.com/staticmarket/ticker_ltc_json.js"
        r = httpRequest(url, {})
        return json.loads(r)

    '''
    获取实时行情
    @param coinType:币种 1 比特币 2 莱特币
    @param depth_size:指定深度
    '''

    def getDepth(self, depth_size=1):

        if self.coinType == 1:
            url = "http://api.huobi.com/staticmarket/depth_btc_" + str(depth_size) + ".js"
        else:
            url = "http://api.huobi.com/staticmarket/depth_ltc_" + str(depth_size) + ".js"

        response = httpRequest(url, {})
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

    '''
    获取最少订单数量
    @param coinType:币种 1 比特币 2 莱特币
    火币上比特币交易及莱特币交易都是0.0001的整数倍
    比特币最小交易数量：0.001,莱特币最小交易数量：0.01
    '''

    @property
    def minimumOrderQty(self):
        if self.coinType == 1:
            return 0.001
        else:
            return 0.01

    '''
    获取最少交易金额
    火币上比特币交易及莱特币交易金额都是0.01的整数倍
    最小交易金额：1
    '''

    @property
    def minimumOrderCashAmount(self):
        return 1

    @property
    def name(self):
        return "Huobi"

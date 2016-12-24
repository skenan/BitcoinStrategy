#coding=utf-8

'''
本程序在 Python 3.3.0 环境下测试成功
使用方法：python HuobiTest.py
'''

from api.huobi.HuobiService import HuobiService
import time
HUOBI_BTC = 1
MAX_WAITING_TIME = 2
if __name__ == "__main__":

    service = HuobiService("BTC")
    order_id = service.buy(2000, 0.01)
    if order_id:
        order_info = service.getOrderInfo(order_id)
        print(order_info)
        if order_info.status != 2:
            print(service.cancelOrder(order_id))
    '''
    print("开始下达Huobi限价卖单...")
    print("下单价格 %s, 下单数量:%s， " % (5000, 0.1))
    res = service.buy(5000, 0.1)
    print(res)
    if 'result' in res and res['result'] == 'success':
        order_info = service.getOrderInfo(res['id'])
        if order_info["status"] != 2:
            print("Huobi限价卖单等待中")
            time.sleep(MAX_WAITING_TIME)
            order_info = service.getOrderInfo(res['id'])
        print(order_info)
        if order_info["status"] != 2:
            service.cancelOrder(res['id'])
        executed_qty = float(order_info["processed_amount"])
        print("成交数量:%s， 成交价格 %s" % (executed_qty, 5000))
    '''
    '''
    print ("获取账号详情")
    print (HuobiService.getAccountInfo())

    print ("获取所有正在进行的委托")
    print (HuobiService.getOrders(1))

    print ("获取订单详情")
    print (HuobiService.getOrderInfo(1,3096714115))

    print ("限价买入")
    print (HuobiService.buy(1,"1","0.01"))

    print ("限价卖出")
    print (HuobiService.sell(2,"100","0.2"))

    print ("市价买入")
    print (HuobiService.buyMarket(2,"30"))

    print ("市价卖出")
    print (HuobiService.sellMarket(2,"1.3452"))

    print ("查询个人最新10条成交订单")
    print (HuobiService.getNewDealOrders(1))

    print ("根据trade_id查询order_id")
    print (HuobiService.getOrderIdByTradeId(1,274424))

    print ("取消订单接口")
    print (HuobiService.cancelOrder(1,3096609180))
    '''
    '''
    print(HuobiService.getDepth(1, 1))
    print(HuobiService.getTicker(1))
    '''
#!/usr/bin/env python
# -*- coding: utf-8 -*-
from api.huobi.HuobiService import HuobiService
from api.okcoin.OKcoinService import OKcoinService
from tools import Utils
from tools.Log import Log
import time
import numpy as np

ORDER_RATIO = 0.8
MAX_WAITING_TIME = 3
MAX_HISTORY_SIZE = 5
MAX_PRICE_DIFF = 12
MAX_STD_DEV = 1.5
log = Log()


def buy(service, quantity, price, support_cancel):
    log.debug("开启买单")
    order_id = service.buy(price, quantity)
    if not order_id:
        log.warning("%s 买单下单失败" % service.name)
        return None

    order_info = service.getOrderInfo(order_id)
    retry_time = 0
    while retry_time < MAX_WAITING_TIME and order_info.status != 2:
        time.sleep(1)
        order_info = service.getOrderInfo(order_id)
        retry_time += 1

    if support_cancel and order_info.status != 2:
        service.cancelOrder(order_id)
        service.cancelOrder(order_id)
        order_info = service.getOrderInfo(order_id)

    executed_qty = order_info.deal_amount
    log.info("%s 买入 %.3f 比特币, 花费 %.2f" % (
        service.name, order_info.deal_amount, order_info.avg_price * order_info.deal_amount))
    return executed_qty if executed_qty > 0 else None


def sell(service, quantity, price, support_cancel):
    log.debug("开启卖单")
    order_id = service.sell(price, quantity)
    if not order_id:
        log.warning("%s 卖单下单失败" % service.name)
        return None

    order_info = service.getOrderInfo(order_id)
    retry_time = 0
    while retry_time < MAX_WAITING_TIME and order_info.status != 2:
        time.sleep(1)
        order_info = service.getOrderInfo(order_id)
        retry_time += 1

    if support_cancel and order_info.status != 2:
        service.cancelOrder(order_id)
        service.cancelOrder(order_id)
        order_info = service.getOrderInfo(order_id)

    executed_qty = order_info.deal_amount
    log.info("%s 卖出 %.3f 比特币, 收到 %.2f" % (
        service.name, order_info.deal_amount, order_info.avg_price * order_info.deal_amount))
    return executed_qty if executed_qty > 0 else None


def calculate_tradatable_amount(avaliable_amount, buy_amount, sell_amount):
    Qty = Utils.downRound(min(avaliable_amount, min(buy_amount, sell_amount) * ORDER_RATIO, 0.05), 3)
    return Qty if Qty > 0.01 else 0


def calculate_price_trend(data):
    # 需要根据最近1分钟的价格变化进行计算
    # False指价格下跌趋势, True指价格上升趋势
    x = np.arange(0, MAX_HISTORY_SIZE)
    y = np.array(data)
    z = np.polyfit(x, y, 1)
    return z[0] > 0


def go():
    huobi_service = HuobiService("BTC")
    okcoin_service = OKcoinService("BTC")
    history_prices = []
    while len(history_prices) < MAX_HISTORY_SIZE:
        okcoin_depth = okcoin_service.getDepth(3)
        history_prices.append(okcoin_depth.sell_price)

    while True:
        log.debug("正在分析..")

        # 先获取账户信息，耗时长
        huobi_account = huobi_service.getAccountInfo()
        okcoin_account = okcoin_service.getAccountInfo()

        log.info("可用人民币 %.4f, 可用比特币%.4f" % (
            huobi_account.cny_balance + okcoin_account.cny_balance,
            huobi_account.btc_balance + okcoin_account.btc_balance))
        huobi_depth = huobi_service.getDepth(3)
        okcoin_depth = okcoin_service.getDepth(3)
        history_prices.append(okcoin_depth.sell_price)
        history_prices = history_prices[-MAX_HISTORY_SIZE:]
        std_dev = np.std(history_prices)
        if std_dev > MAX_STD_DEV:
            log.info("波动性过大 %.4f,等待" % std_dev)
            continue
        sprend1 = huobi_depth.buy_price - okcoin_depth.sell_price
        sprend2 = okcoin_depth.buy_price - huobi_depth.sell_price

        if 0 < sprend1 <= MAX_PRICE_DIFF:  # 获利信号：OKcoin买，huobi卖
            Qty = min(huobi_account.btc_balance, okcoin_account.cny_balance / okcoin_depth.sell_price)
            Qty = calculate_tradatable_amount(Qty, huobi_depth.buy_amount, okcoin_depth.sell_amount)
            if Qty:
                log.info(
                    "获利信号：OKcoin买入 %.2f, Huobi卖出 %.2f, 数量 %.3f" % (okcoin_depth.sell_price, huobi_depth.buy_price, Qty))
                if not calculate_price_trend(history_prices):
                    # 先huobi卖， 再okcoin买
                    exec_amount = sell(huobi_service, Qty, huobi_depth.buy_price, True)
                    if exec_amount:
                        real_amount = buy(okcoin_service, Qty, okcoin_depth.sell_price, False)
                else:
                    # 先Okcoin买， 再Huobi卖
                    exec_amount = buy(okcoin_service, Qty, okcoin_depth.sell_price, True)
                    if exec_amount:
                        real_amount = sell(huobi_service, Qty, huobi_depth.buy_price, False)

        elif 0 <= sprend2 <= MAX_PRICE_DIFF:  # 获利信号：OKcoin卖，huobi买
            Qty = min(okcoin_account.btc_balance, huobi_account.cny_balance / huobi_depth.sell_price)
            Qty = calculate_tradatable_amount(Qty, okcoin_depth.buy_amount, huobi_depth.sell_amount)
            if Qty:
                log.info(
                    "获利信号：Huobi买入 %.2f, Okcoin卖出 %.2f, 数量 %.3f" % (huobi_depth.sell_price, okcoin_depth.buy_price, Qty))
                if calculate_price_trend(history_prices):
                    # 先huobi买，再okcoin卖
                    exec_amount = buy(huobi_service, Qty, huobi_depth.sell_price, True)
                    if exec_amount:
                        real_amount = sell(okcoin_service, Qty, okcoin_depth.buy_price, False)
                else:
                    # 先okcoin卖，再huobi买
                    exec_amount = sell(okcoin_service, Qty, okcoin_depth.buy_price, True)
                    if exec_amount:
                        real_amount = buy(huobi_service, Qty, huobi_depth.sell_price, False)
        # last_huobi_depth = huobi_depth
        # last_okcoin_depth = okcoin_depth
        time.sleep(1)

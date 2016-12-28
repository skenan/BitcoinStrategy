#!/usr/bin/env python
# -*- coding: utf-8 -*-

from strategy import arbitrage
import time

if __name__ == '__main__':

    while True:
        try:
            arbitrage.go()
        except Exception:
            arbitrage.log.warning("出错")
        finally:
            time.sleep(5)
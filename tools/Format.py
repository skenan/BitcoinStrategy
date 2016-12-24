#!/usr/bin/env python
# -*- coding: utf-8 -*-


def sort_and_format(l, reverse=False):
    l.sort(key=lambda x: float(x[0]), reverse=reverse)
    r = []
    for i in l:
        r.append({'price': float(i[0]), 'amount': float(i[1])})
    return r

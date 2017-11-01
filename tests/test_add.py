#!/usr/bin/env python
# coding:UTF-8
from __future__ import absolute_import, unicode_literals


# テストする関数
def add(a, b):
    return a + b


# テストコード 関数名はtest_ から始めるのがpytestでのお作法
def test_add():
    assert add(1, 1) == 2
    assert add(1, 2) != 2
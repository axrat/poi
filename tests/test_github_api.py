#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import requests


def test_api():
    # GitHubAPIを試験する
    url = "https://api.github.com/repos/vmg/redcarpet/issues?state=closed"
    headers = {'Accept-Encoding': 'identity, deflate, compress, gzip',
               'Accept': '*/*', 'User-Agent': 'python-requests/1.2.0',
               'Content-type': 'application/json; charset=utf-8',
               }
    response = requests.get(url, headers=headers)
    # HTTP Statusコードが200であること
    assert response.status_code == 200


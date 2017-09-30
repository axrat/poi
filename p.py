#!/usr/bin/env python3
# coding:utf-8

import pprint
import requests

def main():
    response = requests.get(
      'https://api.github.com/users/onoie',
        params={'foo': 'bar'})
    pprint.pprint(response.json())

if __name__== '__main__':
    print("HelloWorld!")
    main()

#!/usr/bin/env python3
# coding:utf-8

import sys
import os
import json
import pprint
import requests
import sqlite3
import argparse


def option():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))


def writeFile():
    f = open('text.txt', 'w')  # 書き込みモードで開く
    f.write("hello")  # 引数の文字列をファイルに書き込む
    f.close()  # ファイルを閉じる


def githubapi():
    response = requests.get('https://api.github.com/users/onoie')
    pprint.pprint(response.json())


def loadJson():
    print("loadJson")
    # 変数1 = open(‘読み込むJSONファイルのパス’, ‘r’)
    # 変数2 = json.load(変数1)


def sl(dbpath):
    conn = sqlite3.connect(dbpath)
    c = conn.cursor()
    # executeメソッドでSQL文を実行する
    create_table = '''create table users (id int, name varchar(64),age int, gender varchar(32))'''
    c.execute(create_table)
    # SQL文に値をセットする場合は，Pythonのformatメソッドなどは使わずに，
    # セットしたい場所に?を記述し，executeメソッドの第2引数に?に当てはめる値を
    # タプルで渡す．
    sql = 'insert into users (id, name, age, gender) values (?,?,?,?)'
    user = (1, 'Taro', 20, 'male')
    c.execute(sql, user)
    # 一度に複数のSQL文を実行したいときは，タプルのリストを作成した上で
    # executemanyメソッドを実行する
    insert_sql = 'insert into users (id, name, age, gender) values (?,?,?,?)'
    users = [
        (2, 'Shota', 54, 'male'),
        (3, 'Nana', 40, 'female'),
        (4, 'Tooru', 78, 'male'),
        (5, 'Saki', 31, 'female')
    ]
    c.executemany(insert_sql, users)
    conn.commit()
    select_sql = 'select * from users'
    for row in c.execute(select_sql):
        print(row)
    conn.close()


def sl2(dbpath):
    from sqlite3 import dbapi2 as sqlite
    dbname = "mysqlite.db"  # DBファイルの名前
    tablename = "personae"  # テーブルの名前
    con = sqlite.connect(dbname)
    # テーブルの存在確認
    cur = con.execute("SELECT * FROM sqlite_master WHERE type='table' and name='%s'" % tablename)
    if cur.fetchone() == None:  # 存在してないので作る
        con.execute("CREATE TABLE %s(id INTEGER, name TEXT, hp INTEGER, mp INTEGER)" % tablename)
        con.commit()
    con.close()


def args():
    argv = sys.argv
    argc = len(argv)
    if argc == 1:
        print('Usage: # python %s filename' % argv[0])
        quit()

    print('Command:%s' % argv[1])


def main():
    print("HelloWorld!")
    args()
    # dbpath = os.path.dirname(os.path.abspath(__file__)) + "/mysqlite.db"
    ## writeFile()
    # githubapi()
    # sl(dbpath)
    # sl2(dbpath)


if __name__ == '__main__':
    main()

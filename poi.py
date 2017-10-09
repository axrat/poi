#!/usr/bin/env python3
# coding:utf-8

import sys
import os
import json
import pprint
import requests
import sqlite3
import argparse
import textwrap


def readme():
    string = textwrap.dedent(
        '''
          {temp}
          Require [Command]
          poi hello/touch/test/githubapi/bitbucketapi
        ''').format(temp="README").strip()
    print(string)


def option():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                        help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                        const=sum, default=max,
                        help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print(args.accumulate(args.integers))


def touch():
    f = open(parent+'/ok', 'w')
    f.write("hello")
    f.close()


def githubapi(github_user = os.environ["GITHUB_USER"],
        github_token = os.environ["GITHUB_TOKEN"]):
    print("GithubAPI")
    print("User:%s,Token:%s" % (github_user,github_token))
    response = requests.get('https://api.github.com/users/'+github_user+'/repos')
    pprint.pprint(response.json())
    data = response.json()
    with open(parent+'/RESPONSE_GITHUB', 'w') as f:
        json.dump(data, f)


def bitbucketapi(bitbucket_user = os.environ["BITBUCKET_USER"],
        bitbucket_pass = os.environ["BITBUCKET_PASS"]):
    print("BitbucketAPI")
    print("User:%s,Pass:%s" % (bitbucket_user, bitbucket_pass))
    response = requests.get('https://api.bitbucket.org/2.0/repositories/'+bitbucket_user)
    pprint.pprint(response.json())
    data = response.json()
    with open(parent+'/RESPONSE_BITBUCKET', 'w') as f:
        json.dump(data, f)

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
    if cur.fetchone() is None:  # 存在してないので作る
        con.execute("CREATE TABLE %s(id INTEGER, name TEXT, hp INTEGER, mp INTEGER)" % tablename)
        con.commit()
    con.close()

def createJson():
    dict = {
        "name": "aaa",
        "age": 30
    }
    jsonstring = json.dumps(dict, indent=2)
    print(jsonstring)


def test():
    print("TestFunction")
    f = open(parent+'/RESPONSE_GITHUB', 'r')
    json_dict = json.load(f)
    jsonstring = json.dumps(json_dict, indent=2)
    print(jsonstring)


def main():
    argv = sys.argv
    argc = len(argv)
    if argc == 1:
        readme()
        quit()
    # print('Command:%s' % argv[1])
    p1 = argv[1]
    if p1 == "hello":
        print("HelloWorld!")
    elif p1 == "touch":
        touch()
    elif p1 == "test":
        test()
    elif p1 == "githubapi":
        githubapi()
    elif p1 == "bitbucketapi":
        bitbucketapi()
    elif p1 == "sqlite":
        # sl(dbpath)
        sl2(db_path)
    else:
        print('Unknown Command:%s' % p1)


if __name__ == '__main__':
    parent = os.path.dirname(os.readlink(os.path.abspath(__file__)))
    db_path = parent + "/mysqlite.db"
    main()

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
import collections as cl
from datetime import datetime

def readme():
    string = textwrap.dedent(
        '''
          {temp}
          Require [Command]
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


def slinit(dbpath):
    con = sqlite3.connect(dbpath)
    initializeTable(con, "stack", "create table stack (id int, val varchar(255))")
    return con


def slpush(con,val):
    c = con.cursor()
    sql = 'insert into stack (id,val) values (?,?)'
    query = [(datetime.now().strftime("%Y%m%d%H%M%S"),val),]
    c.executemany(sql, query)
    con.commit()
    print("push complete")


def slpop(con):
    c = con.cursor()
    select_sql = 'select * from stack'
    for row in c.execute(select_sql):
        print(row)
    con.close()


def slclear(con):
    c = con.cursor()
    c.execute('DELETE FROM stack')
    con.commit()
    con.close()


def slout(con,json_path):
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from stack")
    ys = cl.OrderedDict()
    for row in cur:
        # print(str(row["id"]) + "," + row["val"])
        data = cl.OrderedDict()
        ys[str(row["id"])] = data
        data["val"] = row["val"]
    cur.close()
    fw = open(json_path, 'w')
    json.dump(ys, fw, indent=2)
    print("out complete")


def initializeTable(con,table,create):
    cur = con.execute("SELECT * FROM sqlite_master WHERE type='table' and name='%s'" % table)
    if cur.fetchone() is None:
        print("NotFoundTable:%s" % table)
        con.execute(create)
        con.commit()
    # else:
    #     print("FoundTable:%s" % table)


def jsonLoad(json_path):
    f = open(json_path, 'r')
    json_data = json.load(f)  # JSON形式で読み込む
    name_list = ["honoka", "eri", "kotori", "umi", "rin", "maki", "nozomi", "hanayo", "niko"]
    for name in name_list:
        print("{0:6s} 身長：{1}cm BWH: ".format(name, json_data[name]["height"]), end="\t")
        for i in range(len(json_data[name]["BWH"])):
            print("{}".format(json_data[name]["BWH"][i]), end="\t")
        print()


def jsonWrite(json_path):
    name_list = ["honoka", "eri", "kotori", "umi", "rin", "maki", "nozomi", "hanayo", "niko"]
    height = [157, 162, 159, 159, 155, 161, 159, 156, 154]
    BWH = [[78, 58, 82], [88, 60, 84], [80, 58, 80], [76, 58, 80],[75, 59, 80], [78, 56, 83], [90, 60, 82], [82, 60, 83], [74, 57, 79]]
    ys = cl.OrderedDict()
    for i in range(len(name_list)):
        data = cl.OrderedDict()
        data["BWH"] = BWH[i]
        data["height"] = height[i]
        ys[name_list[i]] = data
    # print("{}".format(json.dumps(ys,indent=4)))
    fw = open(json_path, 'w')
    json.dump(ys, fw, indent=2)


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
    elif p1 == "test":
        test()
    elif p1 == "touch":
        touch()
    elif p1 == "githubapi":
        githubapi()
    elif p1 == "bitbucketapi":
        bitbucketapi()
    elif p1 == "push":
        if argc == 2:
            print("require push param")
            exit()
        slpush(slinit(dbpath),argv[2])
    elif p1 == "pop":
        slpop(slinit(dbpath))
    elif p1 == "out":
        slout(slinit(dbpath),parent + "/out.json")
    elif p1 == "clear":
        slclear(slinit(dbpath))
    elif p1 == "json":
        if argc == 2:
            print("require param load/write")
            exit()
        p2 = argv[2]
        if p2 == "write":
            jsonWrite(parent + "/myu_s.json")
        elif p2 == "load":
            jsonLoad(parent + "/myu_s.json")
        else:
            print("UnknownParam:%s" % p2)
    else:
        print('UnknownCommand:%s' % p1)


if __name__ == '__main__':
    parent = os.path.dirname(os.readlink(os.path.abspath(__file__)))
    dbpath = parent + "/mysqlite.db"
    main()

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

#import src.Prism
#p1 = src.Prism.Prism(10, 20, 30)
#print(p1.content())

# class MyClass:
#     """A simple example class"""         # 三重クォートによるコメント
#     def __init__(self):                  # コンストラクタ
#         self.name = ""
#
#     def getName(self):                   # getName()メソッド
#         return self.name
#
#     def setName(self, name):             # setName()メソッド
#         self.name = name
#
# a = MyClass()                            # クラスのインスタンスを生成
# a.setName("Tanaka")                      # setName()メソッドをコール
# print(a.getName())


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
    f = open(parent + '/ok', 'w')
    f.write("hello")
    f.close()


def api_request(url, user, token):
    # print("API Request User:%s,Token:%s" % (user, token))
    print("Request:%s" % url)
    return requests.get(url, auth=(user, token))


def github_request(url):
    return api_request(url, os.environ["GITHUB_USER"], os.environ["GITHUB_TOKEN"])


def bitbucket_request(url):
    return api_request(url, os.environ["BITBUCKET_USER"], os.environ["BITBUCKET_TOKEN"]).json()


def json_print(json):
    pprint.pprint(json)


def create_json(list):
    # print(list)
    json = cl.OrderedDict()
    for i in range(len(list)):
        data = cl.OrderedDict()
        # data["directory"] = "None"
        json[list[i]] = data
    return json


def github_repositories(repository_list, next):
    if next:
        response = github_request(next)
        json_data = response.json()
        for i in range(len(json_data)):
            repository_list.append(json_data[i]["name"])
        # print("Next:%s" % response.links["next"]["url"])
        if response.links.get("next"):
            return github_repositories(repository_list, response.links["next"]["url"])
    return repository_list


def bitbucket_repositories(repository_list, next):
    if next:
        json_data = bitbucket_request(next)
        json_data_values = json_data["values"]
        for i in range(len(json_data_values)):
            repository_list.append(json_data_values[i]["name"])
        return bitbucket_repositories(repository_list, json_data.get("next"))
    else:
        return repository_list


def db_list_push(con, sql, list):
    for i in range(len(list)):
        c = con.cursor()
        c.execute(sql, [list[i]])
        con.commit()
    print("list push complete")


def db_select(con, table):
    c = con.cursor()
    for row in c.execute("SELECT * FROM %s" % table):
        print(row)


def db_table_nodata(con, table):
    c = con.cursor()
    c.execute("select count(*) from %s" % table)
    return 0 == c.fetchone()[0]


def github_init():
    con = slinit(dbpath)
    repository_list = github_repositories([], 'https://api.github.com/users/' + os.environ["GITHUB_USER"] + '/repos')
    db_list_push(con, "INSERT INTO github (val) VALUES (?)", repository_list)
    con.close()
    print("complete")


def github_out(repository_list):
    fw = open(parent + '/RESPONSE_GITHUB', 'w')
    json.dump(create_json(repository_list), fw, indent=2)


def bitbucket_out(repository_list):
    fw = open(parent + '/RESPONSE_BITBUCKET', 'w')
    json.dump(create_json(repository_list), fw, indent=2)


def bitbucket_init():
    con = slinit(dbpath)
    repository_list = bitbucket_repositories([], 'https://api.bitbucket.org/2.0/repositories/' + os.environ["BITBUCKET_USER"])
    db_list_push(con, "INSERT INTO bitbucket (val) VALUES (?)", repository_list)
    con.close()
    print("complete")


def github_select():
    con = slinit(dbpath)
    db_select(con, "github")
    con.close()


def bitbucket_select():
    con = slinit(dbpath)
    db_select(con, "bitbucket")
    con.close()


def github_test():
    print("github test")
    con = slinit(dbpath)
    if db_table_nodata(con, "github"):
        print("github table is nodata")


def bitbucket_test():
    print("bitbucket test")
    con = slinit(dbpath)
    if db_table_nodata(con, "bitbucket"):
        print("bitbucket table is nodata")



def github_write():
    response = github_request('https://api.github.com/users/' + os.environ["GITHUB_USER"] + '/repos' + '?per_page=100')
    response = response.json()
    pprint.pprint(response)
    with open(parent + '/RESPONSE_GITHUB', 'w') as f:
        json.dump(response, f, indent=2)


def github_load():
    f = open(parent + '/RESPONSE_GITHUB', 'r')
    json_data = json.load(f)
    repo_count = len(json_data)
    # print("Repository:%s" % repo_count)
    for i in range(repo_count):
        print(json_data[i]["name"])



def bitbucket_write():
    bitbucket_user = os.environ["BITBUCKET_USER"]
    json_data = bitbucket_request('https://api.bitbucket.org/2.0/repositories/' + bitbucket_user)
    with open(parent + '/RESPONSE_BITBUCKET', 'w') as f:
        json.dump(json_data, f, indent=2)


def bitbucket_load():
    f = open(parent + '/RESPONSE_BITBUCKET', 'r')
    json_data = json.load(f)
    # print(json_data["next"])
    json_data = json_data["values"]
    for i in range(len(json_data)):
        print(json_data[i]["name"])


def slinit(dbpath):
    con = sqlite3.connect(dbpath)
    init_table(con, "github", "CREATE TABLE github (val VARCHAR(255))")
    init_table(con, "bitbucket", "CREATE TABLE bitbucket (val VARCHAR(255))")
    init_table(con, "stack", "CREATE TABLE stack (id INT, val VARCHAR(255))")
    return con


def slpush(con, val):
    c = con.cursor()
    sql = 'insert into stack (id,val) values (?,?)'
    query = [(datetime.now().strftime("%Y%m%d%H%M%S"), val), ]
    c.executemany(sql, query)
    con.commit()
    print("push complete")


def slpop(con):
    c = con.cursor()
    select_sql = 'select * from stack'
    for row in c.execute(select_sql):
        print(row)
    con.close()


def sldel(con, id):
    c = con.cursor()
    c.execute('DELETE FROM stack WHERE id = %s' % id)
    con.commit()
    con.close()
    print("delete complete")


def slclear(con):
    c = con.cursor()
    c.execute('DELETE FROM stack')
    con.commit()
    con.close()


def slout(con, json_path):
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


def init_table(con, table, create):
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
    BWH = [[78, 58, 82], [88, 60, 84], [80, 58, 80], [76, 58, 80], [75, 59, 80], [78, 56, 83], [90, 60, 82],
           [82, 60, 83], [74, 57, 79]]
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
    f = open(parent + '/RESPONSE_GITHUB', 'r')
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
    elif p1 == "github":
        if argc == 2:
            print("require param load/write")
            exit()
        p2 = argv[2]
        if p2 == "init":
            github_init()
        elif p2 == "select":
            github_select()
        elif p2 == "write":
            github_write()
        elif p2 == "load":
            github_load()
        elif p2 == "test":
            github_test()
        else:
            print("UnknownParam:%s" % p2)
    elif p1 == "bitbucket":
        if argc == 2:
            print("require param load/write")
            exit()
        p2 = argv[2]
        if p2 == "init":
            bitbucket_init()
        elif p2 == "select":
            bitbucket_select()
        elif p2 == "write":
            bitbucket_write()
        elif p2 == "load":
            bitbucket_load()
        elif p2 == "test":
            bitbucket_test()
        else:
            print("UnknownParam:%s" % p2)
    elif p1 == "push":
        if argc == 2:
            print("require push param")
            exit()
        slpush(slinit(dbpath), argv[2])
    elif p1 == "pop":
        slpop(slinit(dbpath))
    elif p1 == "out":
        slout(slinit(dbpath), parent + "/out.json")
    elif p1 == "clear":
        slclear(slinit(dbpath))
    elif p1 == "delete":
        if argc != 3:
            print("require param [id]")
            exit()
        sldel(slinit(dbpath), argv[2])
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

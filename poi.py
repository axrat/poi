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
    f = open(parent + '/ok', 'w')
    f.write("hello")
    f.close()


def githubapi_request(url,github_user=os.environ["GITHUB_USER"],github_token=os.environ["GITHUB_TOKEN"]):
    print("GithubAPI Request User:%s,Token:%s" % (github_user, github_token))
    print("RequestUrl:%s" % url)
    return requests.get(url, auth=(github_user, github_token))


def githubapi_repositories(repository_list, next):
    if next:
        response = githubapi_request(next)
        json_data=response.json()
        for i in range(len(json_data)):
            repository_list.append(json_data[i]["name"])
        # print("Next:%s" % response.links["next"]["url"])
        if response.links.get("next"):
            return githubapi_repositories(repository_list, response.links["next"]["url"])
    return repository_list


def githubapi_test():
    repository_list = []
    repository_list = githubapi_repositories(
        repository_list,
        'https://api.github.com/users/' + os.environ["GITHUB_USER"] + '/repos'
    )
    print(repository_list)
    rootDirct = cl.OrderedDict()
    for i in range(len(repository_list)):
        data = cl.OrderedDict()
        data["directory"] = "None"
        rootDirct[repository_list[i]] = data
    fw = open(parent + '/RESPONSE_GITHUB', 'w')
    json.dump(rootDirct, fw, indent=2)


def githubapi_write():
    response = githubapi_request('https://api.github.com/users/' + os.environ["GITHUB_USER"] + '/repos'+'?per_page=100')
    response = response.json()
    pprint.pprint(response)
    with open(parent + '/RESPONSE_GITHUB', 'w') as f:
        json.dump(response, f, indent=2)


def githubapi_load():
    f = open(parent + '/RESPONSE_GITHUB', 'r')
    json_data = json.load(f)
    repo_count = len(json_data)
    # print("Repository:%s" % repo_count)
    for i in range(repo_count):
        print(json_data[i]["name"])


def json_print(json):
    pprint.pprint(json)


def bitbucket_request(url, bitbucket_user=os.environ["BITBUCKET_USER"], bitbucket_pass=os.environ["BITBUCKET_TOKEN"]):
    # print("BitbucketAPI Request User:%s,Pass:%s" % (bitbucket_user, bitbucket_pass))
    print("RequestUrl:%s" % url)
    return requests.get(url, auth=(bitbucket_user, bitbucket_pass)).json()


def bitbucketapi_repositories(repository_list, next):
    if next:
        json_data = bitbucket_request(next)
        json_data_values = json_data["values"]
        for i in range(len(json_data_values)):
            repository_list.append(json_data_values[i]["name"])
        return bitbucketapi_repositories(repository_list,json_data.get("next"))
    else:
        return repository_list


def bitbucketapi_test():
    repository_list = []
    repository_list = bitbucketapi_repositories(
        repository_list,
        'https://api.bitbucket.org/2.0/repositories/' + os.environ["BITBUCKET_USER"]
    )
    # print(repository_list)
    rootDirct = cl.OrderedDict()
    for i in range(len(repository_list)):
        data = cl.OrderedDict()
        data["directory"] = "None"
        rootDirct[repository_list[i]] = data
    fw = open(parent + '/RESPONSE_BITBUCKET', 'w')
    json.dump(rootDirct, fw, indent=2)


def bitbucketapi_write():
    bitbucket_user = os.environ["BITBUCKET_USER"]
    json_data = bitbucket_request('https://api.bitbucket.org/2.0/repositories/' + bitbucket_user)
    with open(parent + '/RESPONSE_BITBUCKET', 'w') as f:
        json.dump(json_data, f, indent=2)


def bitbucketapi_load():
    f = open(parent + '/RESPONSE_BITBUCKET', 'r')
    json_data = json.load(f)
    # print(json_data["next"])
    json_data = json_data["values"]
    for i in range(len(json_data)):
        print(json_data[i]["name"])


def slinit(dbpath):
    con = sqlite3.connect(dbpath)
    initializeTable(con, "stack", "create table stack (id int, val varchar(255))")
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


def initializeTable(con, table, create):
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
    elif p1 == "githubapi":
        if argc == 2:
            print("require param load/write")
            exit()
        p2 = argv[2]
        if p2 == "write":
            githubapi_write()
        elif p2 == "load":
            githubapi_load()
        elif p2 == "test":
            githubapi_test()
        else:
            print("UnknownParam:%s" % p2)
    elif p1 == "bitbucketapi":
        if argc == 2:
            print("require param load/write")
            exit()
        p2 = argv[2]
        if p2 == "write":
            bitbucketapi_write()
        elif p2 == "load":
            bitbucketapi_load()
        elif p2 == "test":
            bitbucketapi_test()
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

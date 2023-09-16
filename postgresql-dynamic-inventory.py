#!/usr/bin/python2.7
# -*- coding:utf-8 -*-

import commands
import psycopg2
import json

output_dict={}

conn = psycopg2.connect(
    host = "192.168.196.120",
    port = 5000,
    database="postgres",
    user="postgres",
    password="password")

cur_group = conn.cursor()
cur_group.execute("""SELECT groupname FROM groups""")

for row_group in cur_group:
    group_dict={}
    grouphosts=[]
    groupvars={}

    cur_hosts = conn.cursor()
    cur_hosts.execute("""SELECT hostname FROM hosts WHERE groupname = %s""", (row_group[0],))

    for row_host in cur_hosts:
        grouphosts.append(row_host[0])

    group_dict["hosts"]=grouphosts
    group_dict["vars"]=groupvars
    output_dict[row_group[0]]=group_dict

cur_hosts = conn.cursor()
cur_hosts.execute("""SELECT DISTINCT hostname FROM hosts""")

meta_dict={}
hostvars={}

for row_host in cur_hosts:
    hostvar={}

    cur_hostvars = conn.cursor()
    cur_hostvars.execute("""SELECT varname,varvalue FROM hostvars WHERE hostname = %s""", (row_host[0],))

    for row_hostvar in cur_hostvars:
        hostvar[row_hostvar[0]]=row_hostvar[1]

    hostvars[row_host[0]]=hostvar

meta_dict["hostvars"]=hostvars
output_dict["_meta"]=meta_dict

print json.dumps(output_dict, indent=4)


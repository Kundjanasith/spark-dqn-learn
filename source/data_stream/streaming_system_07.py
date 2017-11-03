import urllib2 

ip = "http://203.154.114.153:10050"
cluster_url = ip+"/cluster"
clusters = []
file_cluster = open("historical_data/cluster.txt","w")
for cluster in urllib2.urlopen(cluster_url): 
    file_cluster.write(cluster)
    clusters.append(cluster[:-1])
file_cluster.close()
print(clusters)

cpu_users = []
cpu_systems = []
bytes_in = []
bytes_out = []
for c in clusters:
    print(c)

    file_cu = open("historical_data/system/"+c+"-cpu_user.xml","w")
    str_cu = ""
    for cu in urllib2.urlopen(ip+"/cpu_user/"+c):
        str_cu += cu
    file_cu.write(str_cu)
    cpu_users.append(str_cu)
    file_cu.close()

    file_cs = open("historical_data/system/"+c+"-cpu_system.xml","w")
    str_cs = ""
    for cs in urllib2.urlopen(ip+"/cpu_system/"+c):
        str_cs += cs
    file_cs.write(str_cs)
    cpu_systems.append(str_cs)
    file_cs.close()

    file_bi = open("historical_data/system/"+c+"-bytes_in.xml","w")
    str_bi = ""
    for bi in urllib2.urlopen(ip+"/bytes_in/"+c):
        str_bi += bi
    file_bi.write(str_bi)
    bytes_in.append(str_bi)
    file_bi.close()

    file_bo = open("historical_data/system/"+c+"-bytes_out.xml","w")
    str_bo = ""
    for bo in urllib2.urlopen(ip+"/bytes_out/"+c):
        str_bo += bo
    file_bo.write(str_bo)
    bytes_out.append(str_bo)
    file_bo.close()

str_sp = ""
for sp in urllib2.urlopen(ip+"/spark"): 
    str_sp += sp
str_date = str_sp[0:17]
str_date = str_date.replace("/","-").replace(" ","_") + "_spark.txt" 
file_spark = open("historical_data/spark/"+str_date,"w")
file_spark.write(str_sp)
file_spark.close()



def date_format(date):
    return date.replace("/","-").replace(" ","_")[2:]

def value_format(value):
    return float(value)

for c in clusters:

    file_cu = open("historical_data/system/"+c+"-cpu_user.xml","r")
    content_file_cu = []
    for cu in file_cu:
        content_file_cu.append(cu)
    f_cu = open("historical_data/system/csv/"+c+"-cpu_user.csv","w")
    for i in content_file_cu[35:len(content_file_cu)-3]:
        line = i.split("</v></row>\n")[0].split("<row><v> ")
        if len(line) == 2:
            key = date_format(line[0].split(" +07 / ")[0][8:])
            value = value_format(line[1][:-1])
            f_cu.write(key+","+str(value)+"\n")
    f_cu.close()

    file_cs = open("historical_data/system/"+c+"-cpu_system.xml","r")
    content_file_cs = []
    for cs in file_cs:
        content_file_cs.append(cs)
    f_cs = open("historical_data/system/csv/"+c+"-cpu_system.csv","w")
    for i in content_file_cs[35:len(content_file_cs)-3]:
        line = i.split("</v></row>\n")[0].split("<row><v> ")
        if len(line) == 2:
            key = date_format(line[0].split(" +07 / ")[0][8:])
            value = value_format(line[1][:-1])
            f_cs.write(key+","+str(value)+"\n")
    f_cs.close()

    file_bi = open("historical_data/system/"+c+"-bytes_in.xml","r")
    content_file_bi = []
    for bi in file_bi:
        content_file_bi.append(bi)
    f_bi = open("historical_data/system/csv/"+c+"-bytes_in.csv","w")
    for i in content_file_bi[35:len(content_file_bi)-3]:
        line = i.split("</v></row>\n")[0].split("<row><v> ")
        if len(line) == 2:
            key = date_format(line[0].split(" +07 / ")[0][8:])
            value = value_format(line[1][:-1])
            f_bi.write(key+","+str(value)+"\n")
    f_bi.close()

    file_bo = open("historical_data/system/"+c+"-bytes_out.xml","r")
    content_file_bo = []
    for bo in file_bo:
        content_file_bo.append(bo)
    f_bo = open("historical_data/system/csv/"+c+"-bytes_out.csv","w")
    for i in content_file_bo[35:len(content_file_bo)-3]:
        line = i.split("</v></row>\n")[0].split("<row><v> ")
        if len(line) == 2:
            key = date_format(line[0].split(" +07 / ")[0][8:])
            value = value_format(line[1][:-1])
            f_bo.write(key+","+str(value)+"\n")
    f_bo.close()

import pandas as pd
import numpy as np

for c in clusters:
    cpuUser = pd.read_csv("historical_data/system/csv/"+c+"-cpu_user.csv",header=None)
    cpuUser.columns = ['time', 'cpu_user']
    cpuSystem = pd.read_csv("historical_data/system/csv/"+c+"-cpu_system.csv",header=None)
    cpuSystem.columns = ['time', 'cpu_system']
    result = cpuUser.join(cpuSystem.set_index('time'), on='time')
    byteIn = pd.read_csv("historical_data/system/csv/"+c+"-bytes_in.csv",header=None)
    byteIn.columns = ['time', 'bytes_in']
    result = result.join(byteIn.set_index('time'), on='time')
    byteOut = pd.read_csv("historical_data/system/csv/"+c+"-bytes_out.csv",header=None)
    byteOut.columns = ['time', 'bytes_out']
    result = result.join(byteOut.set_index('time'), on='time')
    result.to_csv("historical_data/system/node_csv/"+c+".csv", index=False)

for c in clusters:
    file = pd.read_csv("historical_data/system/node_csv/"+c+".csv")
    file.groupby(['time']).mean()
    file.to_csv("historical_data/system/node_csv_z/"+c+".csv", index=False)

import os
os.system("rm -rf historical_data/system/system.csv")
index = 0
worker = 0
for c in clusters:
    if "worker" in c:
        worker = worker + 1
        if index == 0:
            file = pd.read_csv("historical_data/system/node_csv_z/"+c+".csv")
            file.to_csv("historical_data/system/system.csv", index=False)
        else:
            file_res = pd.read_csv("historical_data/system/system.csv")
            file = pd.read_csv("historical_data/system/node_csv_z/"+c+".csv")
            file_res = pd.concat([file_res,file]).groupby('time').mean()
            file_res.to_csv("historical_data/system/system.csv")
        index = index + 1

file = pd.read_csv("historical_data/system/system.csv")
file['worker'] = worker
file.to_csv("historical_data/system/system.csv", index=False)

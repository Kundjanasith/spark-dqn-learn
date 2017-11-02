import glob
import pandas as pd
from datetime import datetime
from time import mktime

path = 'historical_data/spark'
filenames = glob.glob(path + "/*.txt")

file_lists = []
for filename in filenames:
    file_lists.append(filename)

def MB2KB(x):
    res = 0
    if x[-2:]=="MB":
        res = float(x[:-2])*1000
    if x[-2:]=="KB":
        res = float(x[:-2])
    return res

def date_format(date):
    return date.replace("/","-").replace(" ","_")

def date_norm(date):
    year = "20" + date.split("/")[0]
    month = date.split("/")[1]
    day = date.split("/")[2].split(" ")[0]
    hour = date.split(":")[0].split(" ")[1]
    minu = date.split(":")[1]
    sec = date.split(":")[2]
    return [int(year),int(month),int(day),int(hour),int(minu),int(sec)]

for path in file_lists:
    file = open(path, "r") 
    blockManagerInfo_list = []
    memoryStore_list = []
    status = "NONE"
    index_start = 0
    index_stop = 0
    start_time = "start_time"
    stop_time = "stop_time"
    for line in file:
        l = line.split(" ")
        if len(l) > 3:
            if l[3] == "MemoryStore:": #transformation
                memoryStore_list.append(l)
            if l[3] == "BlockManagerInfo:": #action
                blockManagerInfo_list.append(l)
        if "java.lang.OutOfMemoryError:" in line:
            status = "-1"
            # print(path+":"+status)
        if index_stop == 0:
            stop_time = line
        if index_start == 0:
            start_time = line
        index_start = index_start + 1

    if status != "-1" and start_time != "start_time" and stop_time != "stop_time":
        startTime = start_time.split(" ")[0] + " " + start_time.split(" ")[1]
        stopTime = stop_time.split(" ")[0] + " " + stop_time.split(" ")[1]
        # print(startTime)
        startNorm = date_norm(startTime)
        startDate = datetime(startNorm[0], startNorm[1], startNorm[2], startNorm[3], startNorm[4], startNorm[5])
        startDate = mktime(startDate.timetuple())
        # print(startDate)
        # print(stopTime)
        stopNorm = date_norm(stopTime)
        stopDate = datetime(stopNorm[0], stopNorm[1], stopNorm[2], stopNorm[3], stopNorm[4], stopNorm[5])
        stopDate = mktime(stopDate.timetuple())
        # print(stopDate)
        status = str(stopDate - startDate)
        # print(path+":"+status)

    input_path = path.split("/")[2][:-3]+"csv"
    file_output = open("historical_data/spark/csv/"+input_path,"w")
    file_output.write("time,status,mem_trans,mem_act\n")
    for m in memoryStore_list:
        time = m[0]+" "+m[1]
        time = date_format(time)
        if m[4]=="Block":
            size = (m[13]+m[14])[:-1]
            free = (m[16]+m[17])[:-2]
            file_output.write(time+","+status+","+str(MB2KB(size))+",0"+"\n")
    for b in blockManagerInfo_list:
        time = m[0]+" "+m[1]
        time = date_format(time)
        if b[4]=="Added": 
            storage = b[7]
            size = (b[11]+b[12])[:-1]
            free = (b[14]+b[15])[:-2]
            file_output.write(time+","+status+",0,"+str(MB2KB(size))+"\n")
        if b[4]=="Removed":
            storage = b[9]
            if storage == "disk":
                size = (b[11]+b[12])[:-2]
                file_output.write(time+","+status+",0,"+str(MB2KB(size))+"\n")
            if storage ==  "memory":
                size = (b[11]+b[12])[:-1]
                free = (b[14]+b[15])[:-2]
                file_output.write(time+","+status+",0,"+str(MB2KB(size))+"\n")
        if b[4]=="Updated":
            storage = b[7]
            size = (b[12]+b[13])[:-1]
            free = (b[16]+b[17])[:-2]
            file_output.write(time+","+status+",0,"+str(MB2KB(size))+"\n")
    file_output.close()
    # f_group = pd.read_csv("historical_data/spark/csv/"+input_path)
    # f_group = f_group.groupby('time').mean()
    # f_group.to_csv("historical_data/spark/csv/"+input_path)

pathZ = 'historical_data/spark/csv'
filenamesZ = glob.glob(pathZ + "/*.csv")

import os
os.system("rm -rf historical_data/spark/spark.csv")
index = 0
for filenameZ in filenamesZ:
    if index == 0:
        file = pd.read_csv(filenameZ)
        file.to_csv("historical_data/spark/spark.csv", index=False)
    else:
        file_res = pd.read_csv("historical_data/spark/spark.csv")
        file = pd.read_csv(filenameZ)
        file_res = file_res.append(file)
        file_res = file_res.sort_values(['time'])
        file_res.to_csv("historical_data/spark/spark.csv", index=False)
    index = index + 1

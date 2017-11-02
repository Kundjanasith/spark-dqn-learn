#SparkLog class to analyse Spark log
import numpy as np
class SparkLog:

    __memoryStoreList = []
    __blockManagerInfoList = []

    def __init__(self,inputPath):
        spark_file = open(inputPath, "r")  
        for line in spark_file:
            l = line.split(" ")
            if l[2]=="INFO":
                if l[3]=="MemoryStore:":
                    self.__memoryStoreList.append(line)
                if l[3]=="BlockManagerInfo:":
                    self.__blockManagerInfoList.append(line)

    def __MB2KB(self,x):
        res = 0
        if x[-2:]=="MB":
            res = float(x[:-2])*1000
        if x[-2:]=="KB":
            res = float(x[:-2])
        return res

    def getMemoryTransformation(self):
        res = []
        for mt in self.__memoryStoreList:
            m = mt.split(" ")
            if m[4]=="Block":
                size = (m[13]+m[14])[:-1]
                usage = (m[16]+m[17])[:-2]
                res.append(self.__MB2KB(usage))
        return np.mean(res)
    
    def getMemoryAction(self):
        res = []
        for ma in self.__blockManagerInfoList:
            m = ma.split(" ")
            if m[4]=="Added": 
                storage = m[7]
                size = (m[11]+m[12])[:-1]
                usage = (m[14]+m[15])[:-2]
                res.append(self.__MB2KB(usage))
            if m[4]=="Removed":   
                storage = m[9]
                if storage == "disk":
                    size = (m[11]+m[12])[:-2]
                    res.append(self.__MB2KB(size))
                if storage ==  "memory":
                    size = (m[11]+m[12])[:-1]
                    usage = (m[14]+m[15])[:-2]
                    res.append(self.__MB2KB(usage))
            if m[4]=="Updated":
                storage = m[7]
                current = (m[12]+m[13])[:-1]
                original = (m[16]+m[17])[:-2]
                res.append(self.__MB2KB(current))
        return np.mean(res)

    
    


   
    

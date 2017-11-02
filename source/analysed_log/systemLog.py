#SystemkLog class to analyse Systemlog
class SystemLog:

    __cpuLine = ""
    __networkLine = ""

    def __init__(self,inputPath):
        system_file = open(inputPath, "r")  
        count_line = 0
        for line in system_file:
            count_line = count_line + 1
            if count_line == 4:
                self.__cpuLine = line
            if count_line == 9:
                self.__networkLine = line
   
    def getCpuUser(self):
        return self.__cpuLine.split(" ")[2][:-1]
    
    def getCpuSyst(self):
        return self.__cpuLine.split(" ")[4][:-1]

    def getCpuIdle(self):
        return self.__cpuLine.split(" ")[6][:-1]

    def getNetworkIn(self):
        return self.__networkLine.split(" ")[2].split("/")[0]

    def getNetworkOut(self):
        return self.__networkLine.split(" ")[4].split("/")[0]
       

import sys
from sparkLog import SparkLog 
from systemLog import SystemLog

def printList(lists):
    for l in lists:
        print(l)

print("Spark log analysis start . . .")

spark_file = SparkLog(sys.argv[1])
memoryTransformation = spark_file.getMemoryTransformation()
memoryAction = spark_file.getMemoryAction()
print("Memory Usage Transformation (KB) : ", memoryTransformation)
print("Memory Usage Action (KB) : ", memoryAction)

print("Spark log analysis complete . . .")

print("System log analysis start . . .")

system_file = SystemLog(sys.argv[2])
cpuUser = system_file.getCpuUser()
cpuSyst = system_file.getCpuSyst()
cpuIdle = system_file.getCpuIdle()
networkIn = system_file.getNetworkIn()
networkOut = system_file.getNetworkOut()
print("CPU usage of user processes (%) : ", cpuUser)
print("CPU usage of system processes (%) : ", cpuSyst)
print("CPU usage of idle processes (%) : ", cpuIdle)
print("The number of packets inbound network (packets) : ", networkIn)
print("The number of packets outbound network (packets) : ", networkOut)

print("System log analysis complete . . .")
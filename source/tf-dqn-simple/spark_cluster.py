import os
import numpy as np


class SparkCluster:
    def __init__(self):
        # parameterspyt
        self.name = os.path.splitext(os.path.basename(__file__))[0]
        self.action = 0
        self.max_node = 10
        cluster = open("../data_stream/historical_data/cluster.txt","r")
        self.current_node = 0
        for line in cluster:
            if "worker" in line:
                self.current_node = self.current_node + 1
        action_out = range(1,self.max_node)
        action_in = reversed(range(-(self.max_node-1),0))
        prob_out = self.max_node - self.current_node
        prob_in = self.current_node - 1
        self.enable_actions = (0,)
        for out in action_out:
            if prob_out == 0:
                break
            self.enable_actions = self.enable_actions + (out,)
            prob_out = prob_out - 1
        for inn in action_in:
            if prob_in == 0:
                break
            self.enable_actions = self.enable_actions + (inn,)
            prob_in = prob_in - 1
        
        # variables
        self.reset()

    def update(self, action):
        """
        action:
            0: do nothing
            y: scale-out y nodes
            -y: scale-in y nodes
            1 < y < N
        """
        self.action = action
        if self.action == 0 :
            self.current_node = self.current_node
        if self.action > 0 :
            temp = self.current_node
            self.current_node = self.current_node + self.action
            if self.current_node > self.max_node:
                self.current_node = temp
        if self.action < 0 :
            temp = self.current_node
            self.current_node = self.current_node + self.action
            if self.current_node < 1:
                self.current_node = temp
        # self.current_node = self.current_node + action

    def observe(self, memA, memT, cpuU, cpuS, netI, netO, execu, t, n):
        self.reward = 0
        self.terminal = False
        self.max_node = n
        self.time = t*60
        if t == 0:
            execu = 0
        else:
            execu = (self.time - float(execu)) / self.time
        if self.max_node == 0 or self.max_node == 1:
            nodes = 0
        else:
            al = self.current_node + self.action
            nodes = 1 - 2*((al-1)/(self.max_node-1))
        memA = (500000 - float(memA)) / 500000
        memT = (500000 - float(memT)) / 500000
        cpuU = (50 - float(cpuU)) / 50
        cpuS = (50 - float(cpuS)) / 50
        netI = (500000 - float(netI)) / 500000
        netO = (500000 - float(netO)) / 500000
        self.reward = ( nodes + 0.5*memA + 0.5*memT + 0.5*cpuU + 0.5*cpuS + 0.5*netI + 0.5*netO + execu )/ 5
        if 1 < execu < -1 or self.reward < -1 or nodes > n or nodes < 1:
            self.reward = -1
            self.terminal = True
        res = np.array([[memA,memT,cpuU,cpuS,netI,netO,execu,self.current_node]])
        return res, self.reward, self.terminal

    def execute_action(self, action):
        self.update(action)

    def reset(self):
        self.reward = 0
        self.terminal = False

from __future__ import division

import argparse
import os
import sys

import matplotlib.animation as animation
import matplotlib.pyplot as plt

from spark_cluster import SparkCluster
from dqn_agent import DQNAgent

if __name__ == "__main__":
    max_nodes = int(sys.argv[1])
    time_constraint = int(sys.argv[2])*60
    env = SparkCluster()
    agent = DQNAgent(env.enable_actions, env.name)
    agent.load_model("kitwai_models/spark")

    # variables
    file = open("../data_stream/historical_data/data/current.csv","r")
    next(file)
    rewards = []
    nodes = []
    state_t_1, reward_t, terminal = env.observe(0,0,0,0,0,0,0,0,0)
    for line in file:
        arr = line.split(",")
        execu, memT, memA, cpuU, cpuS, netI, netO = arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7]
        state_t_1, reward_t, terminal = env.observe(memA,memT,cpuU,cpuS,netI,netO,execu,time_constraint,max_nodes)
        print("NODE : "+str(state_t_1[0][7]))
        print("REWARD : "+str(reward_t))
        rewards.append(reward_t)
        nodes.append(state_t_1[0][7])
    print(min(rewards))
    print(nodes[rewards.index(max(rewards))])

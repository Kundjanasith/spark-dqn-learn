from __future__ import division
import os
from flask import Flask, request, jsonify, send_from_directory
from json import dumps, loads
app = Flask(__name__, static_folder=".", template_folder=".")
import argparse
import os
import sys
from spark_cluster import SparkCluster
from dqn_agent import DQNAgent

env = SparkCluster()
agent = DQNAgent(env.enable_actions, env.name)

@app.after_request
def add_headers(response):
    agent.load_model("kitwai_models/spark")
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization, data')
    return response

@app.route("/")
def hello():
    return "<h1>Kitwai : Deep Q-Network model service</h1><h2>[kundjanasith@datascienceth.com]</h2>"

@app.route("/train/<int:node>/<int:time>", methods=['GET'])
def train(node,time):
    n = node #The number of maximum worker nodes
    t = time #The time constraint
    max_nodes = int(n)
    time_constraint = int(t)*60
    file = open("../data_stream/historical_data/data/current.csv","r")
    next(file)
    rewards = []
    nodes = []
    for line in file:
        arr = line.split(",")
        execu, memT, memA, cpuU, cpuS, netI, netO = arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7]
        state_t_1, reward_t, terminal = env.observe(memA,memT,cpuU,cpuS,netI,netO,execu,t,n)
        rewards.append(reward_t)
        nodes.append(state_t_1[0][7])
    re = max(rewards)
    no = nodes[rewards.index(max(rewards))]
    # os.system("python model.py"+str(n)+" "+str(t))
    return str(no)+"|"+str(re)

@app.route("/log1", methods=['GET'])
def log1():
    path = "trainZ.txt"
    return send_from_directory(".", path)

@app.route("/log2", methods=['GET'])
def log2():  
    path = "train_res.txt"
    return send_from_directory(".", path)

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=10050)
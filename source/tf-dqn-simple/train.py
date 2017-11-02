import numpy as np
import os

import sys
from spark_cluster import SparkCluster
from dqn_agent import DQNAgent
import glob

path = 'historical_data/data'
filenames = glob.glob(path + "/*.csv")

result_train = open("train_res.txt","w")

if __name__ == "__main__":
    print("Main . . .")
    n_epochs = 100
    max_nodes = int(sys.argv[1])
    time_constraint = int(sys.argv[2])*60
    env = SparkCluster()
    agent = DQNAgent(env.enable_actions, env.name)
    agent.load_model("kitwai_models/spark")
    os.system("rm -rf trainZ.txt")
    os.system("touch trainZ.txt")
    for e in range(n_epochs):
        frame = 1
        loss = 0.0
        Q_max = 0.0
        env.reset()
        path = '../data_stream/historical_data/data'
        filenames = glob.glob(path + "/*.csv")
        state_t_1, reward_t, terminal = env.observe(0,0,0,0,0,0,0,0,0)
        count = 0
        for f in filenames:
            log_file = open("trainZ.txt","a")
            count = count + 1
            print(str(e)+"|"+str(count)+"|"+f+"\n")
            log_file.write(str(e)+"|"+str(count)+"|"+f)
            file = open(f,"r")
            next(file)
            for line in file:
                arr = line.split(",")
                execu, memT, memA, cpuU, cpuS, netI, netO = arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7]
                state_t = state_t_1
                action_t = agent.select_action(state_t, agent.exploration)
                env.execute_action(action_t)
                state_t_1, reward_t, terminal = env.observe(memA,memT,cpuU,cpuS,netI,netO,execu,time_constraint,max_nodes)
                agent.store_experience(state_t, action_t, reward_t, state_t_1, terminal)
                agent.experience_replay()
                frame += 1
                loss += agent.current_loss
                Q_max += np.max(agent.Q_values(state_t))
                log_file.write(str(reward_t)+"|"+str(loss/frame)+"|"+str(Q_max/frame)+"\n")
            log_file.close()
            agent.save_model()
        print("EPOCH: {:03d}/{:03d} | LOSS: {:.4f} | Q_MAX: {:.4f}".format( e, n_epochs - 1, loss / frame, Q_max / frame))
        result_train.write(str(e)+","+str(n_epochs - 1)+","+str( loss / frame)+","+str( Q_max / frame)+"\n")
        agent.save_model()
        
from keras.models import *
from keras.layers import *
from keras.optimizers import *
from collections import deque
import random
import pandas as pd

# MAXIMUM_NODES = 10
# model = Sequential()
# model.add(Dense(49, input_dim=7, activation='relu'))
# model.add(Dense(49, activation='relu'))
# model.add(Dense(2*MAXIMUM_NODES, activation='linear'))
# model.compile(loss='mse', optimizers=Adam(lr= learning_Rate))

#Let's code !
class QAgent():
    def __init__( self, state_size, action_size):
        self.weight_backup = "Spark-DQN1.h5"
        self.state_size = state_size
        self.action_size = action_size
        self.memory = deque(maxlen=2000)
        self.learning_rate = 0.001
        self.gamma = 0.95
        self.exploration_rate = 1.0
        self.exploration_min = 0.01
        self.exploration_decay = 0.995
        self.brain = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(49, input_dim=self.state_size, activation='relu'))
        model.add(Dense(49, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(lr=self.learning_rate))
        
        if os.path.isfile(self.weight_backup):
            model.load_weights(self.weight_backup)
            self.exploration_rate = self.exploration_min
        return model
    
    def save_model(self):
        self.brain.save(self.weight_backup)

    def act(self, state):
        if np.random.rand() <= self.exploration_rate:
            return random.randrange(self.action_size)
        act_values = self.brain.predict(state)
        return np.argmax(act_values[0])
    
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def replay(self, sample_batch_size):
        if len(self.memory) < sample_batch_size:
            return
        sample_batch = random.sample(self.memory, sample_batch_size)
        for state, action, reward, next_state, done in sample_batch:
            target = reward
            if not done:
              target = reward + self.gamma * np.amax(self.brain.predict(next_state)[0])
            target_f = self.brain.predict(state)
            target_f[0][action] = target
            self.brain.fit(state, target_f, epochs=1, verbose=0)
        if self.exploration_rate > self.exploration_min:
            self.exploration_rate *= self.exploration_decay

class SparkCluster:
    
    def __init__(self, time, max_nodes):
        self.max_nodes         = max_nodes
        self.sample_batch_size = 32
        self.episodes          = 10000
        self.state_size        = 8
        self.action_size       = (2*(self.max_nodes-1)) + 1
        self.agent             = QAgent(self.state_size, self.action_size)
        self.const_time        = time
    
    def train(self, status, memT, memA, cpuU, cpuS, bytI, bytO, worker):
        try:
            for index_episode in range(self.episodes):
                state = np.ndarray(8)
                print("KKK")
                status = float(status) / self.const_time
                memT = float(memT) / 1000000
                memA = float(memA) / 1000000
                cpuU = float(cpuU) / 100
                cpuS = float(cpuS) / 100
                bytI = float(bytI) / 1000000
                bytO = float(bytO) / 1000000
                worker = float(worker) / self.max_nodes
                state.put(0,status)
                state.put(1,memT)
                state.put(2,memA)
                state.put(3,cpuU)
                state.put(4,cpuS)
                state.put(5,bytI)
                state.put(6,bytO)
                state.put(7,worker)
                state = np.reshape(state, [1, 8])
                done = False
                index = 0
                while not done:
                     action = self.agent.act(state)
                     next_state, reward, done, _ = self.env.step(action)
                     next_state = np.reshape(next_state, [1, self.state_size])
                     self.agent.remember(state, action, reward, next_state, done)
                     state = next_state
                     index += 1
                print("Episode {}# Score: {}".format(index_episode, index + 1))
                self.agent.replay(self.sample_batch_size)
        finally:
            self.agent.save_model()

    def step(self, action):
        # X action --> next_state, reward, done
        reward_out = (2 - (2*(self.current_node+self.scale_node))/(self.max_nodes-1) + self.memoryTransformation + self.memoryAction + self.cpuUser + self.cpuSyst + self.networkIn + self.networkOut + (self.const_time-self.exec_time)/(self.const_time))/10
        reward_in  = (2 - (2*(self.current_node-self.scale_node))/(self.max_nodes-1) + self.memoryTransformation + self.memoryAction + self.cpuUser + self.cpuSyst + self.networkIn + self.networkOut + (self.const_time-self.exec_time)/(self.const_time))/10


import glob
if __name__ == "__main__":
    TIME_CONSTRAINT = 3000 #seconds
    MAXIMUM_NODES = 10 #nodes
    sparkCluster = SparkCluster(TIME_CONSTRAINT, MAXIMUM_NODES)
    path = '../data_stream/historical_data/data'
    filenames = glob.glob(path + "/*.csv")
    for filename in filenames:
        print(filename)
        data = open(filename,"r")
        index = 0
        for line in data:
            if index != 0:
                arr = line.split(",")
                sparkCluster.train(arr[1],arr[2],arr[3],arr[4],arr[5],arr[6],arr[7],arr[8])
            index = index + 1
     
    # sparkCluster.run()
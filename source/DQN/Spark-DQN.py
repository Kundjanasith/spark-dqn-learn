import random, numpy, math, gym
from keras.models import Sequential
from keras.layers import *
from keras.optimizers import *
# https://medium.com/@gtnjuvin/my-journey-into-deep-q-learning-with-keras-and-gym-3e779cc12762

class Brain:

    def __init__(self, stateCnt, actionCnt):
        self.stateCnt = stateCnt
        self.actionCnt = actionCnt
        self.model = self._createModel()
    
    def _createModel(self):
        model = Sequential()
        model.add(Dense(output_dim=64, activation='relu', input_dim=stateCnt))
        model.add(Dense(output_dim=actionCnt, activation='linear'))
        opt = RMSprop(lr=0.00025)
        model.compile(loss='mse', optimizer=opt)
        return model
    
    def train(self, x, y, epoch=1, verbose=0):
        self.model.fit(x, y, batch_size=64, nb_epoch=epoch, verbose=verbose)
    
    def predict(self, s):
        return self.model.predict(s)

    def predictOne(self, s):
        return self.predict(s.reshape(1, self.stateCnt)).flatten()

class Memory:

    samples = []

    def __init__(self, capacity):
        self.capacity = capacity

    def add(self, sample):
        self.samples.append(sample)

        if len(self.samples) > self.capacity:
            self.samples.pop(0)

    def sample(self, n):
        n = min(n, len(self.samples))
        return random.sample(self.samples, n)

MEMORY_CAPACITY = 100000
BATCH_SIZE = 64
GAMMA = 0.99
MAX_EPSILON = 1
MIN_EPSILON = 0.01
LAMBDA = 0.001

class Agent:

    steps = 0
    epsilon = MAX_EPSILON

    def __init__(self, stateCnt, actionCnt):
        self.stateCnt = stateCnt
        self.actionCnt = actionCnt
        self.brain = Brain(stateCnt, actionCnt)
        self.memory = Memory(MEMORY_CAPACITY)
    
    def act(self, s):
        if random.random() < self.epsilon:
            return random.randint(0, self.actionCnt-1)
        else:
            return numpy.argmax(self.brain.predictOne(s))
    
    def observe(self, sample):
        self.memory.add(sample)
        self.steps += 1
        self.epsilon = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON)

    def replay(self):
        batch = self.memory.sample(BATCH_SIZE)
        batchLen = len(batch)
        no_state = numpy.zeros(self.stateCnt)
        states = numpy.array([ o[0] for o in batch ])
        states_ = numpy.array([ (no_state if o[3] is None else o[3]) for o in batch ])
        p = agent.brain.predict(states)
        p_ = agent.brain.predict(states_)
        x = numpy.zeros((batchLen, self.stateCnt))
        y = numpy.zeros((batchLen, self.actionCnt))
        for i in range(batchLen):
            o = batch[i]
            s = o[0]
            a = o[1]
            r = o[2]
            s_ = o[3]
            t = p[i]
            if s_ is None:
                t[a] = r 
            else:
                t[a] = r + GAMMA * numpy.amax(p_[i])
            x[i] = s
            y[i] = t
        self.brain.train(x,y)

class Environment:
    
    def __init__(self, problem, time):
        self.problem = problem
        self.time = time
        self.env = gym.make(problem)

    def run(self, agent):
        s = self.env.reset()
        R = 0
        for ep in range(self.time):
            self.env.render()
            a = agent.act(s)
            print("s",s)
            print("a",a)
            s_, r, done, info = self.env.step(a)
            print("s_",s_)
            print("r",r)
            print("done",done)
            print("info",info)
            if ep == self.time:
                s_ = None
            agent.observe( (s, a, r, s_) )
            agent.replay()
            s = s_ 
            R += r 
            if done:
                break
        print("------------------------------------Total reward:", R)

PROBLEM = 'CartPole-v0'
time = 3000 #5 minutes
env = Environment(PROBLEM,time)
stateCnt = env.env.observation_space.shape[0]
actionCnt = env.env.action_space.n 
agent = Agent(stateCnt, actionCnt)

try:
    # while True:
    # for i in range(time):
    env.run(agent)
finally:
    agent.brain.model.save_weights("Spark-DQN.h5")
    x = agent.brain.model.load_weights("Spark-DQN.h5")
    y = x.predict(1)
    print(y)




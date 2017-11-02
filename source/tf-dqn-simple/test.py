from __future__ import division

import argparse
import os
import sys

import matplotlib.animation as animation
import matplotlib.pyplot as plt

from spark_cluster import SparkCluster
from dqn_agent import DQNAgent


# def init():
#     img.set_array(state_t_1)
#     plt.axis("off")
#     return img,


# def animate(step):
#     global win, lose
#     global state_t_1, reward_t, terminal

#     if terminal:
#         env.reset()

#         # for log
#         if reward_t == 1:
#             win += 1
#         elif reward_t == -1:
#             lose += 1

#         print("WIN: {:03d}/{:03d} ({:.1f}%)".format(win, win + lose, 100 * win / (win + lose)))

#     else:
#         state_t = state_t_1

#         # execute action in environment
#         action_t = agent.select_action(state_t, 0.0)
#         env.execute_action(action_t)

#     # observe environment
#     state_t_1, reward_t, terminal = env.observe()

#     # animate
#     img.set_array(state_t_1)
#     plt.axis("off")
#     return img,


if __name__ == "__main__":
    # args
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-m", "--model_path")
    # parser.add_argument("-s", "--save", dest="save", action="store_true")
    # parser.set_defaults(save=False)
    # args = parser.parse_args()

    # environmet, agent
    max_nodes = int(sys.argv[1])
    time_constraint = int(sys.argv[2])*60
    env = SparkCluster(time_constraint,max_nodes)
    agent = DQNAgent(env.enable_actions, env.name)
    agent.load_model("kitwai_models/spark")

    # variables
    file = open("../data_stream/historical_data/data/current.csv","r")
    next(file)
    rewards = []
    nodes = []
    for line in file:
        arr = line.split(",")
        execu, memT, memA, cpuU, cpuS, netI, netO = arr[1], arr[2], arr[3], arr[4], arr[5], arr[6], arr[7]
        state_t_1, reward_t, terminal = env.observe(memA,memT,cpuU,cpuS,netI,netO,execu)
        print("NODE : "+str(state_t_1[0][7]))
        print("REWARD : "+str(reward_t))
        rewards.append(reward_t)
        nodes.append(state_t_1[0][7])
    print(max(rewards))
    print(nodes[rewards.index(max(rewards))])
    # animate
    # fig = plt.figure(figsize=(env.screen_n_rows / 2, env.screen_n_cols / 2))
    # fig.canvas.set_window_title("{}-{}".format(env.name, agent.name))
    # img = plt.imshow(state_t_1, interpolation="none", cmap="gray")
    # ani = animation.FuncAnimation(fig, animate, init_func=init, interval=(1000 / env.frame_rate), blit=True)

    # if args.save:
    #     ani_path = os.path.join(
    #         os.path.dirname(os.path.abspath(__file__)), "tmp", "demo-{}.gif".format(env.name))
    #     ani.save(ani_path, writer="imagemagick", fps=env.frame_rate)
    # else:
    #     plt.show()

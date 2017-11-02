import os
from flask import Flask, request, jsonify, send_from_directory
from json import dumps, loads
app = Flask(__name__, static_folder=".", template_folder=".")

@app.after_request
def add_headers(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization, data')
    return response

@app.route("/")
def hello():
    return "<h1>Kitwai : Deep Q-Network model service</h1><h2>[kundjanasith@datascienceth.com]</h2>"

# @app.route("/cluster")
# def cluster():
#     return send_from_directory(".", "cluster_node.txt")

# @app.route("/cpu_user/<string:id>", methods=['GET'])
# def cpu_user(id):
#     path = id+"_cpu_user.xml"
#     return send_from_directory(".", path)

# @app.route("/cpu_system/<string:id>", methods=['GET'])
# def cpu_system(id):
#     path = id+"_cpu_system.xml"
#     return send_from_directory(".", path)

# @app.route("/bytes_in/<string:id>", methods=['GET'])
# def bytes_in(id):
#     path = id+"_bytes_in.xml"
#     return send_from_directory(".", path)

@app.route("/train/<int:node>/<int:time>", methods=['GET'])
def bytes_out(node,time):
    n = node #The number of maximum worker nodes
    t = time #The time constraint
    os.system("python ../tf-dqn-simple/model.py "+str(n)+" "+str(t))
    return str(n)+"|"+str(t)

@app.route("/log1", methods=['GET'])
def log1():
    os.system("cp ../tf-dqn-simple/trainZ.txt log1.txt")    
    path = "log1.txt"
    return send_from_directory(".", path)

@app.route("/log2", methods=['GET'])
def log2():
    os.system("cp ../tf-dqn-simple/train_res.txt log2.txt")    
    path = "log2.txt"
    return send_from_directory(".", path)

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=10050)
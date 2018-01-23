from flask import Flask, render_template, request, redirect
import os, json, atexit
from flask_socketio import SocketIO

try:  
    app = Flask(__name__)
    from riven import Riven
    r = Riven()
    s = sched.schedule(time.time, time.sleep)
    app.config['SECRET_KEY'] = 'secret!'
    socketio = SocketIO(app)

    @app.route("/<box>")
    def index(box):
        node_id = r.new_node(box)
        port = r.nodes[node_id]["port"]
        #port = r.new_node(box)
        if port is not 0:
            direct = "http://localhost:{}".format(port)
            return render_template(r.boxes[box]["template"], direct=direct, user_info = r.boxes[box]["user_info"], node_id = node_id)
        else:
            return "Could not load {}".format(box)

    @socketio.on('awake')
    def is_awake(json):
        r.is_awake(json["data"])
        

except Exception as e:
    print e

@atexit.register
def kill_containers():
    os.system('docker stop $(docker ps -a -q)')
    os.system('docker rm $(docker ps -a -q)')


if __name__ == '__main__':
    socketio.run(app)
    


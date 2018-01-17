from flask import Flask, render_template, request, redirect
import os

try:  
    app = Flask(__name__)
    from riven import Riven

    r = Riven()

    @app.route('/')
    def index():
        port = r.new_node()
        return redirect("http://localhost:{}".format(port), code=302)

except:
    # In case of emergency, panic
    os.system('docker stop $(docker ps -a -q)')
    os.system('docker rm $(docker ps -a -q)')
    


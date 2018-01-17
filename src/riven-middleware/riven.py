import docker, time

class Riven:
    def __init__(self):
        self.client = docker.from_env()
        self.nodes=[]

    def new_node(self):
        port = self.find_new_node_port()
        self.nodes.append(port)
        container = self.client.containers.run("boxbox-node:180116", ports={'3000/tcp': port}, detach=True, name="boxbox-node-{}".format(port))
        time.sleep(1) # This is ghetto and I want to replace it with promises. Promise.
        return port


    def find_new_node_port(self):
        if self.nodes:
            return max(self.nodes)+1
        else:
            return 3000
        
    def kill_node(self,node):
        pass

import docker, time, json, datetime, sched, threading
import dateutil.parser

class Riven:
    def __init__(self):
        self.boxes = json.load(open("config/boxes.json"))
        self.config = json.load(open("config/config.json"))
        
        self.client = docker.from_env()
        self.nodes={}
        self.s = sched.scheduler(time.time, time.sleep)

        self.t = threading.Thread(target=self.schedule_node_check, args = ())
        self.t.daemon = True
        self.t.start()


    def schedule_node_check(self):
        self.s.enter(5, 1, self.node_check, ())
        self.s.run()
        
    def node_check(self):
        print "There are {} active containers".format(len(self.nodes))
        for node in self.nodes.copy():
            if "alive_time" in self.nodes[node]:
                alive_time = self.nodes[node]["alive_time"]
            else:
                alive_time=15
            if dateutil.parser.parse(self.nodes[node]["last_seen"]) < datetime.datetime.now()-datetime.timedelta(seconds=alive_time):
                print "{} is old. Killing Container.".format(node)
                self.kill_node(node)
        self.schedule_node_check()
        
    def is_awake(self, box):
        if box in self.nodes:
            timestamp = datetime.datetime.now().isoformat()
            self.nodes[box]["last_seen"] = timestamp
            print self.nodes[box]
        
    def new_node(self, box):
        if box in self.boxes:
            port = self.find_new_node_port()
            node_id = "boxbox{}".format(port)
            timestamp = datetime.datetime.now().isoformat()
            box_info = {"{}".format(node_id):{"port" : port, "last_seen" : timestamp}}
            self.nodes.update(box_info)
            container = self.client.containers.run(self.boxes[box]["container"], ports={self.boxes[box]["internal_port"]: port}, detach=True, name=node_id)
            loaded = self.wait_for_start_log(container, self.boxes[box]["start_log"], self.config["wait_load_time"])
            if loaded is "True":
                return node_id
            else:
                print "Load failed"
                return 0
        else:
            return 0

    def wait_for_start_log(self, container, start_log, wait_time):
        while start_log not in container.logs():
            wait_time = wait_time - 1
            print "Waiting on Container Load... {}".format(wait_time)
            time.sleep(1)
            if wait_time < 1:
                return "False"
        return "True"
    
    def find_new_node_port(self):
        if self.nodes:
            return len(self.nodes)+self.config["start_port"]
        else:
            return self.config["start_port"]
        
    def kill_node(self, node):
        container = self.client.containers.get(node)
        container.stop()
        self.nodes.pop(node, None)        

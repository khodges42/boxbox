# BoxBox

###### Awesome on-demand disposable Docker containers, served up in an HTML5 package.

![lcomicer Riven](doc/img/riven_by_lcomicer.jpg?raw=true "Riven by lcomicer")

BoxBox is a platform for providing a web API to spin up quick-and-dirty docker (and soon Kubernetes) containers, and power them down as needed. BoxBox can run both TTY (using Wetty) or noVNC!

Configuration is as simple as populating the boxes.json file with default settings for your containers. This then becomes an endpoint on the flask server. By default, the container will be powered down after the user closes their browser session.

This project was originally concieved with CTFs in mind, but it can just as easily be utilized for training, testing, and many other purposes.




#### Version 0.2 Notes:

Added Graceful Error Handling. KeyboardInterrupts and crashes will clear the whole cluster of containers.

Added websockets to make sure the user is active.

Fixed a bug that calls New_node a bunch of times, and added a delay that reads the container's startup log to ensure it is started before directing the user towards it.



#### TODO:

Auto-Login option to docker containers

Add Kubernetes Support

Add RDP Support


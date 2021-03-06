# pomelo
<b><i>pomelo</i></b> is a minimal Flask application that monitor tasks. It uses redis list and multiprocessing to execute tasks.


## First. Get the source code and install requirements.

Clone the public repository:

```console
 git clone git@github.com:edrya/pomelo.git
```
Install requirements:

```console
 pip install -r requirements
```


## Run the Task Dispatcher and Task Processor.

To generate tasks for execution run the task dispatcher from the <i>pq</i> directory:

```console
(ve) $ python run_task_dispatcher.py
```

This will create a queue and populate it with tasks and will run until the queue is empty.
Next, lets run the task processor to create workers to execute the tasks:

```console
(ve) $ python run_task_processor.py
```
This will create one worker by default. To have multiple workers all you need to do is run more instances of the task processor or change the <i>num_worker</i> variable.


## Monitor task status with Flask GUI

First, start the task processor in the background:

```console
(ve) $ python run_task_processor.py
```

Next, from the <i>pomelo</i> directory run the app with following command:

```console
(ve) $ flask run
```
This will start the server on IP address 127.0.0.1 with port 5000. 

To view all tasks go to:

```console
http://localhost:5000/
```




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

This will create the queue and populate it with tasks to be processed. It will run until the queue is empty.
Next, lets run the task processor to create workers to execute the tasks:

```console
(ve) $ python run_task_processor.py
```

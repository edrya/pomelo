SHELL = /bin/bash
VE ?= ./ve
PIP ?= $(VE)/bin/pip
REQUIREMENTS ?= requirements.txt


create:
	@echo "Installing python virtual env at $(VE)"
	rm -rf $(VE)
	python3 -m venv $(VE)
	$(PIP) install --requirement $(REQUIREMENTS)


task-worker:
	$(VE)/bin/python3 pqueue/run_task_processor.py


runserver:
	$(VE)/bin/flask run
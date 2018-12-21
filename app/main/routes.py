import time
from threading import Thread
from multiprocessing import Process

from flask import render_template, flash, redirect, url_for, request, g, \
    jsonify, current_app


from app.main import bp


@bp.route('/',  methods=['GET', 'POST'])
def index():
    current_app.redis_connection.flush_db()
    tasks = current_app.task_generator.generate_tasks()

    return render_template('index.html', tasks=tasks)


@bp.route('/statuses', methods=['GET', 'POST'])
def get_statuses():

    if request.method == 'POST':

        ids = request.form.getlist('ids[]')
        statuses = request.form.getlist('status[]')

        tasks = [{'id': int(task), 'status': statuses[idx]} for idx, task in enumerate(ids)]

        for task in tasks:
            value = get_status(task['id'])
            if value:
                task['status'] = 'completed'
                task['value'] = value

        return jsonify(tasks), 200

    return render_template('dashboard.html')


@bp.route('/dispatch', methods=['POST'])
def run_task_dispatcher():

    tasks = current_app.task_generator.generate_tasks()

    Thread(target=current_app.task_dispatcher.run, args=(tasks,)).start()

    return jsonify({'success': True}), 202


def get_status(key):
    value = current_app.redis_connection.get_value(key)
    return value
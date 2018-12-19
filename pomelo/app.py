import os
import threading
import time

from flask import Flask, render_template, jsonify


from config import config

app = Flask(__name__)
app.config.from_object(config[os.environ.get('FLACK_CONFIG', 'development')])


@app.route('/')
def index():
    """Serve client-side application."""
    return render_template('index.html')

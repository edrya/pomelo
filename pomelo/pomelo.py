import os
import threading
import time
import click

from flask import Blueprint, render_template, jsonify, current_app


from config import config

main = Blueprint('main', __name__)


@main.route('/',  methods=['GET', 'POST'])
def index():
    """Serve client-side application."""
    pass
    return render_template('index.html')

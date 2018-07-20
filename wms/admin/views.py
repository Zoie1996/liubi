from flask import render_template, request

from wms.admin.models import Worker
from . import admin


@admin.route('/index.html')
def index():
    return render_template('index.html')


@admin.route('/table_basic.html', methods=['GET'])
def worker():
    if request.method == 'GET':
        worker_list = Worker.query.all()
        return render_template('table_basic.html', worker_list=worker_list)

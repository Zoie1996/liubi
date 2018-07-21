from flask import render_template, request, redirect, url_for

from wms.admin.models import Worker, Profession
from . import admin


@admin.route('/index.html')
def index():
    """
    显示首页
    :return:
    """
    return render_template('index.html')


@admin.route('/worker.html', methods=['GET'])
def worker():
    """
    显示员工页面
    :return:
    """
    if request.method == 'GET':
        # 所用工人列表
        worker_list = Worker.query.all()
        # 获取工种信息
        pros = Profession.query.all()
        return render_template('worker.html', worker_list=worker_list, pros=pros)


@admin.route('/add_worker', methods=['POST'])
def add_worker():
    """
    添加员工
    :return:
    """
    if request.method == 'POST':
        worker = Worker()
        data = request.form.to_dict()
        worker.name = data['name']
        worker.sex = data['sex']
        worker.phone = data['phone']
        worker.id_card = data['id_card']
        worker.card_img = data['card_img']
        worker.bank_card_no = data['bank_card_no']
        worker.bank_card_name = data['bank_card_name']
        worker.salary = data['salary']
        worker.pro_id = data['pro_id']
        worker.add_update()
        return redirect(url_for('admin.worker'))


@admin.route('/del_worker/<int:worker_id>', methods=['GET'])
def del_worker(worker_id):
    """
    删除工人
    :param worker_id: 工人id
    :return:
    """
    worker = Worker.query.get(worker_id)
    worker.delete()
    return redirect(url_for('admin.worker'))


@admin.route('/worker_info.html', methods=['GET'])
def worker_info():
    if request.method == 'GET':
        pass

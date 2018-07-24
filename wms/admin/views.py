from flask import render_template, request, redirect, url_for, jsonify

from wms import status_code
from wms.admin.models import Worker, Profession, Project
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
        worker_list = list(Worker.query.filter_by(status=0))
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


@admin.route('/del_worker/<int:worker_id>', methods=['PATCH'])
def del_worker(worker_id):
    """
    删除工人
    :param worker_id: 工人id
    :return:
    """
    worker = Worker.query.get(worker_id)
    worker.status = 1
    worker.add_update()
    return jsonify(status_code.SUCCESS)


@admin.route('/worker_info/<int:worker_id>', methods=['GET'])
def worker_info(worker_id):
    """
    显示员工信息
    :param worker_id:
    :return:
    """
    worker = Worker.query.get(worker_id)
    pro_name = Profession.query.get(worker.pro_id).name
    pros = Profession.query.all()
    return jsonify({'code': status_code.OK, 'worker': worker.to_dict(),
                    'pros': [pro.to_dict() for pro in pros]})


@admin.route('/edit_worker/', methods=['POST'])
def edit_worker():
    """
    修改员工信息
    :return:
    """
    data = request.form.to_dict()
    worker_id = data['id']
    worker = Worker.query.get(worker_id)
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
    return jsonify(code=status_code.OK)


@admin.route('/project.html', methods=['GET'])
def project():
    if request.method == 'GET':
        projects = Project.query.all()
        return render_template('project.html', projects=projects)

@admin.route('/add_project', methods=['POST'])
def add_project():
    if request.method == 'POST':
        data = request.form.to_dict()
        project = Project()
        project.name = data['name']
        project.address = data['address']
        project.start_time = data['start_time']
        project.add_update()
        return redirect(url_for('admin.project'))

from time import sleep

from flask import render_template, request, redirect, url_for, jsonify

from wms import status_code
from wms.admin.models import Worker, Profession, Project, Advances
from . import admin


@admin.route('/index.html')
def index():
    """
    显示首页
    :return:
    """
    return render_template('index.html')


""" 工人功能开始 """


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
    :return: 重定向到员工首页
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
        sleep(2)
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


""" 工人功能结束 """

""" 工程功能开始 """


@admin.route('/project.html')
def project():
    """
    显示工程页面
    :return:
    """
    return render_template('project.html')


@admin.route('/project/', methods=['GET'])
def projects():
    """
    渲染工程页面信息
    :return:
    """
    if request.method == 'GET':
        projects = Project.query.filter(Project.status == 0)
        project_list = [project.to_dict() for project in projects]
        return jsonify({'code': status_code.OK, 'projects': project_list})


@admin.route('/add_project', methods=['POST'])
def add_project():
    """
    添加工程
    :return:
    """
    if request.method == 'POST':
        data = request.form.to_dict()
        project = Project()
        project.name = data['name']
        project.address = data['address']
        project.start_time = data['start_time']
        project.add_update()
        return redirect(url_for('admin.project'))


@admin.route('/project_info/<int:project_id>', methods=['GET'])
def project_info(project_id):
    """
    获取工程信息
    :param project_id:
    :return:
    """
    if request.method == 'GET':
        project = Project.query.get(project_id)
        return jsonify({'code': status_code.OK, 'project': project.to_dict()})


@admin.route('/edit_project/', methods=['POST'])
def edit_project():
    """
    编辑工程信息
    :return:
    """
    if request.method == 'POST':
        data = request.form.to_dict()
        id = data['id']
        project = Project.query.get(id)
        project.name = data['name']
        project.address = data['address']
        project.start_time = data['start_time']
        project.add_update()
        return jsonify(code=status_code.OK)


@admin.route('/del_project/<int:project_id>', methods=['PATCH'])
def del_project(project_id):
    """
    删除工程信息
    """
    project = Project.query.get(project_id)
    project.status = 1
    project.add_update()
    return jsonify(code=status_code.OK)


""" 工程功能结束 """

""" 工天功能开始 """
@admin.route('/roster.html', methods=['GET'])
def roster():
    return render_template('roster.html')
""" 工天功能结束 """


""" 借支管理 """
@admin.route('/advances.html', methods=['GET'])
def advances():
    """
    借支界面
    :return:
    """
    if request.method == 'GET':
        # 获取工种信息, 用于添加员工渲染页面
        pros = Profession.query.all()
        return render_template('advances.html',pros=pros)


@admin.route('/show_advances', methods=['GET'])
def show_advances():
    if request.method == 'GET':
        advances = Advances.query.all()
        workers = []
        for advance in advances:
            worker = advance.worker
            if worker not in workers:
                workers.append(worker)
        # 异步请求
        worker_list = [worker.to_dict() for worker in workers]
        advance_list = [advance.to_dict() for advance in advances]
        return jsonify({'code': status_code.OK, 'workers': worker_list, 'advances': advance_list})


@admin.route('/add_advances', methods=['GET', 'POST'])
def add_advances():
    if request.method == 'GET':
        workers = Worker.query.filter_by(status=0)
        worker_list = [worker.to_dict() for worker in workers]
        return jsonify({'code': status_code.OK, 'workers': worker_list})
    if request.method == 'POST':
        data = request.form.to_dict()
        advances = Advances()
        advances.money = data['money']
        advances.time = data['time']
        advances.signature = data['signature']
        advances.mode = data['mode']
        advances.remark = data['remark']
        advances.worker_id = data['worker_id']
        advances.add_update()
        return jsonify(code=status_code.OK)



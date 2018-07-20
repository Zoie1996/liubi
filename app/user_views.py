from flask import Blueprint, jsonify, render_template
from app.models import db, Worker
from utils import status_code

user_blueprint = Blueprint('user', __name__)


# 创建数据表
# @user_blueprint.route('/create_db')
# def create_db():
#     # 创建表
#     db.create_all()
#     return '创建表成功'

@user_blueprint.route('/worker_list')
def worker_list():
    workers = Worker.query.all()
    worker_list  = [worker.to_dict() for worker in workers]
    return jsonify(code=status_code.OK,count=len(worker_list), data=worker_list)

@user_blueprint.route('/worker')
def worker():
    return render_template('worker.html')
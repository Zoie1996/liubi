from datetime import datetime

from flask import jsonify
from flask_sqlalchemy import SQLAlchemy

from utils import status_code

db = SQLAlchemy()


class BaseModel(object):
    """定义基础的模型"""
    create_time = db.Column(db.DATETIME, default=datetime.now())
    update_time = db.Column(db.DATETIME, default=datetime.now(), onupdate=datetime.now())

    def add_update(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
        return jsonify(status_code.DATABASE_ERROR)

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Profession(db.Model, BaseModel):
    """工种"""
    __tablename__ = 'profession'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 工人id
    name = db.Column(db.String(20))
    worker = db.relationship('Worker', backref='profession', lazy=True)

    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name
        }


class Worker(db.Model, BaseModel):
    # 工人
    __tablename__ = 'worker'
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 工人id
    name = db.Column(db.String(10), unique=True)  # 工人名字
    age = db.Column(db.Integer)  # 年龄
    sex = db.Column(db.Integer, default=1) # 性别 默认 1 男
    phone = db.Column(db.String(11))  # 电话号码
    id_card = db.Column(db.String(18), unique=True)  # 身份证号
    card_img = db.Column(db.String(256))  # 身份证照片
    salary = db.Column(db.Integer)  # 薪资
    bank_card_no = db.Column(db.String(20)) # 银行卡号
    bank_card_name = db.Column(db.String(10)) # 持卡人姓名
    pro_id = db.Column(db.Integer, db.ForeignKey('profession.id'))  # 工种

    roster = db.relationship('Roster', backref='worker', lazy=True)  # 工天
    advances = db.relationship('Advances', backref='worker', lazy=True)  # 借支
    facility = db.relationship('Facility', backref='worker', lazy=True) # 设备


    def to_dict(self):
        return {
            'id':self.id,
            'name':self.name,
            'sex': '男' if self.sex else '女',
            'age':self.age,
            'phone' :self.phone,
            'id_card':self.id_card,
            'card_img':self.card_img,
            'salary':self.salary,
            'bank_card_no':self.bank_card_no,
            'bank_card_name':self.bank_card_name,
            'pro_id': self.pro_id
        }


class Project(db.Model, BaseModel):
    """项目模型"""
    __tablename__ = 'project'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 工程id
    name = db.Column(db.String(20))  # 工程名
    address = db.Column(db.String(50))  # 工地所在地



class Roster(db.Model, BaseModel):
    """工天模型"""
    __tablename__ = 'roster'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 工程id
    work_hour = db.Column(db.Float, default=10)  # 工时
    work_overtime = db.Column(db.Float)  # 加班工时
    time = db.Column(db.DATETIME)  # 登记时间
    work_id = db.Column(db.Integer, db.ForeignKey('worker.id'))



class Advances(db.Model, BaseModel):
    """借支模型"""
    __tablename__ = 'advances'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 借支id
    money = db.Column(db.Integer)  # 金额
    signature = db.Column(db.String(256))  # 经办人签字
    time = db.Column(db.DATETIME)  # 借款时间
    mode = db.Column(db.String(20))  # 借款方式 现金/微信转账等
    remark = db.Column(db.Text)  # 备注
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'))



class Income(db.Model, BaseModel):
    """入账模型"""
    __tablename__ = 'income'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 借支id
    money = db.Column(db.Integer)  # 金额
    signature = db.Column(db.String(256))  # 经办人签字
    time = db.Column(db.DATETIME)  # 收款时间
    remark = db.Column(db.Text)  # 备注



class Facility(db.Model, BaseModel):
    """设备模型"""
    __tablename__ = 'facility'

    id = db.Column(db.Integer, autoincrement=True, primary_key=True)  # 借支id
    name = db.Column(db.String(20))  # 设备名称
    borrow_time = db.Column(db.DATETIME)  # 借出时间
    return_time = db.Column(db.DATETIME)  # 归还时间
    worker_id = db.Column(db.Integer, db.ForeignKey('worker.id'))

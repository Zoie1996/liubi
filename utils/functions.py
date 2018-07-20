from flask import Flask

from app.user_views import user_blueprint
from app.work_views import work_blueprint
from utils.setting import STATIC_DIR, TEMPLATES_DIR

from app.models import db

def create_app():
    app = Flask(__name__,
                static_folder=STATIC_DIR,
                template_folder=TEMPLATES_DIR)

    app.register_blueprint(blueprint=user_blueprint, url_prefix='/user')
    app.register_blueprint(blueprint=work_blueprint, url_prefix='/')
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost:3306/wms"
    app.config['SQLALCHEMY_TRAKE_MODIFICATIONS'] = False
    db.init_app(app=app)
    return app

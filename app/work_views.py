from flask import Blueprint, render_template

work_blueprint = Blueprint('work', __name__)

@work_blueprint.route('/')
def index():
    return render_template('index.html')

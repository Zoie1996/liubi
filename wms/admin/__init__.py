from flask import Blueprint

admin = Blueprint(
    'admin',
    __name__,
    template_folder='templates',
    static_folder='static'
)
print(admin.static_folder)
from . import views

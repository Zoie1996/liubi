# 项目启动文件
from wms import create_app
from flask_script import Manager
# from flask_migrate import Migrate, MigrateCommand
from config import Config

app = create_app('develop')

# Migrate(app, db)
# manager = Manager(app)
# manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    # print(app.url_map)
    app.run(host=Config.HOST, port=Config.PORT)

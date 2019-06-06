from flask import current_app
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from info import create_app,db

app = create_app('develop')
# 设置flask_script
manager = Manager(app)
# 设置数据库迁移
manager.add_command('db',MigrateCommand)
Manager(app,db)

@app.route('/')
def index():
    # redis_store.set(('name_test'),'sdgewgsfgwe')
    # session['qwe'] = 'sfsdfwrwfsdgwfwgf'
    current_app.logger.debug('debug')
    current_app.logger.error('error')
    return 'index'


if __name__ == "__main__":
    manager.run()
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from info import app,db

# 设置flask_script
manager = Manager(app)
# 设置数据库迁移
manager.add_command('db',MigrateCommand)
Manager(app,db)

@app.route('/')
def index():
    # redis_store.set(('name_test'),'sdgewgsfgwe')
    # session['qwe'] = 'sfsdfwrwfsdgwfwgf'
    return 'index'


if __name__ == "__main__":
    manager.run()
from info import create_app,db,models

# 1、导入相关的类文件
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand

app = create_app("develop")
# 2、创建Manager对象manager来管理app
manager = Manager(app) # type:Manager
# 3、使用migrate，关联db,app
Migrate(app,db)
# 4、给manager添加一条操作命令
manager.add_command("db",MigrateCommand)

if __name__ == '__main__':
    manager.run()
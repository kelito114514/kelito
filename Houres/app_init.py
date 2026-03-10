import os.path

from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from config import configs
from flask_ckeditor import CKEditor
from flask_bootstrap import Bootstrap4
from sqlalchemy import inspect
ckeditor=CKEditor()
boostrap = Bootstrap4()
db = SQLAlchemy()
def create_app(config_name):
    app = Flask(__name__)
    config = configs[config_name]
    app.config.from_object(config)
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['UPLOADED_PATH'] = os.path.join(basedir,'uploadfiles')
    os.makedirs(app.config['UPLOADED_PATH'],exist_ok=True)
    db.init_app(app)
    ckeditor.init_app(app)
    boostrap.init_app(app)
    from user_manager import user_blue
    app.register_blueprint(user_blue)
    from hourse_manager import hourse_blue
    app.register_blueprint(hourse_blue)
    with app.app_context():
        create_database()
    return app

def create_database():
    from hourse_info import Hourse, User, Recommend
    models = [Hourse,User,Recommend]
    ipt = inspect(db.engine)
    for m in models:
        table_name = m.__tablename__
        if not ipt.has_table(table_name):
            try:
                m.__table__.create(db.engine)
                print(f"表'{table_name}'已成功创建")
            except Exception as e:
                print(f"创建表'{table_name}'时出错:{e}")
        else:
            print(f"表'{table_name}'已经存在")
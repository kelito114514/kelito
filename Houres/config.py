import os

class Config:
    SECRET_KEY = '123456'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_PKG_TYPE = 'full'
    CKEDITOR_CSRF = False
    CKEDITOR_FILE_UPLOADER = '/upload_file'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'hourse_data_devel.sqlite'
    )

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'hourse_data_product.sqlite'
    )

class TestConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
        os.path.abspath(os.path.dirname(__file__)), 'hourse_data_test.sqlite'
    )

configs = {'development':DevelopmentConfig, 'testing':TestConfig, 'production':ProductionConfig}
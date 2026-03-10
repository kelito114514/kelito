from flask import Blueprint
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,Length,EqualTo,Regexp

class RegistrationForm(FlaskForm):
    class Meta:
        csrf = True

    name = StringField('用户名', validators=[  # input type='text'
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=20, message='用户名长度在3-20个字符之间')
    ])
    email = StringField('邮箱', validators=[
        DataRequired(message='邮箱不能为空'),
        Regexp(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', message='请输入有效的邮箱地址')
    ])
    phone = StringField('手机号', validators=[
        DataRequired(message='手机号不能为空'),
        Length(min=11, max=11, message='手机号必须是11位数字')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'),
        Length(min=6, message='密码至少6个字符'),
        EqualTo('confirm_password', message='两次密码不一致')
    ])
    confirm_password = PasswordField('确认密码', validators=[
        DataRequired(message='请确认密码')
    ])
    submit = SubmitField('注册')

class Registrationlogin(FlaskForm):
    class Meta:
        csrf = True

    name = StringField('用户名', validators=[  # input type='text'
        DataRequired(message='用户名不能为空'),
        Length(min=3, max=20, message='用户名长度在3-20个字符之间')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='密码不能为空'),
        Length(min=6, message='密码至少6个字符')
    ])

    submit = SubmitField('登录')
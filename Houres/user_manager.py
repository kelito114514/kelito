from flask import Blueprint, render_template, request, redirect, url_for, flash, session,Flask
from form import RegistrationForm,Registrationlogin
from hourse_info import User
from app_init import db
user_blue = Blueprint('users',__name__)
# app = Flask(__name__)
# app.config['SECRET_KEY'] = '123456'

@user_blue.route('/register',methods=['POST','GET'])
def register():
    form_register = RegistrationForm()
    if form_register.validate_on_submit():
        name = form_register.name.data
        exist_name = User.query.filter_by(name=name).first()
        if exist_name:
            flash('用户名已存在','error')
            return render_template('register.html',form=form_register)
        email = form_register.email.data
        exist_email = User.query.filter_by(email=email).first()
        if exist_email:
            flash('邮箱已注册','error')
            return render_template('register.html',form=form_register)
        phone = form_register.phone.data
        exist_phone = User.query.filter_by(phone=phone).first()
        if exist_phone:
            flash('手机号码已经被注册', 'error')
            return render_template('register.html', form=form_register)
        pwd = form_register.password.data
        user1 = User(name=name, email=email, password=pwd,phone=phone)
        db.session.add(user1)
        db.session.commit()
        return redirect(url_for('users.index'))
    return render_template('register.html',form=form_register)


@user_blue.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@user_blue.route('/login',methods=['POST','GET'])
def login():
    form = Registrationlogin()
    if form.validate_on_submit():
        user_name = form.name.data
        pwd = form.password.data
        user = User.query.filter_by(name=user_name,password=pwd).first()
        if user:
            session['user_id'] = user.id
            session['username'] = user_name
            return redirect(url_for('hourse.add_hourse'))
        else:
            flash("用户名或密码错误",'error')
            return render_template('login.html',form=form)
    return render_template('login.html',form=form)


@user_blue.route('/logout')
def logout():
    session['user_id'] = None
    session['username'] = None
    return redirect(url_for('users.login'))
from app_init import db


class Hourse(db.Model):
    __tablename__ = 'hourse_info'
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    title = db.Column(db.String(100))  # 标题
    rooms = db.Column(db.String(100))  # 户型
    area = db.Column(db.String(100))  # 面积
    price = db.Column(db.Float)#
    address = db.Column(db.String(100))  # 地址
    region = db.Column(db.String(100))  # 所在区
    publish_time = db.Column(db.DateTime)
    page_views = db.Column(db.Integer)#浏览量
    desc = db.Column(db.TEXT)#描述
    landlord = db.Column(db.String(100))#房东姓名
    phone_num = db.Column(db.String(100))#电话号码
    district = db.Column(db.String(100)) #区域/行政区
    house_type = db.Column(db.String(50)) #房屋类型:出租
    user_id = db.Column(db.Integer,db.ForeignKey('user_info.id'))
    bedrooms = db.Column(db.Integer)#卧室数量
    living_rooms = db.Column(db.Integer)#客厅数量
    bathrooms = db.Column(db.Integer)#卫生间数量
    floor = db.Column(db.String(20))
    property_type = db.Column(db.String(20))
    decoration = db.Column(db.String(20))
    main_image = db.Column(db.String(20))

class User(db.Model):
    __tablename__ = 'user_info'
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    name = db.Column(db.String(100),unique = True)  # 用户名
    password = db.Column(db.String(100))  # 密码
    email = db.Column(db.String(100))  # 邮箱
    phone = db.Column(db.String(100))  # 电话
    collect_id = db.Column(db.String(200))  # 收藏房号
    hourses = db.relationship('Hourse',backref='User',lazy=True)

class Recommend(db.Model):
    __tablename__ = 'hourse_recomend'
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    user_id = db.Column(db.Integer)  # 用户id
    hourse_id = db.Column(db.Integer)  # 房子id
    score = db.Column(db.Integer)  # 房子被用户浏览次数
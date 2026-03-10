# app/forms/house_forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SelectField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Optional
from flask_wtf.file import FileField, FileAllowed, MultipleFileField


class HouseForm(FlaskForm):
    # 基本信息
    title = StringField('房源标题', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('房源描述', validators=[DataRequired(), Length(max=2000)])

    # 交易信息
    house_type = SelectField('交易类型', choices=[
        ('出售', '出售'),
        ('出租', '出租')
    ], validators=[DataRequired()])
    price = FloatField('价格', validators=[DataRequired(), NumberRange(min=0)])

    # 房屋信息
    area = FloatField('面积(㎡)', validators=[DataRequired(), NumberRange(min=1)])
    bedrooms = IntegerField('卧室数量', validators=[DataRequired(), NumberRange(min=0)])
    living_rooms = IntegerField('客厅数量', validators=[DataRequired(), NumberRange(min=0)])
    bathrooms = IntegerField('卫生间数量', validators=[DataRequired(), NumberRange(min=0)])

    # 位置信息
    district = SelectField('所在区域', choices=[
        ('', '请选择区域'),
        ('东城区', '东城区'),
        ('西城区', '西城区'),
        ('朝阳区', '朝阳区'),
        ('海淀区', '海淀区'),
        ('丰台区', '丰台区'),
        ('石景山区', '石景山区'),
        ('通州区', '通州区'),
        ('昌平区', '昌平区'),
        ('大兴区', '大兴区'),
        ('顺义区', '顺义区'),
        ('房山区', '房山区'),
        ('门头沟区', '门头沟区'),
        ('怀柔区', '怀柔区'),
        ('平谷区', '平谷区'),
        ('密云区', '密云区'),
        ('延庆区', '延庆区')
    ], validators=[DataRequired()])
    address = StringField('详细地址', validators=[DataRequired(), Length(max=300)])

    # 房屋特征
    orientation = SelectField('朝向', choices=[
        ('', '请选择朝向'),
        ('南', '南'),
        ('北', '北'),
        ('东', '东'),
        ('西', '西'),
        ('南北', '南北'),
        ('东西', '东西'),
        ('东南', '东南'),
        ('西南', '西南'),
        ('东北', '东北'),
        ('西北', '西北')
    ], validators=[DataRequired()])
    floor = StringField('所在楼层', validators=[DataRequired(), Length(max=20)])
    #total_floors = IntegerField('总楼层数', validators=[DataRequired(), NumberRange(min=1)])
    decoration = SelectField('装修情况', choices=[
        ('', '请选择装修'),
        ('毛坯', '毛坯'),
        ('简装', '简装'),
        ('精装', '精装'),
        ('豪华装修', '豪华装修')
    ], validators=[DataRequired()])
    #built_year = IntegerField('建造年份', validators=[DataRequired(), NumberRange(min=1900, max=2030)])
    property_type = SelectField('物业类型', choices=[
        ('', '请选择物业类型'),
        ('住宅', '住宅'),
        ('公寓', '公寓'),
        ('别墅', '别墅'),
        ('商住两用', '商住两用'),
        ('其他', '其他')
    ], validators=[DataRequired()])

    # 联系信息
    contact_name = StringField('联系人', validators=[DataRequired(), Length(max=100)])
    contact_phone = StringField('联系电话', validators=[DataRequired(), Length(max=20)])

    # 图片上传
    main_image = MultipleFileField('主图', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '只允许上传图片文件!')
    ])
    additional_images = MultipleFileField('附加图片', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], '只允许上传图片文件!')
    ])
    submit = SubmitField('登录')
import os.path
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app,send_from_directory
from form import RegistrationForm,Registrationlogin
from hourse_info import User,Hourse
from app_init import db
from sqlalchemy import or_
from house_forms import HouseForm
hourse_blue = Blueprint('hourse',__name__)
def allowed_file(filename):
    ALLOWED_EXTENSIONS = {'jpg','jpeg','png','gif'}
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
def save_images(files):
    image_list = []
    for image in files:
        image_name = image.filename
        if allowed_file(image_name):#判断图片是否是'jpg','jpeg','png','gif'
            timetamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
            image_name = timetamp + image_name#更改图片的名字，加了时间
            image.save(os.path.join(current_app.config['UPLOADED_PATH'],image_name))
            image_list.append(image_name)
    return image_list

@hourse_blue.route('/add_hourse',methods=['POST','GET'])
def add_hourse():
    hourse_form = HouseForm()
    user_id = session['user_id']
    if hourse_form.validate_on_submit():
        files = request.files.getlist('main_image')
        image_list = save_images(files)
        houre = Hourse(title=hourse_form.title.data,
                       area=hourse_form.area.data,
                       price=hourse_form.price.data,
                       address=hourse_form.address.data,
                       publish_time=datetime.now(),
                       desc=hourse_form.description.data,
                       landlord=hourse_form.contact_name.data,
                       phone_num=hourse_form.contact_phone.data,
                       district=hourse_form.district.data,
                       house_type=hourse_form.house_type.data,
                       user_id=user_id,
                       bedrooms=hourse_form.bedrooms.data,
                       living_rooms=hourse_form.living_rooms.data,
                       bathrooms=hourse_form.bathrooms.data,
                       floor=hourse_form.floor.data,
                       property_type=hourse_form.property_type.data,
                       decoration=hourse_form.decoration.data,
                       main_image=','.join(image_list)
                       )
        db.session.add(houre)
        db.session.commit()
        return redirect(url_for('hourse.hourse_list',page=1))
    user = User.query.filter_by(id=user_id).first()
    if user:
        hourse_form.contact_name.data = user.name
        hourse_form.contact_phone.data = user.phone
    return render_template('add_hourse.html',form=hourse_form)

@hourse_blue.route('/upload_files/<filename>')
def upload_files(filename):
    path = current_app.config['UPLOADED_PATH']
    return send_from_directory(path,filename)

@hourse_blue.route('/hourse_list/<int:page>')
def hourse_list(page):
    per_page=3
    districts = ['东城区', '西城区', '朝阳区', '海淀区', '丰台区', '石景山区', '通州区', '昌平区',
                 '大兴区', '顺义区', '房山区', '门头沟区', '怀柔区', '平谷区', '密云区', '延庆区']
    district_filter = request.args.get('district')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    query = Hourse.query
    if district_filter:
        query = query.filter(Hourse.district == district_filter)
    if min_price:
        query = query.filter(Hourse.price >= float(min_price))
    if max_price:
        query = query.filter(Hourse.price <= float(max_price))
    pagination = query.order_by(Hourse.publish_time.desc()).paginate(page=int(page),per_page=per_page,error_out=False)
    hourses = pagination.items
    filter_values = {'district':district_filter,'min_price':min_price,'max_price':max_price}
    for hourse in hourses:
        if hourse:
            hourse_imgurls=[]
            for imgurl in hourse.main_image.split(','):
                hourse_imgurls.append(url_for('hourse.upload_files',filename=imgurl))
            if len(hourse_imgurls) <=0:
                hourse_imgurls.append(url_for('hourse.upload_files',filename='default.jpg'))
            hourse.image_urls = hourse_imgurls
    return render_template('hourse_list.html',hourses=hourses,pagination=pagination,districts=districts,filter_values=filter_values)


@hourse_blue.route('/search')
def search():
    districts = ['东城区', '西城区', '朝阳区', '海淀区', '丰台区', '石景山区', '通州区', '昌平区',
                 '大兴区', '顺义区', '房山区', '门头沟区', '怀柔区', '平谷区', '密云区', '延庆区']
    search_value = request.args.get('q').strip()
    page = request.args.get('page',1,type=int)
    per_page = 3
    query = Hourse.query.filter(or_(Hourse.title.ilike(f'%{search_value}'),Hourse.district.ilike(f'%{search_value}'),Hourse.desc.ilike(f'%{search_value}')))
    district_filter = request.args.get('district')
    min_price = request.args.get('min_price')
    max_price = request.args.get('max_price')
    if district_filter:
        query = query.filter(Hourse.district == district_filter)
    if min_price:
        query = query.filter(Hourse.price >= float(min_price))
    if max_price:
        query = query.filter(Hourse.price <= float(max_price))
    pagination = query.order_by(Hourse.publish_time.desc()).paginate(page=int(page),per_page=per_page,error_out=False)
    hourses = pagination.items
    filter_values = {'district': district_filter,'min_price':min_price,'max_price':max_price}
    for hourse in hourses:
        if hourse:
            hourse_imgurls = []
            for imgurl in hourse.main_image.split(','):
                hourse_imgurls.append(url_for('hourse.upload_files', filename=imgurl))
            if len(hourse_imgurls) <= 0:
                hourse_imgurls.append(url_for('hourse.upload_files', filename='default.jpg'))
            hourse.image_urls = hourse_imgurls
    return render_template('hourse_list.html', hourses=hourses, pagination=pagination,districts=districts,filter_values=filter_values,search_value=search_value)
@hourse_blue.route('/house_detail/<house_id>')
def hourse_detail(house_id):
    hourse = Hourse.query.filter_by(id=house_id).first()
    if hourse:
        hourse.page_views = hourse.page_views + 1 if hourse.page_views else 1
        db.session.commit()
        hourse_imgurls = []
        for imgurl in hourse.main_image.split(','):
            hourse_imgurls.append(url_for('hourse.upload_files', filename=imgurl))
        if len(hourse_imgurls) <= 0:
            hourse_imgurls.append(url_for('hourse.upload_files', filename='default.jpg'))
        hourse.image_urls = hourse_imgurls

    landlord = User.query.filter_by(id = hourse.user_id).first()

    # 获取推荐房源（同区域的房源）
    recommended_houses = Hourse.query.filter(
        Hourse.district == hourse.district,
        Hourse.id != hourse.id
    ).order_by(Hourse.publish_time.desc()).limit(4).all()

    # 处理推荐房源的图片
    for rec_house in recommended_houses:
        rec_house.image_urls = []
        if rec_house.main_image:
            image_filenames = rec_house.main_image.split(',')
            for image_file in image_filenames:
                img_url = url_for('hourse.uploaded_file', filename=f'{image_file.strip()}')
                rec_house.image_urls.append(img_url)

        if not rec_house.image_urls:
            rec_house.image_urls.append(url_for('hourse.upload_files',filename='default.jpg'))

    return render_template('house_detail.html',house=hourse,landlord=landlord,recommended_houses=recommended_houses)
import base64
import os
import re
import random
import threading

import cv2
import numpy as np

from flask import *

from auth.Auth import Auth
from dao.FollowDAO import FollowDAO
from dao.FollowerDAO import FollowerDAO
from dao.FollowingDAO import FollowingDAO
from dao.ImageDAO import WorkDAO
from dao.InformationDAO import InformationDAO
from dao.UserDAO import UserDAO
from dao.addressDAO import AddressDAO
from pojo.Image import Work
from pojo.Information import Information
from pojo.User import User
from operation.tricks import *
from operation.ai import *


from Result import *
from pojo.address import Address

app = Flask(__name__)


# 登录账户
# 已修改
@app.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    if 'phone' not in data or 'password' not in data:
        return "信息缺失"

    phone = data['phone']
    password = data['password']

    # 判断电话号码是否为空
    if phone is None:
        return "The phone number is empty!"

    # 判断密码是否为空
    if password is None:
        return "The password is empty!"

    user = User()
    user.set_phone(phone)
    user.set_password(password)

    try:
        user = UserDAO().retrieve(user)
    except:
        return "Server Failure!"

    # 用户不存在
    if user is None:
        result = return_status(-1)
        return jsonify(result)

    # 授权
    result = Auth.authorize(user)
    return jsonify(result)


# 注册账户
# 已修改
@app.route('/user/register', methods=['POST'])
def register():
    data = request.get_json()
    if 'phone' not in data or 'password' not in data:
        return "信息缺失"

    phone = data['phone']
    password = data['password']

    # 判断电话号码是否为空
    if phone is None:
        return "The phone number is empty!"

    # 判断密码是否为空
    if password is None:
        return "The password is empty!"

    # 检测手机是否已经使用
    phone_is_used = verify_phone(phone)
    if phone_is_used:
        result = return_status(-1)  # 手机号码被使用
        return jsonify(result)

    # 检测手机格式是否正确
    phone_format_false = verify_phone_format(phone)
    if phone_format_false:
        result = return_status(-2)  # 手机格式不正确
        return jsonify(result)

    user = User()
    user.set_phone(phone)
    user.set_password(password)

    try:
        user_dao = UserDAO()
        user_dao.add(user)
        result = return_status(0)
        return jsonify(result)  # 注册成功
    except:
        return "Server failure!"


# 验证电话号码
def verify_phone(phone):
    return False


# 验证手机格式
def verify_phone_format(phone):
    return False


# 退出账号
@app.route('/user/logout', methods=['GET'])
def logout():
    result = return_status(0)
    return jsonify(result)


# 获取个人信息
# 已修改
@app.route('/user/profile', methods=['GET'])
def getInformation():
    auth = request.headers.get('Authorization')
    auth_user_id = Auth.identify(auth)

    # Authorization header不正确
    if auth_user_id is None:
        result = return_status(-2)
        return jsonify(result)

    user_id = request.args.get('userid')

    information = Information()

    if user_id is None:
        # user_id空取JWT中id
        information.set_user_id(auth_user_id)
    else:
        # user_id不为空取user_id
        information.set_user_id(user_id)

    try:
        information = InformationDAO().retrieve(information)
        if information is None:
            # 用户不存在
            result = return_status(-1)
            return jsonify(result)
        else:
            # 返回用户信息
            result = return_Information(0, information)
            return jsonify(result)
    except:
            result = return_status(-2)
            return jsonify(result)


# 修改个人信息
# 已修改
@app.route('/user/profile', methods=['POST'])
def modifyInformation():
    auth = request.headers.get('Authorization')
    auth_user_id = Auth.identify(auth)

    # Authorization header不正确
    if auth_user_id is None:
        result = return_status(-2)
        return jsonify(result)

    # 获取用户
    user = User()
    user.set_user_id(auth_user_id)
    user_dao = UserDAO()
    try:
        retrieve_user = user_dao.retrieve(user)
    except:
        result = return_status(-2)
        return jsonify(result)

    # 用户不存在
    if retrieve_user is None:
        result = return_status(-1)
        return jsonify(result)

    information = Information()
    information.set_user_id(auth_user_id)

    data = request.get_json()
    if 'NickName' not in data:
        return "上传的信息不完整"
    nick_name = data['NickName']
    nick_name = str(nick_name)
    information.set_nick_name(nick_name)

    if 'Avatar' not in data:
        return "上传的信息不完整"
    avatar = data['Avatar']
    avatar = str(avatar)
    information.set_avatar(avatar)

    if 'Signature' not in data:
        return "上传的信息不完整"
    signature = data['Signature']
    signature = str(signature)
    information.set_signature(signature)

    if 'BackgroundPhoto' not in data:
        return "上传的信息不完整"
    background_photo = data['BackgroundPhoto']
    background_photo = str(background_photo)
    information.set_background_photo(background_photo)

    information_dao = InformationDAO()
    result = information_dao.update(information)
    result = return_status(result)
    return jsonify(result)


# 创建文件夹
def mkdir(folder_path):
    folder = os.path.exists(folder_path)
    if not folder:
        os.makedirs(folder_path)
    return folder_path


# 上传头像
@app.route('/user/avatar', methods=['POST'])
def upload_avatar():
    auth = request.headers.get('Authorization')
    auth_user_id = Auth.identify(auth)

    # Authorization header不正确
    if auth_user_id is None:
        result = return_status(-2)
        return jsonify(result)

    # 获取用户
    user = User()
    user.set_user_id(auth_user_id)
    user_dao = UserDAO()
    try:
        retrieve_user = user_dao.retrieve(user)
    except:
        result = return_status(-2)
        return jsonify(result)

    # 用户不存在
    if retrieve_user is None:
        result = return_status(-1)
        return jsonify(result)

    # 设置路径
    folder_path = 'avatar/' + str(auth_user_id)
    mkdir(folder_path)

    information = Information()
    information.set_user_id(auth_user_id)
    path = folder_path + '/avatar.jpg'
    information.set_avatar(path)

    # 读取头像图片
    try:
        avatar = request.get_data()
        if avatar is None:
            return "上传的图片为空"
        with open(path, 'wb') as f:
            f.write(avatar)
    except:
        result = return_status(-2)
        return jsonify(result)

    # 数据库修改
    information_dao = InformationDAO()
    try:
        result = information_dao.update_avatar(information)
        if result is not None:
            result = return_homepage(result, path)
            return jsonify(result)
        else:
            result = return_status(-2)
            return jsonify(result)
    except:
        result = return_status(-2)
        return jsonify(result)


# 上传个人主页图
@app.route('/user/homepage', methods=['POST'])
def upload_homepage():
    auth = request.headers.get('Authorization')
    auth_user_id = Auth.identify(auth)

    # Authorization header不正确
    if auth_user_id is None:
        result = return_status(-2)
        return jsonify(result)

    # 获取用户
    user = User()
    user.set_user_id(auth_user_id)
    user_dao = UserDAO()
    try:
        retrieve_user = user_dao.retrieve(user)
    except:
        result = return_status(-2)
        return jsonify(result)

    # 用户不存在
    if retrieve_user is None:
        result = return_status(-1)
        return jsonify(result)

    # 设置路径
    folder_path = 'background/' + str(auth_user_id)
    mkdir(folder_path)

    information = Information()
    path = folder_path + '/background.jpg'
    information.set_user_id(auth_user_id)
    information.set_background_photo(path)

    # 读取背景图片
    try:
        homepage = request.get_data()
        if homepage is None:
            return "上传的图片为空"
        with open(path, 'wb') as f:
            f.write(homepage)
    except:
        result = return_status(-2)
        return jsonify(result)

    # 数据库修改
    information_dao = InformationDAO()
    try:
        result = information_dao.update_background_photo(information)
        if result is not None:
            result = return_homepage(result, path)
            return jsonify(result)
        else:
            result = return_status(-2)
            return jsonify(result)
    except:
        result = return_status(-2)
        return jsonify(result)


# 获取我关注的列表
@app.route('/user/following', methods=['GET'])
def following():
    auth = request.headers.get('Authorization')
    auth_user_id = Auth.identify(auth)

    # Authorization header不正确
    if auth_user_id is None:
        result = return_status(-2)
        return jsonify(result)

    # 获取用户
    user = User()
    user.set_user_id(auth_user_id)
    user_dao = UserDAO()
    try:
        retrieve_user = user_dao.retrieve(user)
    except:
        result = return_status(-2)
        return jsonify(result)

    # 用户不存在
    if retrieve_user is None:
        result = return_status(-1)
        return jsonify(result)

    following_dao = FollowingDAO()
    try:
        followings = following_dao.retrieve(retrieve_user.get_user_id())
        results = return_following(followings)
        return jsonify(results)
    except:
        result = return_status(-2)
        return jsonify(result)


# 点击/取消关注
@app.route('/user/follow', methods=['POST'])
def follow():
    auth = request.headers.get('Authorization')
    auth_user_id = Auth.identify(auth)

    # Authorization header不正确
    if auth_user_id is None:
        result = return_status(-2)
        return jsonify(result)

    # 获取用户
    user = User()
    user.set_user_id(auth_user_id)
    user_dao = UserDAO()
    try:
        retrieve_user = user_dao.retrieve(user)
    except:
        result = return_status(-2)
        return jsonify(result)

    # 用户不存在
    if retrieve_user is None:
        result = return_status(-1)
        return jsonify(result)

    data = request.get_json()

    if 'UserID' not in data or 'Cancel' not in data:
        return "信息缺失"
    user_id = data['UserID']
    cancel_follow = data['Cancel']

    follow_dao = FollowDAO()
    if cancel_follow == 'True' or cancel_follow == 'true' or cancel_follow is True:
        follow_dao.delete(user_id, auth_user_id)
        result = return_status(1)
        return jsonify(result)
    if cancel_follow == 'False' or cancel_follow == 'false' or cancel_follow is False:
        follow_dao.add(user_id, auth_user_id)
        result = return_status(0)
        return jsonify(result)
    else:
        result = return_status(-1)
        return jsonify(result)

# 获取关注我的列表
@app.route('/user/follower', methods=['GET'])
def follower():
    auth = request.headers.get('Authorization')
    auth_user_id = Auth.identify(auth)

    # Authorization header不正确
    if auth_user_id is None:
        result = return_status(-2)
        return jsonify(result)

    # 获取用户
    user = User()
    user.set_user_id(auth_user_id)
    user_dao = UserDAO()
    try:
        retrieve_user = user_dao.retrieve(user)
    except:
        result = return_status(-2)
        return jsonify(result)

    # 用户不存在
    if retrieve_user is None:
        result = return_status(-1)
        return jsonify(result)

    follower_dao = FollowerDAO()
    try:
        followers = follower_dao.retrieve(retrieve_user.get_user_id())
        results = return_follower(followers)
        return jsonify(results)
    except:
        result = return_status(-2)
        return jsonify(result)


# 获取11位随机数
def get_work_id():
    return random.randint(10000000000, 99999999999)


# 获取个人作品
@app.route('/illustration/mywork', methods=['GET'])
def get_myworks():
    auth = request.headers.get('Authorization')
    auth_user_id = Auth.identify(auth)

    # Authorization header不正确
    if auth_user_id is None:
        result = return_status(-2)
        return jsonify(result)

    user_id = request.args.get('userid')
    if user_id is None:
        return "信息不完整"

    # 获取用户
    user = User()
    user.set_user_id(user_id)
    user_dao = UserDAO()
    try:
        retrieve_user = user_dao.retrieve(user)
    except:
        result = return_status(-2)
        return jsonify(result)

    # 用户不存在
    if retrieve_user is None:
        result = return_status(-1)
        return jsonify(result)

    type = request.args.get('type')
    if type is None:
        return "信息不完整"
    type = str(type)

    top = request.args.get('top')
    if top is None:
        return "信息不完整"
    top = str(top)

    work_dao = WorkDAO()
    works = work_dao.retrieve(user_id)
    if type == 'home':
        if top is 'true' or top is 'True':
            pass
        else:
            result = return_home(works)
            return jsonify(result)
    if type == 'detail':
        if top is 'true' or top is 'True':
            pass
        else:
            result = return_detail(works)
            return jsonify(result)
    else:
        return "信息不正确"

# 获取作品图片
@app.route('/illustration/image', methods=['GET'])
def get_image():
    auth = request.headers.get('Authorization')
    auth_user_id = Auth.identify(auth)

    # Authorization header不正确
    if auth_user_id is None:
        result = return_status(-2)
        return jsonify(result)

    # 获取用户
    # user = User()
    # user.set_user_id(auth_user_id)
    # user_dao = UserDAO()
    # try:
    #     retrieve_user = user_dao.retrieve(user)
    # except:
    #     result = return_status(-2)
    #     return jsonify(result)

    # 用户不存在
    # if retrieve_user is None:
    #     result = return_status(-1)
    #     return jsonify(result)

    id = request.args.get('id')
    if id is None:
        return "信息不完整"
    id = int(id)

    size = request.args.get('size')
    if size is None:
        size = None
    else:
        size = str(size)

    type = request.args.get('type')
    if type is None:
        type = None
    else:
        type = str(type)
    print(type)
    print(size)

    path = WorkDAO().retrieve_address(id)
    if size == 'mid':
        if type == 'sketch':
            path = path + '/sketch.jpg'
        else:
            if type is None or type == 'sketch':
                path = path + '/work.jpg'
            else:
                return "信息不正确"
    else:
        if size is None:
            if type == 'sketch':
                path = path + '/sketch.jpg'
            else:
                if type is None or type == 'sketch':
                    path = path + '/work.jpg'
                else:
                    return "信息不正确"
        else:
            return "信息不正确"

    try:
        with open(path, 'rb') as f:
            image = f.read()
            response = Response(image, mimetype='image/jpg')
            return response
    except:
        return "Server Failure"


# 获取收藏作品
@app.route('/illustration/mylike', methods=['GET'])
def get_mylike():
    auth = request.headers.get('Authorization')
    auth_user_id = Auth.identify(auth)

    # Authorization header不正确
    if auth_user_id is None:
        result = return_status(-2)
        return jsonify(result)

    user_id = request.args.get('userid')
    if user_id is None:
        return "信息不完整"
    user_id = int(user_id)

    # 获取用户
    user = User()
    user.set_user_id(user_id)
    user_dao = UserDAO()
    try:
        retrieve_user = user_dao.retrieve(user)
    except:
        result = return_status(-2)
        return jsonify(result)

    # 用户不存在
    if retrieve_user is None:
        result = return_status(-1)
        return jsonify(result)

    my_like_work_ids = user_dao.get_my_like(retrieve_user)

    my_like_works = WorkDAO().list(my_like_work_ids)

    start = request.args.get('start')
    if start is None:
        return "信息不完整"
    start = int(start)

    count = request.args.get('count')
    if count is None:
        return "信息不完整"
    count = int(count)

    type = request.args.get('type')
    if type is None:
        return "信息不完整"
    type = str(type)

    if type == 'home':
        result = return_home_my_like(my_like_works, start, count)
        return jsonify(result)
    if type == 'detail':
        result = return_detail_my_like(my_like_works, start, count)
        return jsonify(result)
    else:
        return "信息不正确"


# 收藏作品
@app.route('/illustration/mylike', methods=['POST'])
def like():
    auth = request.headers.get('Authorization')
    auth_user_id = Auth.identify(auth)

    # Authorization header不正确
    if auth_user_id is None:
        result = return_status(-2)
        return jsonify(result)

    # 获取用户
    user = User()
    user.set_user_id(auth_user_id)
    user_dao = UserDAO()
    try:
        retrieve_user = user_dao.retrieve(user)
    except:
        result = return_status(-2)
        return jsonify(result)

    # 用户不存在
    if retrieve_user is None:
        result = return_status(-1)
        return jsonify(result)

    data = request.get_json()

    if 'id' not in data or 'Cancel' not in data:
        return "信息缺失"
    id = data['id']
    cancel_like = data['Cancel']

    work_dao = WorkDAO()
    if cancel_like == 'True' or cancel_like == 'true' or cancel_like is True:
        work_dao.delete_my_like(auth_user_id, id)
        result = return_status(1)
        return jsonify(result)
    if cancel_like == 'False' or cancel_like == 'false' or cancel_like is False:
        work_dao.add_my_like(auth_user_id, id)
        result = return_status(0)
        return jsonify(result)
    else:
        result = return_status(-1)
        return jsonify(result)


# 获取作品详情
@app.route('/illustration/sketchwork', methods=['GET'])
def get_sketchwork():
    auth = request.headers.get('Authorization')
    auth_user_id = Auth.identify(auth)

    # Authorization header不正确
    if auth_user_id is None:
        result = return_status(-2)
        return jsonify(result)

    # 获取用户
    # user = User()
    # user.set_user_id(auth_user_id)
    # user_dao = UserDAO()
    # try:
    #     retrieve_user = user_dao.retrieve(user)
    # except:
    #     result = return_status(-2)
    #     return jsonify(result)

    # 用户不存在
    # if retrieve_user is None:
    #     result = return_status(-1)
    #     return jsonify(result)

    id = request.args.get('id')
    if id is None:
        return "信息不完整"
    id = int(id)

    work_dao = WorkDAO()
    try:
        work = work_dao.retrieve_information(id)
        result = return_detail_work(work)
        return jsonify(result)
    except:
        return 'Server Failure'


# 搜索作品
@app.route('/illustration/search', methods=['GET'])
def search():
    keywords = request.args.get('keywords')
    keywords = str(keywords)
    return "search"


# 获取受欢迎的线稿
@app.route('/illustration/favorite_sketch', methods=['GET'])
def get_favorite_sketch():
    return 'get_favorite_sketch'


# 获取受欢迎的上色
@app.route('/illustration/favorite_colorization', methods=['GET'])
def get_favorite_colorization():
    return 'get_favorite_colorization'


# 今日推荐作品
@app.route('/illustration/todays', methods=['GET'])
def get_todays():
    return "get_todays"


# 发布作品
@app.route('/illustration/upload', methods=['POST'])
def upload():
    auth = request.headers.get('Authorization')
    auth_user_id = Auth.identify(auth)

    # Authorization header不正确
    if auth_user_id is None:
        result = return_status(-2)
        return jsonify(result)

    # 获取用户
    user = User()
    user.set_user_id(auth_user_id)
    user_dao = UserDAO()
    try:
        retrieve_user = user_dao.retrieve(user)
    except:
        result = return_status(-2)
        return jsonify(result)

    # 用户不存在
    if retrieve_user is None:
        result = return_status(-1)
        return jsonify(result)

    data = request.get_json()
    if 'name' not in data or 'created' not in data or 'description' not in data or 'tags' not in data or 'allow_download' not in data or 'allow_sketch' not in data or 'allow_fork' not in data or 'original_image' not in data or 'colorization_image' not in data:
        return '信息不完整'

    work = Work()
    work.set_artist(auth_user_id)

    name = data['name']
    name = str(name)
    work.set_name(name)

    created_time = data['created']
    created_time = str(created_time)
    work.set_created(created_time)

    description = data['description']
    description = str(description)
    work.set_description(description)

    tags = data['tags']
    work.set_tags(tags)

    allow_downloaded = data['allow_download']
    allow_downloaded = bool(allow_downloaded)
    work.set_allow_fork(allow_downloaded)

    allow_sketch = data['allow_sketch']
    allow_sketch = bool(allow_sketch)
    work.set_allow_sketch(allow_sketch)

    allow_fork = data['allow_fork']
    allow_fork = bool(allow_fork)
    work.set_allow_fork(allow_fork)

    original_image = data['original_image']
    original_image = str(original_image)

    colorization_image = data['colorization_image']
    colorization_image = str(colorization_image)

    address = Address()
    address.set_original_image(original_image)
    address.set_colorization_image(colorization_image)

    work_dao = WorkDAO()
    try:
        work_dao.add_work(work, address)
        result = return_status(0)
        return jsonify(result)
    except:
        result = return_status(-2)
        return jsonify(result)


def get_request_image(image):
    image = re.sub('^data:image/.+;base64,', '', image)
    image = base64.urlsafe_b64decode(image)
    image = np.fromstring(image, dtype=np.uint8)
    image = cv2.imdecode(image, -1)
    return image


# pool = []
# lock = 1
#
#
def handle_colorization(pool):
    # mutex = threading.Lock()
    # 锁定
    # mutex.acquire(lock)
    # print(len(pool))
    # if len(pool) > 0:
    #     sketch, points, path = pool[0]
    #     del pool[0]
    # else:
    #     return
    # 释放
    # mutex.release()
    sketch, points, path = pool
    improved_sketch = sketch.copy()
    improved_sketch = min_resize(improved_sketch, 512)
    improved_sketch = cv_denoise(improved_sketch)
    improved_sketch = sensitive(improved_sketch, s=5.0)
    improved_sketch = go_tail(improved_sketch)

    std = cal_std(improved_sketch)
    if std > 100.0:
        improved_sketch = go_passline(improved_sketch)
        improved_sketch = min_k_down_c(improved_sketch, 2)
        improved_sketch = cv_denoise(improved_sketch)
        improved_sketch = go_tail(improved_sketch)
        improved_sketch = sensitive(improved_sketch, s=5.0)

    improved_sketch = min_black(improved_sketch)
    improved_sketch = cv2.cvtColor(improved_sketch, cv2.COLOR_BGR2GRAY)
    sketch_1024 = k_resize(improved_sketch, 64)
    sketch_256 = mini_norm(k_resize(min_k_down(sketch_1024, 2), 16))
    sketch_128 = hard_norm(sk_resize(min_k_down(sketch_1024, 4), 32))

    baby = go_baby(sketch_128, opreate_normal_hint(ini_hint(sketch_128), points, type=0, length=1))
    baby = de_line(baby, sketch_128)
    for _ in range(16):
        baby = blur_line(baby, sketch_128)
    baby = go_tail(baby)
    baby = clip_15(baby)

    composition = go_gird(sketch=sketch_256, latent=d_resize(baby, sketch_256.shape), hint=ini_hint(sketch_256))
    composition = go_tail(composition)

    painting_function = go_head
    reference = None
    alpha = 0
    result = painting_function(
        sketch=sketch_1024,
        global_hint=k_resize(composition, 14),
        local_hint=opreate_normal_hint(ini_hint(sketch_1024), points, type=2, length=2),
        global_hint_x=k_resize(reference, 14) if reference is not None else k_resize(composition, 14),
        alpha=(1 - alpha) if reference is not None else 1
    )
    result = go_tail(result)
    cv2.imwrite(path, result)
    return


# 提交上色请求
@app.route('/illustration/colorization', methods=['POST'])
def colorization():
    auth = request.headers.get('Authorization')
    auth_user_id = Auth.identify(auth)

    # Authorization header不正确
    if auth_user_id is None:
        result = return_status(-2)
        return jsonify(result)

    # 获取用户
    user = User()
    user.set_user_id(auth_user_id)
    user_dao = UserDAO()
    try:
        retrieve_user = user_dao.retrieve(user)
    except:
        result = return_status(-2)
        return jsonify(result)

    # 用户不存在
    if retrieve_user is None:
        result = return_status(-1)
        return jsonify(result)

    # 获取信息
    data = request.get_json()
    if 'image' not in data or 'points' not in data:
        return "信息不完整"

    image = data['image']

    points = data['points']
    for _ in range(len(points)):
        points[_][1] = 1 - points[_][1]

    # data = datas['data']
    #
    # anchor = data['anchor']
    # anchor_x = anchor['x']
    # anchor_y = anchor['y']
    # anchor_color = anchor['color']
    # print(anchor_x + ' ' + anchor_y + ' ' + anchor_color)
    #
    # hint = data['hint']

    # 处理图片
    try:
        image = get_request_image(image)
        image = from_png_to_jpg(image)
    except:
        result = return_status(-1)
        return jsonify(result)

    # 生成图片id
    id = get_work_id()

    path = 'works/' + str(auth_user_id) + '/' + str(id)
    path = mkdir(path)

    cv2.imwrite(path + '/sketch.jpg', image)

    address = Address()
    address.set_work_id(id)
    address.set_user_id(auth_user_id)
    address.set_path(path)
    original_image = str(auth_user_id) + str(id) + '0'
    address.set_original_image(original_image)
    colorization_image = str(auth_user_id) + str(id) + '1'
    address.set_colorization_image(colorization_image)
    receipt = str(id) + 'r' + str(auth_user_id)
    address.set_receipt(receipt)

    address_dao = AddressDAO()
    address_dao.add(address)

    path = path + '/result.jpg'
    pool = [image, points, path]
    threading.Thread(target=handle_colorization, args=(pool, )).start()
    # cv2.imwrite(path, image)

    result = return_receipt(0, address)
    return jsonify(result)


# 查询上色请求
@app.route('/illustration/colorization', methods=['GET'])
def get_receipt():
    auth = request.headers.get('Authorization')
    auth_user_id = Auth.identify(auth)

    # Authorization header不正确
    if auth_user_id is None:
        result = return_status(-2)
        return jsonify(result)

    receipt = request.args.get('receipt')
    if receipt is None:
        return '信息不完整'

    receipt = str(receipt)
    address = Address()
    address.set_receipt(receipt)

    address_dao = AddressDAO()
    address = address_dao.retrieve(address)

    if address is None:
        result = return_status(-1)
        return jsonify(result)

    path = address.get_path() + '/result.jpg'
    flag = os.path.exists(path)
    if flag:
        result = return_load(0, address)
        return jsonify(result)
    else:
        result = return_status(1)
        return jsonify(result)


# def handle_threading():
#     while True:
#         try:
#             handle_colorization()
#         except Exception as e:
#             print(e)

# threading.Thread(target=handle_threading).start()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)

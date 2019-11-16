import os
from random import random
import cv2
import numpy as np

from flask import *

from auth.Auth import Auth
from dao.FollowerDAO import FollowerDAO
from dao.FollowingDAO import FollowingDAO
from dao.ImageDAO import WorkDAO
from dao.UserDAO import UserDAO
from pojo.User import User

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


# 登录账户
@app.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()
    phone = data['phone']

    payload = data['password']
    payload = Auth.decode_auth_token(payload)
    # JWT 格式错误
    if 'password' not in payload:
        result = {"StatusCode": -1}
        return jsonify(result)

    password = payload['password']
    user = User()
    user.set_phone(phone)
    user.set_password(password)
    user = UserDAO().retrieve(user)

    # 用户不存在
    if user is None:
        result = {"StatusCode": -1}
        return jsonify(result)

    result = Auth.authorize(user)
    return jsonify(result)


# 注册账户
@app.route('/user/register', methods=['POST'])
def register():
    data = request.get_json()
    phone = data['phone']

    # 检测手机是否已经使用
    phone_is_used = verify_phone(phone)
    if phone_is_used:
        result = {'StatusCode': -1}  # 手机号码被使用
        return jsonify(result)

    # 检测手机格式是否正确
    phone_format_false = verify_phone_format(phone)
    if phone_format_false:
        result = {'StatusCode': -2}  # 手机格式不正确
        return jsonify(result)

    payload = data['password']
    payload = Auth.decode_auth_token(payload)
    password = payload['password']

    user = User()
    user.set_phone(phone)
    user.set_password(password)
    user_dao = UserDAO()
    user_dao.add(user)

    result = {'StatusCode': 0}
    return jsonify(result)  # 注册成功


# 验证电话号码
def verify_phone(phone):
    return False


# 验证手机格式
def verify_phone_format(phone):
    return False


# 退出账号
@app.route('/user/logout', methods=['GET'])
def logout():
    result = {"StatusCode": 0}
    return jsonify(result)


# 获取个人信息
@app.route('/user/profile', methods=['GET'])
def getInformation():
    auth = request.headers.get('Authorization')
    user_id = Auth.identify(auth)

    # Authorization header不正确
    if user_id is None:
        result = {"StatusCode": -2}
        return jsonify(result)

    id = request.args.get('id')
    user_id = int(user_id)
    id = int(id)

    # 认证信息不符合
    if user_id != id:
        result = {"StatusCode": -2}
        return jsonify(result)

    user_dao = UserDAO()
    retrieve_user = user_dao.get(user_id)

    # 用户不存在
    if retrieve_user is None:
        result = {"StatusCode": -1};
        return jsonify(result)

    follower_dao = FollowerDAO()
    following_dao = FollowingDAO()
    followers = follower_dao.retrieve(retrieve_user.get_user_id())
    followings = following_dao.retrieve(retrieve_user.get_user_id())
    retrieve_user.set_follower(followers)
    retrieve_user.set_following(followings)

    result = {
        "StatusCode": 0,
        "NickName": retrieve_user.get_nick_name(),
        "Avatar": retrieve_user.get_avatar(),
        "BackgroundPhoto": retrieve_user.get_background_photo(),
        "Signature": retrieve_user.get_signature(),
        "Follower": retrieve_user.get_follower(),
        "Following": retrieve_user.get_following(),
        "Rank": retrieve_user.get_rank()
    }
    return jsonify(result)


# 修改个人信息
@app.route('/user/profile', methods=['POST'])
def modifyInformation():
    # 获取user_id
    auth = request.headers.get('Authorization')
    user_id = Auth.identify(auth)

    # 获取用户
    user_dao = UserDAO()
    retrieve_user = user_dao.get(user_id)

    if retrieve_user is None:
        result = {"StatusCode":-1}
        return jsonify(result)

    data = request.get_json()
    nick_name = data['NickName']
    nick_name = str(nick_name)

    avatar = data['Avatar']
    avatar = str(avatar)

    signature = data['Signature']
    signature = str(signature)

    background_photo = data['BackgroundPhoto']
    background_photo = str(background_photo)

    retrieve_user.set_nick_name(nick_name)
    retrieve_user.set_avatar(avatar)
    retrieve_user.set_signature(signature)
    retrieve_user.set_background_photo(background_photo)
    result = user_dao.update(retrieve_user)
    return jsonify(result)


# 创建文件夹
def mkdir(folder_path):
    folder = os.path.exists(folder_path)
    if not folder:
        os.makedirs(folder_path)
    return

# 上传头像
@app.route('/user/avatar', methods=['POST'])
def upload_avatar():
    # 获取user_id
    auth = request.headers.get('Authorization')
    user_id = Auth.identify(auth)

    # 获取用户
    user_dao = UserDAO()
    retrieve_user = user_dao.get(user_id)

    # 用户不存在
    if retrieve_user is None:
        result = {"StatusCode": -1}
        return jsonify(result)

    # 设置路径
    folder_path = 'avatar/' + str(user_id)
    mkdir(folder_path)

    path = folder_path + '/avatar.jpg'
    retrieve_user.set_avatar(path)

    # 读取头像图片
    avator = request.files['Avatar']
    avator.save(path)

    # 数据库修改
    result = user_dao.update_avatar(retrieve_user)
    return jsonify(result)


# 上传个人主页图
@app.route('/user/homepage', methods=['POST'])
def upload_homepage():
    # 获取user_id
    auth = request.headers.get('Authorization')
    user_id = Auth.identify(auth)

    # 获取用户
    user_dao = UserDAO()
    retrieve_user = user_dao.get(user_id)

    # 用户不存在
    if retrieve_user is None:
        result = {"StatusCode": -1}
        return jsonify(result)

    # 设置路径
    folder_path = 'background/' + str(user_id)
    mkdir(folder_path)

    path = folder_path + '/background.jpg'
    retrieve_user.set_background_photo(path)

    # 读取背景图片
    homepage = request.files['Homepage']
    homepage.save(path)

    # 数据库修改
    result = user_dao.update_background_photo(retrieve_user)
    return jsonify(result)


# 获取我关注的列表
@app.route('/user/following', methods=['GET'])
def following():
    # 获取user_id
    auth = request.headers.get('Authorization')
    user_id = Auth.identify(auth)

    # 获取用户
    user_dao = UserDAO()
    retrieve_user = user_dao.get(user_id)

    # 用户不存在
    if retrieve_user is None:
        result = {"StatusCode": -1}
        return jsonify(result)

    following_dao = FollowingDAO()
    followings = following_dao.retrieve(retrieve_user.get_user_id())
    results = following_dao.get(followings)
    return jsonify(results)


# 获取关注我的列表
@app.route('/user/follower', methods=['GET'])
def follower():
    # 获取user_id
    auth = request.headers.get('Authorization')
    user_id = Auth.identify(auth)

    # 获取用户
    user_dao = UserDAO()
    retrieve_user = user_dao.get(user_id)

    # 用户不存在
    if retrieve_user is None:
        result = {"StatusCode": -1}
        return jsonify(result)

    follower_dao = FollowerDAO()
    followers = follower_dao.retrieve(retrieve_user.get_user_id())
    results = follower_dao.get(followers)
    return jsonify(results)


# 获取11位随机数
def get_work_id():
    return random.randint(10000000000, 99999999999)


# 获取个人作品
@app.route('/illustration/mywork', methods=['GET'])
def get_myworks():
    # 获取user_id
    auth = request.headers.get('Authorization')
    user_id = Auth.identify(auth)

    # 获取用户
    user_dao = UserDAO()
    retrieve_user = user_dao.get(user_id)

    # 用户不存在
    if retrieve_user is None:
        result = {"StatusCode": -1}
        return jsonify(result)

    type = request.args.get('type')
    type = str(type)
    print(type)

    top = request.args.get('top')
    top = str(top)
    print(top)

    work_dao = WorkDAO()
    if type == 'home':
        if top is 'true' or top is 'True':
            pass
        else:
            result = work_dao.home_retrieve(user_id)
            return jsonify(result)
    else:
        if top is 'true' or top is 'True':
            pass
        else:
            result = work_dao.detail_retrieve(user_id)
            return jsonify(result)


# 获取作品图片
@app.route('/illustration/image', methods=['GET'])
def get_image():
    # 获取user_id
    auth = request.headers.get('Authorization')
    user_id = Auth.identify(auth)

    # 获取用户
    user_dao = UserDAO()
    retrieve_user = user_dao.get(user_id)

    # 用户不存在
    if retrieve_user is None:
        result = {"StatusCode": -1}
        return jsonify(result)

    id = request.args.get('id')
    id = int(id)

    size = request.args.get('size')
    size = str(size)

    type = request.args.get('type')
    type = str(type)

    path = WorkDAO().retrieve_address(id)
    if size is None:
        if type == 'sketch':
            path = path + '/sketch.jpg'
        else:
            path = path + '/work.jpg'
    else:
        if type == 'sketch':
            path = path + '/sketch.jpg'
        else:
            path = path + '/work.jpg'

    with open(path, 'rb') as f:
        image = f.read()
    response = Response(image, mimetype='text/jpg')
    return response


# 获取收藏作品
@app.route('/illustration/mylike', methods=['GET'])
def get_mylike():
    # 获取user_id
    auth = request.headers.get('Authorization')
    user_id = Auth.identify(auth)

    # 获取用户
    user_dao = UserDAO()
    retrieve_user = user_dao.get(user_id)

    # 用户不存在
    if retrieve_user is None:
        result = {"StatusCode": -1}
        return jsonify(result)

    id = request.args.get('userid')
    id = int(id)

    my_like_work_ids = user_dao.get_my_like(retrieve_user.get_user_id())
    my_like_works = WorkDAO().list(my_like_work_ids)

    start = request.args.get('start')
    start = int(start)

    count = request.args.get('count')
    count = int(count)

    type = request.args.get('type')
    type = str(type)


    return "get_mylike"


# 获取作品详情
@app.route('/illustration/sketchwork', methods=['GET'])
def get_sketchwork():
    id = request.args.get('id')
    id = int(id)
    return "get_sketchwork"


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
    data = request.get_json()
    name = data['name']
    name = str(name)

    created_time = data['created']
    created_time = str(created_time)

    description = data['description']
    description = str(description)

    tags = data['tags']

    allow_downloaded = data['allow_download']
    allow_downloaded = bool(allow_downloaded)

    allow_sketch = data['allow_sketch']
    allow_sketch = bool(allow_sketch)

    allow_fork = data['allow_fork']
    allow_fork = bool(allow_fork)

    original_image = data['original_image']
    original_image = str(original_image)

    colorization_image = data['colorization_image']
    colorization_image = str(colorization_image)
    return 'upload'


# 提交上色请求
app.route('/illustration/colorization', methods=['POST'])


def colorization():
    return


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

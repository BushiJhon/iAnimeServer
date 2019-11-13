from flask import *

from auth.Auth import Auth
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

    password = data['password']
    password = str(password)

    user = User()
    user.set_phone(phone)
    user.set_password(password)
    user = UserDAO().retrieve(user)

    if user is None:
        result = {"StatusCode": -1}
        return jsonify(result)

    auth = Auth()
    result = auth.authorize(user)
    return jsonify(result)


# 注册账户
@app.route('/user/register', methods=['POST'])
def register():
    data = request.get_json()
    phone = data['phone']
    phone = int(phone)

    phone_is_used = verify_phone(phone)
    if phone_is_used:
        result = {'StatusCode': -1}     # 手机号码被使用
        return jsonify(result)

    phone_format_false = verify_phone_format(phone)
    if phone_format_false:
        result = {'StatusCode': -2}     # 手机格式不正确
        return jsonify(result)

    password = data['password']
    password = str(password)

    user = User()
    user.set_phone(phone)
    user.set_password(password)
    user_dao = UserDAO()
    user_dao.add(user)

    result = {'StatusCode': 0}
    return jsonify(result)      # 注册成功


# 验证电话号码
def verify_phone(phone):
    return False


# 验证手机格式
def verify_phone_format(phone):
    return True


# 退出账号
@app.route('/user/logout', methods=['GET'])
def logout():
    return


# 获取个人信息
@app.route('/user/profile', methods=['GET'])
def getInformation():
    id = request.args.get('id')
    id = int(id)
    print(id)
    return "getInformation Success"


# 修改个人信息
@app.route('/user/profile', methods=['POST'])
def modifyInformation():
    data = request.get_json()
    nick_name = data['NickName']
    nick_name = str(nick_name)

    avatar = data['Avatar']
    avatar = str(avatar)

    signature = data['Signature']
    signature = str(signature)

    background_photo = data['BackgroundPhoto']
    background_photo = str(background_photo)

    return "modifyInformation Success"

# 上传头像
@app.route('/user/avator', methods=['POST'])
def upload_avator():
    avator = request.files['Avator']
    avator.save('uploads/uploaded_avator.jpg')
    return 'avator'


# 上传个人主页图
@app.route('/user/homepage')
def upload_homepage():
    homepage = request.files['Homepage']
    homepage.save('uploads/uploaded_avator.jpg')
    return 'homepage'


# 获取我关注的列表
@app.route('/user/following', methods=['GET'])
def following():
    return "following"

# 获取关注我的列表
@app.route('/user/follower', methods=['GET'])
def follower():
    return "follower"


# 获取个人作品
@app.route('/illustration/mywork', methods=['GET'])
def get_myworks():
    id = request.args.get('userid')
    id = int(id)

    type = request.args.get('type')
    type = str(type)

    top = request.args.get('top')
    top = bool(top)
    return "get_mywork"

# 获取作品图片
@app.route('/illustration/image', methods=['GET'])
def get_image():
    id = request.args.get('id')
    id = int(id)

    size = request.args.get('size')
    size = str(size)

    type = request.args.get('type')
    type = str(type)
    return "get_image"

# 获取收藏作品
@app.route('/illustration/mylike', methods=['GET'])
def get_mylike():
    id = request.args.get('userid')
    id = int(id)

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

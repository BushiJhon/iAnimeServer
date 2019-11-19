# 返回状态码
def return_status(status_code):
    reuslt = {"StatusCode": status_code}
    return reuslt


# 返回个人信息
def return_Information(status_code, information):
    result = {
        "StatusCode": status_code,
        "NickName": information.get_nick_name(),
        "Avatar": information.get_avatar(),
        "BackgroundPhoto": information.get_background_photo(),
        "Signature": information.get_signature(),
        "Follower": information.get_follower(),
        "Following": information.get_following(),
        "Rank": information.get_rank()
    }
    return result


# 返回头像地址
def return_avatar(status_code, avatar):
    result = {
        "StatusCode": status_code,
        "Avatar": avatar
    }
    return result


# 返回背景地址
def return_homepage(status_code, homepage):
    result = {
        "StatusCode": status_code,
        "Homepage": homepage
    }
    return result


# 返回关注列表
def return_following(follows):
    result = []
    for index in range(len(follows)):
        sub_result = {
            "NickName": follows[index].get_name(),
            "UserID": follows[index].get_following_id(),
            "Avatar": follows[index].get_avatar()
        }
        result.append(sub_result)
    return result


# 返回被关注列表
def return_follower(follows):
    result = []
    for index in range(len(follows)):
        sub_result = {
            "NickName": follows[index].get_name(),
            "UserID": follows[index].get_follower_id(),
            "Avatar": follows[index].get_avatar()
        }
        result.append(sub_result)
    return result


# home模式
def return_home(works):
    result = []
    for index in range(len(works)):
        sub_result = {
            "id": works[index].get_id(),
            "name": works[index].get_name(),
            "created": works[index].get_created(),
            "artist_name": works[index].get_artist_name()
        }
        result.append(sub_result)
    return result


# detail模式
def return_detail(works):
    result = []
    for index in range(len(works)):
        sub_result = {
            "id": works[index].get_id(),
            "artist": works[index].get_artist(),
            "artist_name": works[index].get_artist_name(),
            "name": works[index].get_name(),
            "created": works[index].get_created(),
            "description": works[index].get_description(),
            "tags": works[index].get_tags(),
            "forks": works[index].get_forks(),
            "like": works[index].get_likes(),
            "allow_download": works[index].get_allow_download(),
            "allow_sketch": works[index].get_allow_sketch(),
            "allow_fork": works[index].get_allow_fork()
        }
        result.append(sub_result)
    return result


def return_detail_work(work):
    result = {
        "id": work.get_id(),
        "artist": work.get_artist(),
        "artist_name": work.get_artist_name(),
        "name": work.get_name(),
        "created": work.get_created(),
        "description": work.get_description(),
        "tags": work.get_tags(),
        "forks": work.get_forks(),
        "like": work.get_likes(),
        "allow_download": work.get_allow_download(),
        "allow_sketch": work.get_allow_sketch(),
        "allow_fork": work.get_allow_fork()
    }
    return result


# home模式
def return_home_my_like(works, start, count):
    result = []
    if count > len(works):
        count = len(works)
    for index in range(count):
        sub_result = {
            "id": works[index].get_id(),
            "name": works[index].get_name(),
            "created": works[index].get_created(),
            "artist_name": works[index].get_artist_name()
        }
        result.append(sub_result)
    return result


# detail模式
def return_detail_my_like(works, start, count):
    result = []
    if count > len(works):
        count = len(works)
    for index in range(count):
        sub_result = {
            "id": works[index].get_id(),
            "artist": works[index].get_artist(),
            "artist_name": works[index].get_artist_name(),
            "name": works[index].get_name(),
            "created": works[index].get_created(),
            "description": works[index].get_description(),
            "tags": works[index].get_tags(),
            "forks": works[index].get_forks(),
            "like": works[index].get_likes(),
            "allow_download": works[index].get_allow_download(),
            "allow_sketch": works[index].get_allow_sketch(),
            "allow_fork": works[index].get_allow_fork()
        }
        result.append(sub_result)
    return result


# 返回回执
def return_receipt(status_code, address):
    result = {
        "StatusCode": status_code,
        "Receipt": address.get_receipt(),
        "ImageID": address.get_original_image()
    }
    return result


# 返回进度
def return_load(status_code, address):
    result = {
        "StatusCode": status_code,
        "ImageID": address.get_colorization_image(),
        "url": address.get_path() + '/result.jpg'
    }
    return result
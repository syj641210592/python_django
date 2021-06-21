def register_data():
    data = [
        {
            "title": "注册成功",
            "username": "sunwang2",
            "password": "334498sun",
            "password_confirm": "334498sun",
            "email": "6412105922@qq.com",
            "status_code": 200,
            "msg": "token"  # 只能填写返回字段数据的key值
        },
        {
            "title": "注册失败_用户名为空",
            "username": "",
            "password": "334498xsun",
            "password_confirm": "334498xsun",
            "email": "641210592x@qq.com",
            "status_code": 400,
            "msg": "username"  # 只能填写返回字段数据的key值
        },
        {
            "title": "注册失败_用户名重复",
            "username": "sunwang",
            "password": "334498xsun",
            "password_confirm": "334498xsun",
            "email": "641210592x@qq.com",
            "status_code": 400,
            "msg": "username"  # 只能填写返回字段数据的key值
        },
        {
            "title": "注册失败_密码为空",
            "username": "sunwangx",
            "password": "",
            "password_confirm": "334498xsun",
            "email": "641210592x@qq.com",
            "status_code": 400,
            "msg": "password"  # 只能填写返回字段数据的key值
        },
        {
            "title": "注册失败_确认密码不一致",
            "username": "sunwangx",
            "password": "334498xsun",
            "password_confirm": "334498xsunx",
            "email": "641210592x@qq.com",
            "status_code": 400,
            "msg": "password_confirm"  # 只能填写返回字段数据的key值
        },
        {
            "title": "注册失败_确认密码为空",
            "username": "sunwangx",
            "password": "334498xsun",
            "password_confirm": "",
            "email": "641210592x@qq.com",
            "status_code": 400,
            "msg": "password_confirm"  # 只能填写返回字段数据的key值
        },
        {
            "title": "注册失败_邮箱为空",
            "username": "sunwangx",
            "password": "334498xsun",
            "password_confirm": "334498xsun",
            "email": "",
            "status_code": 400,
            "msg": "email"  # 只能填写返回字段数据的key值
        },
        {
            "title": "注册失败_邮箱重复",
            "username": "sunwangx",
            "password": "334498xsun",
            "password_confirm": "334498xsun",
            "email": "641210592@qq.com",
            "status_code": 400,
            "msg": "email"  # 只能填写返回字段数据的key值
        }
    ]
    return data

from enum import Enum

class UserInfo(Enum):
    users = [ # 如果需要多人打卡，请按照下面的格式多填几个
        {
            'id': '', # 学工号
            'password': '', # 系统临时密码，默认为身份证后8位
            'password2': '', # 如果使用VPN，请输入新信息门户密码
            'enable': True # 若要启用，请设为True，反之为False
        },
        {
            'id': '', # 学工号
            'password': '', # 系统临时密码，默认为身份证后8位
            'password2': '', # 如果使用VPN，请输入新信息门户密码,
            'enable': False # 若要启用，请设为True，反之为False
        },
        {
            'id': '', # 学工号
            'password': '', # 系统临时密码，默认为身份证后8位
            'password2': '', # 如果使用VPN，请输入新信息门户密码,
            'enable': False # 若要启用，请设为True，反之为False
        },
    ]
    
    vpn = False # 经过VPN，默认为不经过
    auto_vpn = True # 若上项设置为不经过，当学校封网时，自动切换为经过VPN

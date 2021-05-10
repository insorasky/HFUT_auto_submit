from enum import Enum

class UserInfo(Enum):
    id = '' # 学工号
    password = '' # 系统临时密码，默认为身份证后8位

    vpn = False # 经过VPN，默认为不经过
    auto_vpn = True # 若上项设置为不经过，当学校封网时，自动切换为经过VPN
    password2 = '' # 如果使用VPN，请输入新信息门户密码

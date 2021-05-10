import requests, re, base64, json
from datetime import time, datetime
from enum import Enum
from utils.Student import Student
from utils.ECBPkcs7 import ECBPkcs7
from config import UserInfo

class Url(Enum):
    key = 'http://stu.hfut.edu.cn/xsfw/sys/emapfunauth/pages/funauth-login.do'
    login = 'http://stu.hfut.edu.cn/xsfw/sys/emapfunauth/loginValidate.do'
    initialize = 'http://stu.hfut.edu.cn/xsfw/sys/swpubapp/indexmenu/getAppConfig.do?appId=5811258723206966&appName=xsyqxxsjapp'
    date = 'http://stu.hfut.edu.cn/xsfw/sys/xsyqxxsjapp/mrbpa/getDateTime.do'
    time = 'http://stu.hfut.edu.cn/xsfw/sys/xsyqxxsjapp/mrbpa/getTsxx.do'
    jbxx = 'http://stu.hfut.edu.cn/xsfw/sys/xsyqxxsjapp/mrbpa/getJbxx.do'
    zxpaxx = 'http://stu.hfut.edu.cn/xsfw/sys/xsyqxxsjapp/mrbpa/getZxpaxx.do'
    save = 'http://stu.hfut.edu.cn/xsfw/sys/xsyqxxsjapp/mrbpa/saveMrbpa.do'

class Daka:
    __student = Student()
    __headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:88.0) Gecko/20100101 Firefox/88.0',
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
    }

    def __vpnLogin(self):
        return self.__student.login(UserInfo.id.value, UserInfo.id.password2) == True

    def __getCryptoKey(self):
        data = self.__student.request(Url.key.value).text
        regexp = r'cryptoKey = "(.*)"'
        key = re.findall(regexp, data)[0]
        return key

    def __encryptPwd(self, password):
        key = self.__getCryptoKey()
        return ECBPkcs7(key).encrypt(password)

    def __login(self):
        data = self.__student.request(
            url=Url.login.value,
            method='POST',
            headers=self.__headers,
            data={
                'userName': UserInfo.id.value,
                'password': self.__encryptPwd(UserInfo.password.value),
                'isWeekLogin': 'false'
            }
        ).json()
        if 'validate' in data:
            return data['validate'] == 'success'
        else:
            return False

    def __initialize(self):
        self.__student.request(Url.initialize.value)

    def __getZxpaxx(self):
        data = self.__student.request(
            url=Url.zxpaxx.value,
            method='POST',
            headers=self.__headers,
            data={'data': '{}'}
        ).json()
        if data['code'] == '0':
            return data['data']
        else:
            return False

    def __getJbxx(self):
        data = self.__student.request(
            url=Url.jbxx.value,
            method='POST',
            headers=self.__headers,
            data={'data': '{}'}
        ).json()
        if data['code'] == '0':
            return data['data']
        else:
            return False

    def __getDate(self):
        data = self.__student.request(
            url=Url.date.value,
            method='POST',
            headers=self.__headers,
            data={'data': '{}'}
        ).json()
        return data['data']['DQRQ']

    def __getTime(self):
        data = self.__student.request(
            url=Url.time.value,
            method='POST',
            headers=self.__headers,
            data={'data': '{}'}
        ).json()
        class Time:
            def __init__(self, start, end):
                start = re.findall(r'([0-9]{2})', start)
                end = re.findall(r'([0-9]{2})', end)
                self.start = time(hour=int(start[0]), minute=int(start[1]), second=int(start[2]))
                self.end = time(hour=int(end[0]), minute=int(end[1]), second=int(end[2]))
        return Time(data['data']['DZ_TBKSSJ'], data['data']['DZ_TBJSSJ'])

    def __save(self):
        zxpaxx = self.__getZxpaxx()
        jbxx = self.__getJbxx()
        data = {
            'data': json.dumps({
                'JBXX': json.dumps(jbxx),
                'MRQK': json.dumps({
                    'WID': '',
                    'XSBH': '',
                    'DZ_TBDZ': '',
                    'TW': '',
                    'BRJKZT': '',
                    'SFJZ': '',
                    'JTCYJKZK': '',
                    'XLZK': '',
                    'QTQK': '',
                    'TBSJ': self.__getDate(),
                    'DZ_SFSB': '1',
                    'BY1': '1',
                    **zxpaxx
                })
            })
        }
        data = self.__student.request(
            url=Url.save.value,
            method='POST',
            headers=self.__headers,
            data=data
        ).json()
        if data['code'] == '0':
            return True
        else:
            return data['msg']

    def __getIp(self):
        return self.__student.request('http://210.45.240.45/backend/getIP.php').json()['processedString']

    def run(self):
        if UserInfo.vpn.value:
            if self.__student.login(UserInfo.id.value, UserInfo.password2.value) is not True:
                print('新信息门户密码错误！')
                return
        print('当前IP地址为：', self.__getIp())
        try:
            logined = self.__login()
        except requests.exceptions.RequestException: # 你HFUT又双叒封网辣
            if UserInfo.auto_vpn and (not UserInfo.vpn):
                print("封网，正在尝试使用VPN")
                if self.__student.login(UserInfo.id.value, UserInfo.password2.value) is not True:
                    print('新信息门户密码错误！')
                    return
                print('WebVPN登录成功！')
                logined = self.__login()
            else:
                print("连接失败，可能又封网了！")
                return
        except:
            print("未知错误，可能又封网了！")
            return
        if logined:
            self.__initialize()
            times = self.__getTime()
            now = datetime.now()
            now = time(hour=now.hour, minute=now.minute, second=now.second)
            print('开始时间：', times.start)
            print('结束时间：', times.end)
            return
            if (now < times.end) and (now > times.start):
                saved = self.__save()
                if saved == True:
                    print('打卡成功！')
                else:
                    print('打卡失败！错误信息：', saved)
            else:
                print('在签到开放时间外！')
        else:
            print('帐号或密码错误！或错误次数过多，请明天再试！')


if __name__ == '__main__':
    daka = Daka()
    daka.run()

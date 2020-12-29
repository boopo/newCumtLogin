import requests
from bs4 import BeautifulSoup

from encrypt import get_token

#from settings import username, password

url_login = 'http://authserver.cumt.edu.cn/authserver/login?service=http%3A//portal.cumt.edu.cn/casservice'  # 登录
url_post = 'http://authserver.cumt.edu.cn/authserver/login?service=http%3A%2F%2Fportal.cumt.edu.cn%2Fcasservice'  # 提交表单
url_balance = 'http://portal.cumt.edu.cn/ykt/balance'  # 校园卡余额(未跳转)
url_balance_re1 = 'http://ykt.cumt.edu.cn:8088/ias/prelogin?sysid=FWDT'  # 一卡通跳转1
url_balance_re2 = 'http://ykt.cumt.edu.cn/cassyno/index'  # 一卡通跳转2
url_balance_history = 'http://ykt.cumt.edu.cn/Report/GetPersonTrjn'  # 一卡通流水按时间查询
url_balance2 = 'http://portal.cumt.edu.cn/ykt/flow?flow_num=20'  # 校园卡按逆序查询(未跳转)
url_balance_charge = 'http://ykt.cumt.edu.cn/User/Account_Pay'  # 校园卡充值(慎用！！！)
url_library = 'http://portal.cumt.edu.cn/portal/api/v1/api/http/40'  # 图书简单信息(未跳转)
url_library_re = 'http://121.248.104.188:8080/CASSSO/login.jsp'  # 图书馆认证跳转
url_library_Loan = 'https://findcumt.libsp.com/find/loanInfo/loanList'  # 图书馆当前借阅信息
url_library_loan_history = 'https://findcumt.libsp.com/find/loanInfo/loanHistoryList'  # 图书馆历史借阅信息
url_library_favorite = 'https://findcumt.libsp.com/find/favorites/recordList'  # 图书馆收藏列表

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 FireFox / 29.0",
    "X-Requested-With": "XMLHttpRequest"
}


class newIds:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.session = requests.session()

    def login(self):
        r = self.session.get(url=url_login, headers=headers)
        soup = BeautifulSoup(r.text, 'html5lib')
        salt = soup.find('input', id='pwdEncryptSalt')['value']
        execution = soup.find('input', id='execution')['value']
        # 密码加密
        salt_pwd = get_token(self.password, salt)

        form_login = {
            'username': self.username,
            'password': salt_pwd,
            '_eventId': 'submit',
            'cllt': 'userNameLogin',
            'execution': execution
        }
        rs = self.session.post(url=url_post, data=form_login, headers=headers, allow_redirects=False)

        if rs.status_code == 302:
            url_re = rs.headers['Location']
            rss = self.session.get(url=url_re)
            l1 = []
            for a in self.session.cookies:
                l1.append(a.value)
        #    print('校园卡余额所用Cookie', l1[0])

            return True

    def get_balance_simple(self):
        r = self.session.get(url=url_balance, headers=headers)
        return r.json()

    def get_balance_history_simple(self):
        r = self.session.get(url=url_balance2, headers=headers)
        return r.json()

    def get_balance_history_pro(self, sdata='2020-11-09', edate='2020-12-09', account='119192', page='1', rows='15'):
        r = self.session.get(url=url_balance_re1, headers=headers)
        soup = BeautifulSoup(r.text, 'html5lib')
        token = soup.find('input', id='ssoticketid')['value']
        form = {
            "errorcode": 1,
            "continueurl": '',
            "ssoticketid": token
        }
        r1 = self.session.post(url=url_balance_re2, headers=headers, data=form)
        l1 = []
        for s in self.session.cookies:
            l1.append(s)
        # print("一卡通流水所用cookie", l1[7])
        form_balance = {
            "sdate": sdata,
            "edate": edate,
            "account": account,
            "page": page,
            "rows": rows
        }
        r2 = self.session.post(url=url_balance_history, headers=headers, data=form_balance)
        return r2.json()

    def get_library_simple(self):
        r = self.session.get(url=url_library, headers=headers)
        return r.json()

    def get_library_token(self):
        r = self.session.get(url=url_library_re, headers=headers, allow_redirects=False)
        r2 = self.session.get(url=r.headers['Location'], headers=headers, allow_redirects=False)
        r3 = self.session.get(url=r2.headers['Location'], headers=headers, allow_redirects=False)
        r4 = self.session.get(url=r3.headers['Location'], headers=headers, allow_redirects=False)
        # 重定向出现问题，手动跳转获取token, 反正以后也得拆分。。。
        # print('图书馆所用的jwtOpacAuth为：', r4.headers['Location'][43:-12])
        return r4.headers['Location'][43:-12]

    # account为卡号， tranamt单位为分，也就是100为1元
    # 复用部分get_balance_history_pro, 应该用缓存来解决,但这只是个demo
    def get_balance_charge(self, tranamt='100'):
        # 获取Cookie
        r = self.session.get(url=url_balance_re1, headers=headers)
        soup = BeautifulSoup(r.text, 'html5lib')
        token = soup.find('input', id='ssoticketid')['value']
        form = {
            "errorcode": 1,
            "continueurl": '',
            "ssoticketid": token
        }
        r1 = self.session.post(url=url_balance_re2, headers=headers, data=form)
        l1 = []
        for s in self.session.cookies:
            l1.append(s)
        # 获取卡号
        r2 = self.session.get(url=url_balance, headers=headers)
        account = r2.json()['data']['ZH']

        # 以下为本次表单提交
        header = {
            "Referer": "http://ykt.cumt.edu.cn/Page/Page",
            "Cookie": 'hallticket='+l1[6].value
        }
        form_charge = {
            "account": account,
            "acctype": "23%23%23",
            "tranamt": tranamt,
            "qpwd": "",
            "paymethod": "2",
            "paytype": "%E4%BD%BF%E7%94%A8%E7%BB%91%E5%AE%9A%E7%9A%84%E9%BB%98%E8%AE%A4%E8%B4%A6%E5%8F%B7",
            "client_type": "web"
        }
        r3 = requests.post(url=url_balance_charge, headers=header, data=form_charge)
        return r3.text


# 以下不需要request.session会话保持
# 请不要频繁请求图书馆，http连接池会满，可以令verify为Flase，或connection 为 close
# 有时候，学校的光缆被挖断后，会出现这种情况(手动狗头)
class libIds:
    def __init__(self, jwt_token):
        self.token = jwt_token
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 FireFox / 29.0",
            "X-Requested-With": "XMLHttpRequest",
            "jwtOpacAuth": jwt_token,
            "Referer": "https://findcumt.libsp.com/",
            "Connection": "close"
        }

    def get_library_list(self, page='1', rows='20'):  # page 页吗 rows 每页行数
        form = {
            "page": page,
            "rows": rows
        }
        r = requests.post(url=url_library_Loan, headers=self.headers, json=form, verify=False)
        return r.json()

    def get_library_history_list(self, page='1', rows='20'):
        form = {
            "page": page,
            "rows": rows
        }
        r = requests.post(url=url_library_loan_history, headers=self.headers, json=form, verify=False)
        return r.json()

    def get_library_favorite(self, page='1', rows='10'):
        form = {
            "favoritesId": "",
            "page": page,
            "rows": rows,
            "searchField": "title",
            "searchFieldContent": ""
        }
        r = requests.post(url=url_library_favorite, headers=self.headers, json=form, verify=False)
        return r.json()


if __name__ == '__main__':
    # username为学号， password为密码
    a = newIds("username", "password")
    a.login()
    # 校园卡余额
    print(a.get_balance_simple())

    # 校园卡充值
    print(a.get_balance_charge())

    # 校园卡历史流水(按时间查)
    print(a.get_balance_history_pro())

    # 获取图书馆借阅信息(简约)
    print(a.get_library_simple())

    # 校园卡流水(按消费记录逆序)
    print(a.get_balance_simple())

    # 获取图书馆的jwt_token
    token = a.get_library_token()

    b = libIds(token)

    # 获取目前的图书借阅信息
    print(b.get_library_list())

    # 获取图书馆的历史借阅信息
    print(b.get_library_history_list())

    # 图书馆默认收藏信息
    print(b.get_library_favorite())

import requests
from urllib3 import encode_multipart_formdata
import logging
import json
import time
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)


# 登陆
def getAccessToken(UserNumber, UserPassword):
    # 获取 JSESSIONID
    accessTokenUrl = "https://www.szlib.org.cn/m/mylibrary/member.jsp"
    AccessTokenHeaders = {
        'Host': 'www.szlib.org.cn',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': '_pk_id.8.8720=40ea576fc0bd3629.1649649180.17.1650222176.1650215358.; _pk_ses.8.8720=*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-cn',
        'Referer': 'https://www.szlib.org.cn/m/login.html?formalurl=https%3A%2F%2Fwww.szlib.org.cn%2Fm%2Fmylibrary%2Fmember.jsp',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    session = requests.session()
    session.get(url=accessTokenUrl, headers=AccessTokenHeaders)
    JSESSIONID = session.cookies.get_dict()['JSESSIONID']
    print(JSESSIONID)

    # 密码登陆
    PasswordLoginPayload = {
        'username': UserNumber,
        'password': UserPassword,
        '_': str(round(time.time() * 1000))
    }
    PasswordLoginUrl = "https://www.szlib.org.cn/m/proxyBasic.jsp?readermanage/webReaderLogin?username=" + \
                       PasswordLoginPayload['username'] + "&password=" + PasswordLoginPayload['password'] + "&_=" + \
                       PasswordLoginPayload['_']
    PasswordLoginHeaders = {
        'Host': 'www.szlib.org.cn',
        'Accept-Encoding': 'gzip, deflate, br',
        'Cookie': 'JSESSIONID=' + JSESSIONID + '; _pk_id.7.8720=81c648a809391166.1650215672.1.1650215677.1650215672.; _pk_ses.7.8720=*;',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
        'Referer': 'https://www.szlib.org.cn/m/login.html?formalurl=https%3A%2F%2Fwww.szlib.org.cn%2Fm%2Fmylibrary%2Fmember.jsp',
        'Accept-Language': 'zh-cn',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = requests.get(url=PasswordLoginUrl, headers=PasswordLoginHeaders)
    print(response.text)

    # 获取 accessToken
    accessTokenUrl = "https://www.szlib.org.cn/m/mylibrary/member.jsp"
    AccessTokenHeaders = {
        'Host': 'www.szlib.org.cn',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'JSESSIONID=' + JSESSIONID + '; _pk_id.8.8720=40ea576fc0bd3629.1649649180.17.1650222176.1650215358.; _pk_ses.8.8720=*',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Mobile/15E148 Safari/604.1',
        'Accept-Language': 'zh-cn',
        'Referer': 'https://www.szlib.org.cn/m/login.html?formalurl=https%3A%2F%2Fwww.szlib.org.cn%2Fm%2Fmylibrary%2Fmember.jsp',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    session = requests.session()
    session.get(url=accessTokenUrl, headers=AccessTokenHeaders)
    # print(session.cookies.get_dict())
    accessToken = session.cookies.get_dict()['accessToken_szlib']
    return accessToken, JSESSIONID


# 查询座位
def whereIsmySeat(accessToken):
    url = "https://yun.szlib.org.cn/electroomapi/elecroom/ermonitor"
    params = {
        'servaddr':(None, 'STRead-4E,STRead-4FN'),
        'authkey':(None, 'f4aa3a4b002dee395a6b9a2b35706b01'),
        'lognum':(None, '6'),
        'timesup':(None, '10')
    }
    m = encode_multipart_formdata(params, boundary='----WebKitFormBoundarybj0pV8WEPaUk7HBk')
    headers = {
      'Host': 'yun.szlib.org.cn',
      'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundarybj0pV8WEPaUk7HBk',
      'Origin': 'https://yun.szlib.org.cn',
      'Accept-Encoding': 'gzip, deflate, br',
      'Cookie': 'DISTANCE=42; accessToken_szlib='+ accessToken,
      'Connection': 'keep-alive',
      'Accept': 'application/json, text/plain, */*',
      'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x18001429) NetType/WIFI Language/zh_CN',
      'Referer': 'https://yun.szlib.org.cn/electroom/',
      'Content-Length': '475',
      'Accept-Language': 'zh-cn'
    }

    response = requests.request("POST", url, headers=headers, data=m[0])
    roomJson = json.loads(response.text)
    true = 1
    false = 0
    # 创客空间
    U1 = 0
    C1 = 0
    S1 = 0
    C1list = []
    # 选择的序号
    R1Select = 0
    for i in range(0, 20):
        # print(roomJson['room'][1]['seat'][i]['status'])
        cacheStatus = roomJson['room'][1]['seat'][i]['status']
        if cacheStatus == 'U':
            U1 = U1 + 1
        elif cacheStatus == 'C':
            C1 = C1 + 1
            C1list.append(i)
        else:
            S1 = S1 + 1
    logging.info('创客空间')
    logging.info('正在使用座位：' + str(U1))
    logging.info('无法使用座位：' + str(S1))
    logging.info('可使用座位：' + str(C1))
    print(C1list)
    if C1 > 0:
        # round 四舍五入
        R1Select = str(C1list[round(len(C1list) / 2)]).rjust(3, '0')
        print(R1Select)
        return 'STRead-4FN', R1Select

    # 网络信息空间
    U0 = 0
    C0 = 0
    S0 = 0
    C0list = []
    R0Select = 0
    for i in range(0, 118):
        # print(roomJson['room'][1]['seat'][i]['status'])
        cacheStatus = roomJson['room'][0]['seat'][i]['status']
        if cacheStatus == 'U':
            U0 = U0 + 1
        elif cacheStatus == 'C':
            C0 = C0 + 1
            C0list.append(i)
        else:
            S0 = S0 + 1
    logging.info('网络信息空间')
    logging.info('正在使用座位：' + str(U0))
    logging.info('无法使用座位：' + str(S0))
    logging.info('可使用座位：' + str(C0))
    print(C0list)
    if C0 > 0:
        # round 四舍五入
        R0Select = str(C0list[round(len(C0list) / 2)]).rjust(3, '0')
        print(R0Select)
        return 'STRead-4E', R0Select


# 申请座位
def applySeat(servaddr, seatid, access_token):
    applySeatUrl = 'https://yun.szlib.org.cn/electroom4mobileapi/elecroom4mobile/seatdistribute'
    # ?servaddr=STRead-4FN&seatid=019&access_token=b602873c-83eb-4810-a3ae-83d92b6ec969
    headers = {
        'Host': 'yun.szlib.org.cn',
        'Accept': 'application/json, text/plain, */*',
        'Connection': 'keep-alive',
        'Cookie': 'usermsg=%7B%22cardno%22%3A%220440005181480%22%2C%22readerid%22%3A%224925352%22%2C%22gender%22%3A%22%E7%94%B7%22%2C%22name%22%3A%22%E9%AB%98%E5%AE%87%E6%88%88%22%2C%22address%22%3A%22%22%2C%22phone%22%3A%2218979486699%22%2C%22password%22%3A%2203f724b6323bdb83fa88fe6ce6c047b0%22%2C%22webpsd%22%3A%22e410037f8406406e82135ae290e3b1bb%22%2C%22status%22%3A%22%E6%9C%89%E6%95%88%22%2C%22birth%22%3A20010109%2C%22cardtype%22%3A%22%E9%B9%8F%E5%9F%8E%E5%8A%B1%E8%AF%BB%E8%AF%81%22%2C%22entertimes%22%3A0%2C%22totaltimes%22%3A0%7D; DISTANCE=96.4; accessToken_szlib=b602873c-83eb-4810-a3ae-83d92b6ec969',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_8_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.20(0x18001429) NetType/WIFI Language/zh_CN',
        'Accept-Language': 'zh-cn',
        'Referer': 'https://yun.szlib.org.cn/electroom/',
        'Accept-Encoding': 'gzip, deflate, br'
    }
    params = {
        'servaddr': servaddr,
        'seatid': seatid,
        'access_token': access_token
    }
    result = requests.get(url = applySeatUrl, params = params, headers=headers).text
    return result


if __name__ == '__main__':
    UserNumber = '0440005181480'
    UserPassword = 'k7WpNCSqENTej7T'
    accessToken, JSESSIONID = getAccessToken(UserNumber, UserPassword)
    servaddr, seatid = whereIsmySeat(accessToken)
    result = applySeat(servaddr, seatid, accessToken)
    print(result)
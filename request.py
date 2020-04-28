import json
import math
import random
import re
import sys
import time
import demjson
import requests
from urllib import request
from http import cookiejar
# #跳过SSL验证证书
# import ssl
# #设置忽略SSL验证
# ssl._create_default_https_context = ssl._create_unverified_context
def getUserInfo(cookiestr):
    print("cookiestr",cookiestr)
    # 'uin=o1071343549; skey=@Gry3JTMTU;' skey=@Gry3JTMTU;
    #qq模拟登陆后，可以获取到cookie，cookie带到请求头里
    headers={
        'authority': 'comm.aci.game.qq.com',
        'method': 'GET',
        'scheme': 'https',
        'cookie': cookiestr,
        'referer': 'https://act.qzone.qq.com/vip/roleSelector',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080'
        }
    t = time.time()    
    rand = + t + math.floor(random.random() * 20000);    
    res=requests.get("https://comm.aci.game.qq.com/main?game=dnf&area=65&callback="+str(rand)+"&sCloudApiName=ams.gameattr.role&iAmsActivityId=https%3A%2F%2Fact.qzone.qq.com%2Fvip%2FroleSelector",headers=headers)
    print(res.text)
    #cont=res.text.decode('utf-8')
    rex=re.compile(r'\{[^\}]+\}')
    # print("cont",cont)
    content=rex.findall(res.text)[0]
    # print("content",content)
    # con=json.loads(content)
    con = demjson.decode(content) #json 解析成字典
    # print("con",content)
    print ('data    ',con['data'],'checkparam    ',con['checkparam'],'md5str    ',con['md5str'])
    #qq空间 g_tk 算法 r算法 = Math.random()

    # str = cookie.get("p_skey") || cookie.get("skey")        
    # getTokenByKey: function(str) {
    #             var t = 5381
    #               , i = e;
    #             for (var n = 0, r = i.length; n < r; ++n) {
    #                 t += (t << 5) + i.charAt(n).charCodeAt()
    #             }
    #             return t & 2147483647
    #         },
#getUserInfo("cookiestr")
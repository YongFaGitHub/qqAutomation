import json
import math
import random
import re
import sys
import time
import demjson
import requests

#qq模拟登陆后，可以获取到cookie，cookie带到请求头里
headers={
    "authority":"comm.aci.game.qq.com",
    "method":"GET",
    "path":"/main?game=dnf&area=65&callback=158788728990215532&sCloudApiName=ams.gameattr.role&iAmsActivityId=https%3A%2F%2Fact.qzone.qq.com%2Fvip%2FroleSelector&query_role_result_158788728990215532=jQuery1102014141925064958172_1587887169187&_=1587887169191",
    "scheme":"https",
    "accept":"*/*",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"zh-CN,zh;q=0.9",
    "cookie":"pgv_pvi=1546252288; pgv_si=s5056442368; _qpsvr_localtk=0.5587039485869829; RK=gQbhOKN2dC; ptcz=e146868a984107f0d4d8cbeeb65135701699fdc32a003a5f9731409b1801db15; uin=o0348237511; skey=@Lf47AeNVM; pvid=8715306440; eas_sid=q1Q5V8F7g8a8r4E1y8k0U02396; IED_LOG_INFO2=userUin%3D348237511%26nickName%3D%25252AD0%26userLoginTime%3D1587884194",
    "dnt":"1",
    "referer":"https://act.qzone.qq.com/vip/2019/xcardv2?_wv=4&zz=9&from=arksend",
    "sec-fetch-dest":"script",
    "sec-fetch-mode":"no-cors",
    "sec-fetch-site":"same-site",
    "user-agent":"Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080"
    }
t = time.time()    
rand = + t + math.floor(random.random() * 20000);    
res=requests.get("https://comm.aci.game.qq.com/main?game=dnf&area=65&callback="+str(rand)+"&sCloudApiName=ams.gameattr.role&iAmsActivityId=https%3A%2F%2Fact.qzone.qq.com%2Fvip%2FroleSelector&query_role_result_158788728990215532=jQuery1102014141925064958172_1587887169187&_=1587887169191",headers=headers)
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

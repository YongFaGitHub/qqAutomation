import json
import math
import os
import random
import re
import sys
import time
from http import cookiejar
from urllib import request

import demjson
import requests

import getConfig  # 引用获取配置文件模块

confname = os.getcwd()+"\\conf\\通用配置.ini"
#跳过SSL验证证书
import ssl
#设置忽略SSL验证
ssl._create_default_https_context = ssl._create_unverified_context
def getTokenByKey(skey):
    #qq空间 g_tk 算法 r算法 = Math.random()
    hash = 5381;
    s = skey
    for i in s:
            hash += (hash << 5) + ord(i)
    return hash & 2147483647
#获取用户信息    
def getUserInfo(cookiestr,areas):
    
    #qq模拟登陆后，可以获取到cookie，cookie带到请求头里
    headers={
        'cookie': cookiestr,
        'referer': 'https://act.qzone.qq.com/vip/roleSelector',
        }
    t = time.time()    
    rand = + t + math.floor(random.random() * 20000);    
    res=requests.get("https://comm.aci.game.qq.com/main?game=dnf&area="+areas+"&callback="+str(rand)+"&sCloudApiName=ams.gameattr.role",headers=headers)
    #print("getUserInfo",res.text)
    #cont=res.text.decode('utf-8')
    rex=re.compile(r'\{[^\}]+\}')
    # print("cont",cont)
    content=rex.findall(res.text)[0]
    # print("content",content)
    # con=json.loads(content)
    con = demjson.decode(content) #json 解析成字典
    # print("con",content)
    print ('角色列表 ',con['data'],'checkparam    ',con['checkparam'],'md5str    ',con['md5str'])
    listData = []
    for i in con['data'].split():
        listData.append(i)
    print("listData",listData[0].split("|")[1])
    return listData[0].split("|")[1]
def getLookVideo(cookiestr,skey,user):
    print("getLookVideo",cookiestr,skey,user)
    headers={
        'cookie': cookiestr,
        }
    data = "actid=3316&ruleid=19874&format=json&uin="+user+""
    res=requests.post("https://activity.qzone.qq.com/fcg-bin/fcg_qzact_present?g_tk=%d"%getTokenByKey(skey)+"&r=0.14693180627876368",headers=headers,data=data)
    print("看视频获取资格",res.text)
    con = demjson.decode(res.text) #json 解析成字典
    print("con",str(con))
    #print ('data    ',con['data'],'checkparam    ',con['checkparam'],'md5str    ',con['md5str'])
    #         },
def getLotteryDraw(cookiestr,skey,user):
    print("getLookVideo",cookiestr,skey,user)
    headers={
        'cookie': cookiestr,
        }
    data = "actid=3316&ruleid=19874&format=json&uin="+user+""
    res=requests.post("https://activity.qzone.qq.com/fcg-bin/fcg_qzact_lottery?g_tk=%d"%getTokenByKey(skey)+"&r=0.14693180627876368",headers=headers,data=data)
    print("抽奖资格",res.text)
    con = demjson.decode(res.text) #json 解析成字典
    print("con",str(con))
def getEveryDayLogin(cookiestr,skey,user,area,roleid):
    print("getLookVideo",cookiestr,skey,user,area)
    headers={
        'cookie': cookiestr,
        }
    data = "area="+area+"&partition="+area+"&roleid="+roleid+"&platform=pc&query=0&act_name=act_dnf_ark6&format=json&uin="+user+""
    res=requests.post("https://activity.qzone.qq.com/fcg-bin/v2/fcg_yvip_game_pull_flow?g_tk=%d"%getTokenByKey(skey)+"&r=0.14693180627876368",headers=headers,data=data)
    print("登录dnf获取资格",res.text)
    con = demjson.decode(res.text) #json 解析成字典
    print("con",str(con))
getUserInfo("uin=o1071343549; skey=@a3vvob2kl; p_skey=WXUz262MY3roIvqWzP*LfPm3NYqXpu1g-O6gPCpMMqw_;","40")
#getLookVideo('uin=o1071343549; skey=@a3vvob2kl; p_skey=WXUz262MY3roIvqWzP*LfPm3NYqXpu1g-O6gPCpMMqw_;','WXUz262MY3roIvqWzP*LfPm3NYqXpu1g-O6gPCpMMqw_','1071343549')
#getEveryDayLogin('uin=o1027187669; skey=@fq8xNvT4y; p_skey=FyHZIDkukDxjkYUBCH35LgYzETsZqKGJJ5Z-O3PZZik_;','FyHZIDkukDxjkYUBCH35LgYzETsZqKGJJ5Z-O3PZZik_','1027187669','40')
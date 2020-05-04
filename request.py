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
import logging
from logging import handlers

class Logger(object):
    level_relations = {
        'debug':logging.DEBUG,
        'info':logging.INFO,
        'warning':logging.WARNING,
        'error':logging.ERROR,
        'crit':logging.CRITICAL
    }#日志级别关系映射

    def __init__(self,filename,level='info',when='D',backCount=3,fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt)#设置日志格式
        self.logger.setLevel(self.level_relations.get(level))#设置日志级别
        sh = logging.StreamHandler()#往屏幕上输出
        sh.setFormatter(format_str) #设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename,when=when,backupCount=backCount,encoding='utf-8')#往文件里写入#指定间隔时间自动生成文件的处理器
        #实例化TimedRotatingFileHandler
        #interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)#设置文件里写入的格式
        self.logger.addHandler(sh) #把对象加到logger里
        self.logger.addHandler(th)
    
log = Logger('日志.log',level='debug')

def getTokenByKey(skey):
    #qq空间 g_tk 算法 r算法 = Math.random()
    hash = 5381;
    s = skey
    for i in s:
            hash += (hash << 5) + ord(i)
    return hash & 2147483647
#获取用户信息    
def getUserInfo(cookiestr,areas):
   
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
    #print ('角色列表 ',con['data'],'checkparam    ',con['checkparam'],'md5str    ',con['md5str'])
    listData = []
    for i in con['data'].split():
        listData.append(i)
    print("领奖励角色ID",listData[0].split("|")[1])
    return listData[0].split("|")[1]
#看视频加抽奖次数
def getLookVideo(cookiestr,skey,user):
    #print("getLookVideo",cookiestr,skey,user)
    headers={
        'cookie': cookiestr,
        }
    data = "actid=3316&format=json&uin="+user+"&ruleid=19865"
    res=requests.post("https://activity.qzone.qq.com/fcg-bin/fcg_qzact_present?g_tk=%d"%getTokenByKey(skey)+"",headers=headers,data=data)
    print("看视频",res.text)
    con = demjson.decode(res.text) #json 解析成字典
    #print("con",str(con))
    #print ('data    ',con['data'],'checkparam    ',con['checkparam'],'md5str    ',con['md5str'])
    #         },
#抽奖
def getLotteryDraw(cookiestr,skey,user):
    #print("getLookVideo",cookiestr,skey,user)
    headers={
        'cookie': cookiestr,
        }
    data = "actid=3316&ruleid=19874&format=json&uin="+user+""
    res=requests.post("https://activity.qzone.qq.com/fcg-bin/fcg_qzact_lottery?g_tk=%d"%getTokenByKey(skey)+"&r=0.14693180627876368",headers=headers,data=data)
    print("抽奖",res.text)
    con = demjson.decode(res.text) #json 解析成字典
    #print("con",str(con),"con['code']",int(con['code']))
    return int(con['code'])
#每日登录dnf加抽奖次数
def getEveryDayLogin(cookiestr,skey,user,area,roleid):
    #print("getLookVideo",cookiestr,skey,user,area)
    headers={
        'cookie': cookiestr,
        }
    data = "area="+area+"&partition="+area+"&roleid="+roleid+"&platform=pc&query=0&act_name=act_dnf_ark6&format=json&uin="+user+""
    res=requests.post("https://activity.qzone.qq.com/fcg-bin/v2/fcg_yvip_game_pull_flow?g_tk=%d"%getTokenByKey(skey)+"&r=0.14693180627876368",headers=headers,data=data)
    print("登录dnf获取资格",res.text)
    con = demjson.decode(res.text) #json 解析成字典
    #print("con",str(con))
def getIP(url):
    res = requests.get(url)
    con=''
    if res.status_code == 200:
        con = demjson.decode(res.text) #json 解析成字典
        print(con)
    else:
        print("获取数据失败")
    return con
    #print(con['data'][num]['IP'].split(":")[1])
def checkIP():
    res = requests.get('http://httpbin.org/ip')
    #con = demjson.decode(res.text) #json 解析成字典
    print(res.text)

# def getProxy(data):

    # #代理服务器
    # proxyHost = data.split(":")[[0]
    # proxyPort = data.split(":")[1]

    # proxyMeta = "https://%(host)s:%(port)s" % {
    #     "host" : proxyHost,
    #     "port" : proxyPort,
    # }

    # #pip install -U requests[socks]  socks5代理
    # # proxyMeta = "socks5://%(host)s:%(port)s" % {
    # #     "host" : proxyHost,
    # #     "port" : proxyPort,
    # # }

    # proxies = {
    #     "https"  : proxyMeta,
    # }
    # return proxies

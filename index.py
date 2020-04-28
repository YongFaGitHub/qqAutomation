# encoding=utf8
# pip install urllib2 -i http://pypi.douban.com/simple --trusted-host pypi.douban.com 安装插件命令
import json
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import getConfig  # 引用获取配置文件模块
import request  # 引入请求接口模块

filename = 'user/账号.txt'
confname = 'conf/通用配置.ini'

options = webdriver.ChromeOptions()
options.add_experimental_option('w3c', False)
options.add_argument('user-agent=' + getConfig.ReadConfig(confname,"用户代理",'ua'))
driver = webdriver.Chrome(options=options)
#滑块算法
def get_track(distance):
    track = []
    current = 0
    mid = distance * 3 / 4
    t = 0.2
    v = 0
    while current < distance:
        if current < mid:
            a = 2
        else:
            a = -3
        v0 = v
        v = v0 + a * t
        move = v0 * t + 1 / 2 * a * t * t
        current += move
        track.append(round(move))
    return track

#主线程，qqweb手机端登录代码
def main(user,password,area):
    driver.delete_all_cookies()
    # print("路径！！！",str(getConfig.ReadConfig(confname,"链接路径",'url')))
    
    driver.get('https://ui.ptlogin2.qq.com/cgi-bin/login?style=9&appid=549000929&pt_ttype=1&daid=5&pt_no_auth=1&pt_hide_ad=1&s_url=https%3A%2F%2Fact.qzone.qq.com%2Fvip%2F2019%2Fxcardv2%3F_wv%3D4%26zz%3D9%26from%3Darksend&pt_no_onekey=1')

    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
   
    sleep(1)
    # 输入用户名和密码
    driver.find_element_by_id('u').clear()
    driver.find_element_by_id('u').send_keys(user)
    driver.find_element_by_id('p').clear()
    driver.find_element_by_id('p').send_keys(password)
    sleep(1)
    # 触摸touch事件，登录
    go = driver.find_element_by_id('go')
    Action = TouchActions(driver)
    Action.tap(go).perform()
   
    sleep(5)

    # 切换iframe
    try:
        iframe = driver.find_element_by_xpath('//*[@id="tcaptcha_iframe"]')
       
    except Exception as e:
        print('get iframe failed: ', e)
    sleep(2)  # 等待资源加载
    driver.switch_to.frame(iframe)
    button = driver.find_element_by_id('tcaptcha_drag_button')  # 寻找滑块
    sleep(1)
    # 开始拖动 perform()用来执行ActionChains中存储的行为
    flag = 0
    distance = 195
    offset = 5
    times = 0
    while 1:
        action = ActionChains(driver)
        action.click_and_hold(button).perform()
        action.reset_actions()  # 清除之前的action
        print(distance)
        track = get_track(distance)
        for i in track:
            action.move_by_offset(xoffset=i, yoffset=0).perform()
            action.reset_actions()
        sleep(0.5)
        action.release().perform()
        sleep(3)

        # 判断某元素是否被加载到DOM树里，并不代表该元素一定可见
        try:
            alert = driver.find_element_by_id('tcaptcha_note').text
        except Exception as e:
            print('get alert error: %s' % e)
            alert = ''
        if alert:
            print('滑块位移需要调整: %s' % alert)
            distance -= offset
            times += 1
            sleep(5)
            if times > 9:
                flag = 1
        else:
            print('滑块验证通过')
            flag = 1
            driver.switch_to.parent_frame()  # 验证成功后跳回最外层页面
            break
    sleep(2)
    # 判断成功登录到活动页还是失败并且把失败原因打印出来
    success = 0
    try:
        error_message = driver.find_element_by_id('error_message').text
    except Exception as e:
        print('get error_message error: %s' % e)
        error_message = ''
    if error_message:
        print('登陆失败原因: %s' % error_message)
        sleep(1)
        success = 1
    else:
        print('成功登陆到活动页')
        success = 0
        
    if success == 1:
        return 
    else:
        pass    
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        skey = driver.get_cookie("skey")
        uin = driver.get_cookie("uin")
        print("cookiestr","uin="+str(uin)+"; "+"skey="+str(uin)+";")
        cookiestr="uin="+str(uin)+"; "+"skey="+str(skey)+";"
        
        with open('cookie.text','w',encoding='utf-8') as f:
            f.write(user+'----'+cookiestr+'\r\n')
        request.getUserInfo(cookiestr)
def user():
    user=getConfig.getText(filename)
    # print("user~~",user)
    for i in user:
        print("i~~",i)
        main(i[0],i[1],i[2])
   # print("user~~",user)
    
if __name__ == '__main__':
   # main()
   user()

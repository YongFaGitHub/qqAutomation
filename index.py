# encoding=utf8
# pip install pyinstaller -i http://pypi.douban.com/simple --trusted-host pypi.douban.com 安装插件命令
# pyinstaller -F -i D:\qqAutomation_py\favicon.ico  D:\qqAutomation_py\index.py 打包编译成exe 文件
import json
import logging
import os
import time
from logging import handlers
from time import sleep
import demjson
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import getConfig  # 引用获取配置文件模块
import request  # 引入请求接口模块

filename = os.getcwd()+"\\user\\账号.txt"
confname = os.getcwd()+"\\conf\\通用配置.ini"
district = os.getcwd()+"\\conf\\大区配置.ini"

options = webdriver.ChromeOptions()
options.add_experimental_option('w3c', False)
options.add_argument(
    'user-agent=' + getConfig.ReadConfig(confname, "用户代理", 'ua'))
driver = webdriver.Chrome(options=options)
# 滑块算法


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
# 给json内的键加上双引号


def jsonPropt(astr):
    return astr.replace(' ', '').replace('\n', '').replace('\r', '')\
               .replace("'", '"').replace('{', '{"').replace(':', '":')\
               .replace('],', '],"').replace('",', '","')
# 主线程，qqweb手机端登录代码


def main(user, password, area):
    driver.delete_all_cookies()
    areas = getConfig.ReadConfig(district, "大区配置", area)
    if areas:
        print("获取大区成功:", areas)
    else:
        pass
        print("获取大区失败:", areas)
        return
    # print("路径！！！",str(getConfig.ReadConfig(confname,"链接路径",'url')))

    driver.get('https://ui.ptlogin2.qq.com/cgi-bin/login?style=9&appid=549000929&pt_ttype=1&daid=5&pt_no_auth=1&pt_hide_ad=1&s_url=https%3A%2F%2Fact.qzone.qq.com%2Fvip%2F2019%2Fxcardv2%3F_wv%3D4%26zz%3D9%26from%3Darksend&pt_no_onekey=1')

    print(time.strftime('%Y-%m-%d-%H:%M:%S', time.localtime(time.time())))

    sleep(1)

    # 输入用户名和密码
    driver.find_element_by_id('u').clear()
    driver.find_element_by_id('u').send_keys(user)
    sleep(1)
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
    try:
        driver.switch_to.frame(iframe)
    except Exception as na:
        screeshot = os.getcwd()+"\\screenshot\\"
        if not screeshot:
            os.makedir(screeshot)
        else:
            print("当前截图路径", screeshot, "保存图片的路径", screeshot +time.strftime('%Y-%m-%d_%H_%M_%S_', time.localtime(time.time()))+'.png')
            driver.get_screenshot_as_file(screeshot+time.strftime('%Y-%m-%d_%H_%M_%S_', time.localtime(time.time()))+'_'+user+'.png')
        return
    
    button = driver.find_element_by_id('tcaptcha_drag_button')  # 寻找滑块
    sleep(1)
    # 开始拖动 perform()用来执行ActionChains中存储的行为
    flag = 0
    distance = 197
    offset = 5
    times = 1
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
            alert=''
            message=''
            alert = driver.find_element_by_id('tcaptcha_note').get_attribute('textContent')
            message = driver.find_element_by_id('guideText').text
            print(alert, message)
        except Exception as e:
            
            if alert:
                pass
            else:
                alert = ''
            if message:
                pass
            else:
                message = ''
        if alert and message:
            print('滑块位移需要调整: %s' % alert)
            distance -= offset
            times += 1
            sleep(5)
            if times == 4:
                distance = 197
            if times > 9:
                flag = 1
                break
        else:
            print('滑块验证通过')
            flag = 1
            driver.switch_to.parent_frame()  # 验证成功后跳回最外层页面
            break
    sleep(4)
    # 判断成功登录到活动页还是失败并且把失败原因打印出来
    success = 0
    try:
        error_message=''
        error_message_open=''
        error_message = driver.find_element_by_id('error_message').get_attribute('textContent')
        error_message_open = driver.find_element_by_class_name('qui-dialog-content').text
    except Exception as e:
        
        if error_message:
            pass
        else:
            error_message = ''
        if error_message_open:
            pass
        else:
            error_message_open = ''
    if error_message or error_message_open:
        print('登陆失败原因: %s' % error_message, error_message_open)
        sleep(1)
        getConfig.setText(filename, user, area,'登陆失败原因:'+error_message+error_message_open)
        success = 1
    else:
        print('成功登陆到活动页')
        sleep(2)
        success = 0
        js = """
        var hello = window.syncData;
        return hello;
        """
        con = driver.execute_script(js)

        if con:
            for key, value in con["actCount"].items():
                for key, value in value.items():
                    for key, value in value.items():
                        print(" 名称：", value[0]['name'], "剩余：", value[0]['add'])
        else:
            print("活动页不存在", con)
            try:
                screeshot = os.getcwd()+"\\screenshot\\"
                if not screeshot:
                    os.makedir(screeshot)
                else:
                    print("当前截图路径", screeshot, "保存图片的路径", screeshot+time.strftime('%Y-%m-%d_%H_%M_%S_', time.localtime(time.time()))+'.png')
                    driver.get_screenshot_as_file(screeshot+time.strftime('%Y-%m-%d_%H_%M_%S_', time.localtime(time.time()))+'_'+user+'.png')
            except NameError as na:
                logger.info("截图失败:%s" % na)
                getConfig.setText(filename, user, area, '未到达活动页，失败原因未知')
            return
    if success == 1:
        return
    else:
        pass
        # 获取cookie参数，拼装参数写入文件并且带入到接口中请求
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        skey = driver.get_cookie("skey")
        uin = driver.get_cookie("uin")
        p_skey = driver.get_cookie("p_skey")
        # print("cookiestr","uin="+str(uin)+"; "+"skey="+str(skey)+";")
        cookiestr = "uin="+str(uin['value'])+"; "+"skey=" + \
            str(skey['value'])+"; "+"p_skey="+str(p_skey['value'])+";"
        print("cookiestr", cookiestr)
        with open('cookie.text', 'a+', encoding='utf-8') as f:
            f.write(user+'----'+cookiestr+'\r\n')
        # 获取用户角当前大区角色信息
        roleid = request.getUserInfo(cookiestr, areas)
        print("roleid", roleid)
        key = str(skey['value'])
        if p_skey:
            print("key==p_skey")
            key = str(p_skey['value'])
        # 看视频
        request.getLookVideo(cookiestr, str(key), user)
        # 每日登录
        request.getEveryDayLogin(cookiestr, str(key), user, areas, roleid)
        # 抽奖
        count = 0
        while count == 0:
            data = request.getLotteryDraw(cookiestr, str(key), user)
            if data < 0:
                count = count+1
            else:
                request.getLotteryDraw(cookiestr, str(key), user)
                print("继续抽奖")

        print("完成抽奖")
        getConfig.setText(filename, user, area, '完成抽奖')


def user():
    user = getConfig.getText(filename)
    # print("user~~",user)
    for i in user:
        if len(i) == 4:
            print("跳过当前账号，原因:", i[3])
        else:
            print("账号", str(i[0]), "大区", str(i[2]))
            main(i[0], i[1], i[2])
   # print("user~~",user)


if __name__ == '__main__':

    user()

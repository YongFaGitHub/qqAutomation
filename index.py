# encoding=utf8
# pip install demjson -i http://pypi.douban.com/simple --trusted-host pypi.douban.com 安装插件命令
import time
from time import sleep

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.touch_actions import TouchActions
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

url = 'https://ui.ptlogin2.qq.com/cgi-bin/login?style=9&appid=549000929&pt_ttype=1&daid=5&pt_no_auth=1&pt_hide_ad=1&s_url=https%3A%2F%2Fact.qzone.qq.com%2Fvip%2F2019%2Fxcardv2%3F_wv%3D4%26zz%3D9%26from%3Darksend&pt_no_onekey=1'
ua = 'Mozilla/5.0 (Linux; Android 6.0; PRO 6 Build/MRA58K; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/53.0.2785.49 Mobile MQQBrowser/6.2 TBS/043221 Safari/537.36 V1_AND_SQ_7.0.0_676_YYB_D QQ/7.0.0.3135 NetType/WIFI WebP/0.3.0 Pixel/1080'
options = webdriver.ChromeOptions()
options.add_experimental_option('w3c', False)
options.add_argument('user-agent=' + ua)
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

#主线程
def main(user,password,area):
    
    driver.get(url)
    # 检测id为"switcher_plogin"的元素是否加在DOM树中，如果出现了才能正常向下执行
    # element = WebDriverWait(driver, 5, 0.5).until(
    # 	EC.presence_of_element_located((By.ID, "go"))
    # )
    # element.click()
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

    sleep(1)
    # 输入用户名和密码
    driver.find_element_by_id('u').clear()
    driver.find_element_by_id('u').send_keys(user)
    driver.find_element_by_id('p').clear()
    driver.find_element_by_id('p').send_keys(password)
    sleep(1)
    # 点击登录
    go = driver.find_element_by_id('go')
    Action = TouchActions(driver)
    Action.tap(go).perform()
    # driver.find_element_by_id('go').click()

    sleep(4)

    # 切换iframe
    try:
        iframe = driver.find_element_by_xpath('//*[@id="tcaptcha_iframe"]')
        # iframe = driver.find_element_by_xpath('//iframe')
    except Exception as e:
        print('get iframe failed: ', e)
    sleep(2)  # 等待资源加载
    driver.switch_to.frame(iframe)

    # button = driver.find_element_by_id('tcaptcha_drag_button')
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
        else:
            print('滑块验证通过')
            flag = 1
            driver.switch_to.parent_frame()  # 验证成功后跳回最外层页面
            break

    sleep(2)
    # driver.quit()
    print("finish~~")
    print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    return flag
def user():
    data=[]
    filename = 'user/账号.txt' # txt文件和当前脚本在同一目录下，所以不用写具体路径
    pos = []
    Efield = []
    with open(filename,encoding='UTF-8') as file_to_read:
        while True:
            lines = file_to_read.readline() # 整行读取数据
            if not lines:
                break
            pass
            listData = []
            for i in lines.split():
                listData.append(i)
            pass
            print("账号信息~~user",listData)
            main(listData[0],listData[1],listData[2])
    pass
    return data
if __name__ == '__main__':
   # main()

   user()

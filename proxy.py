Python http/sock5:

#coding=utf-8
import requests

#请求地址
targetUrl = "http://baidu.com"

#代理服务器
proxyHost = "ip"
proxyPort = "port"

proxyMeta = "http://%(host)s:%(port)s" % {
    "host" : proxyHost,
    "port" : proxyPort,
}

#pip install -U requests[socks]  socks5代理
# proxyMeta = "socks5://%(host)s:%(port)s" % {
#     "host" : proxyHost,
#     "port" : proxyPort,
# }

proxies = {
    "http"  : proxyMeta,
}

resp = requests.get(targetUrl, proxies=proxies)
print (resp.status_code)
print (resp.text)
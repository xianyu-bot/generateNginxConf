import re
import os
from nginxConf_template import *

''' 
    本程序用来生成公司的nginx配置文件，目前功能仅实现了根据url生成upstream 和location块。
'''

def getUrl():
    url_list = []
    try:
        f = open("url.txt")
        while True:
            url = f.readline()
            url.strip()
            if not url:
                break
            url_list.append(url)
        f.close()

    except print("Can not open file"):
        exit()
    return url_list


def praseUrl(url):
    socket_list = []
    dir_name_list = []
    upstream_dict = {}

    for url in url:
        url = url.replace('\n', '')
        socket = re.search(
            r'((\d){1,3}\.){3}(\d){1,3}\:(\d+)', url).group(0)  # 获取ip和端口
        dir_name = (url[7:].split("/", 2))[1]  # 获取dirname
        if dir_name in upstream_dict:
            upstream_dict[dir_name].append(socket)
        else:
            upstream_dict[dir_name] = []
            upstream_dict[dir_name].append(socket)

    return upstream_dict


def generateUpstream(t):
    upstream_str = "upstream "
    server_str = "server "
    upstream_str_list = []
    r_upstream = "\n"

    for dirname, socket_list in t.items():
        if len(socket_list) == 1:
            temp = upstream_str + dirname + \
                '{' + '\n' + server_str + socket_list[0] + ';' + '}' + '\n'
            r_upstream = r_upstream + temp

        else:
            for i in socket_list:
                server_str = "server " + i + ';\n' + server_str
            server_str = server_str[0:-8]
            temp = upstream_str + dirname + \
                '{' + '\n' + server_str + '}' + '\n'
            r_upstream = r_upstream + temp

    return r_upstream


def generateLocation(t):
    location_str_head = "location "
    location_str_proxy = "proxy_pass   http://"
    r_location_str = ""

    for dirname in t:
        r_location_str = '      ' + location_str_head + dirname + '{'\
            + '\n' + '      ' + location_str_proxy + dirname + ';' + '\n' + '       ' + \
            '}' + '\n' + '      ' + r_location_str
    return r_location_str


def jointNginxConf(str_upstream, str_location, str_nginx_conf_head, str_nginx_conf_content, str_nginx_conf_tail):
    str_nginx_conf = str_nginx_conf_head + str_upstream + \
        str_nginx_conf_content + str_location + str_nginx_conf_tail
    return str_nginx_conf


def writeNginxConf(str_nginx_conf):
    file_write = open("nginx.conf", mode="w")
    file_write.write(str_nginx_conf)
    file_write.close()


def formatNginxConf(str_nginx_conf):
    pass


url = getUrl()

# url = ["http://192.168.104.213:8084/jcxmjd",
#        "http://192.168.104.239:8080/jclhys",
#        "http://192.168.104.238:8080/jclhys",
#        "http://192.168.104.233:8080/jclhys"]
t = praseUrl(url)

str_upstream = generateUpstream(t)
str_location = generateLocation(t)
str_nginx_conf = jointNginxConf(
    str_upstream, str_location, str_nginx_conf_head, str_nginx_conf_content, str_nginx_conf_tail)
writeNginxConf(str_nginx_conf)

print(str_nginx_conf)

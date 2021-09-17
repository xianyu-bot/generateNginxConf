import re
import os
import sys
from nginxConf_template import *
import nginxfmt

''' 
    本程序用来生成公司的nginx配置文件，目前功能仅实现了根据url生成upstream 和location块。
    版本：v0.1
    作者：咸鱼-bot
'''
# 从url.txt文件中获取url的字符串 url-->url_list


def getUrl() -> list:
    ''' 从文件中获取url的列表 '''
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
        sys.exit()
    return url_list


def praseUrl(url: list) -> dict:
    ''' 遍历url，生成dirname和socket字典 '''
    socket_list = []
    dir_name_list = []
    upstream_dict = {}
    for url in url:
        url = url.replace('\n', '')
        socket = re.search(r'((\d){1,3}\.){3}(\d){1,3}\:(\d+)', url).group(0)  # 获取ip和端口
        dir_name = url.strip().replace('http://', '').split('/', 1)[1]  # 获取dirname
        if dir_name in upstream_dict:
            upstream_dict[dir_name].append(socket)
        else:
            upstream_dict[dir_name] = []
            upstream_dict[dir_name].append(socket)

    return upstream_dict


def generateUpstream(t: dict) -> str:
    ''' 生成nginx配置文件中upstream块 '''
    server_str = ""
    server_r_single = ""
    r_upstream = ''
    temp = "upstream {dirname} {{  {server_str} }}"
    for dirname, socket_list in t.items():
        if len(socket_list) > 1:
            for s in socket_list:
                server_str += "server {s};\n".format(s=s)
            temp_upstream = temp.format(dirname=dirname, server_str=server_str)
        elif len(socket_list) == 1:
            server_str_single = "server {s};\n".format(s=socket_list[0])
            temp_upstream = temp.format(
                dirname=dirname, server_str=server_str_single)
        r_upstream += temp_upstream
    return r_upstream


def generateLocation(t: dict) -> str:
    '''  生成nginx配置文件中location块'''
    r_location_str = ""
    location_str = "location /{dirname}  {{proxy_pass http://{dirname};}}"
    for dirname in t:
        temp_location = location_str.format(dirname=dirname)
        r_location_str += temp_location
    return r_location_str


def jointNginxConf(str_upstream: str, str_location: str,
                   str_nginx_conf_head: str, str_nginx_conf_content: str,
                   str_nginx_conf_tail: str) -> str:
    """ 拼接nginx的配置文件 """
    str_nginx_conf = str_nginx_conf_head + str_upstream + \
        str_nginx_conf_content + str_location + str_nginx_conf_tail
    return str_nginx_conf


def writeNginxConf(str_nginx_conf: str):
    file_write = open("nginx.conf", mode="w", encoding='utf8')
    file_write.write(str_nginx_conf)
    file_write.close()


def formatNginxConf(str_nginx_conf:str):
    """ 调用nginxfmt格式化nginx的配置文件 """
    f = nginxfmt.Formatter()
    formatted_text = f.format_string(str_nginx_conf)
    return formatted_text


url = getUrl()

t = praseUrl(url)

str_upstream = generateUpstream(t)
str_location = generateLocation(t)
str_nginx_conf = jointNginxConf(
    str_upstream, str_location, str_nginx_conf_head, str_nginx_conf_content, str_nginx_conf_tail)

str_nginx_conf = formatNginxConf(str_nginx_conf)
writeNginxConf(str_nginx_conf)

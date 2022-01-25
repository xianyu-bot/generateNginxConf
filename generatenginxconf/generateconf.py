import re
from generatenginxconf.ztb_nginxconf_template import *
from generatenginxconf.nginxconf_template import *
from generatenginxconf import nginxfmt


def getUrl(url_str: str) -> list:
    url_list = []
    url_str = url_str.strip()
    url_list = url_str.split("\n")
    return url_list


def praseUrl(url: list) -> dict:
    ''' 遍历url，生成dirname和socket字典 '''
    upstream_dict = {}

    for url in url:
        url = url.replace('\n', '')
        socket = re.search(
            r'((\d){1,3}\.){3}(\d){1,3}\:(\d+)', url).group(0)  # 获取ip和端口
        dir_name = url.strip().rstrip('/').replace(
            'http://', '').split('/', 1)[1]  # 获取dirname

        if dir_name in upstream_dict:
            upstream_dict[dir_name].append(socket)
        else:
            upstream_dict[dir_name] = []
            upstream_dict[dir_name].append(socket)

    return upstream_dict


def generateUpstream(t: dict) -> str:
    ''' 生成nginx配置文件中upstream块 '''
    r_upstream = ''
    temp = "upstream {dirname} {{ keepalive 1024; {server_str} }}"
    server_str = "server {socket};\n"
    for dirname in t:
        temp_str = ""
        for i in t[dirname]:
            server = server_str.format(socket=i)
            temp_str += server
        temp_stream = temp.format(dirname=dirname, server_str=temp_str)
        r_upstream = r_upstream + temp_stream

    return r_upstream


def generateLocation(t: dict) -> str:
    '''  生成nginx配置文件中location块'''
    r_location_str = ""
    location_str = "location /{dirname}  {{proxy_pass http://{dirname};}}"
    for dirname in t:
        temp_location = location_str.format(dirname=dirname)
        r_location_str += temp_location
    return r_location_str


def ztbGenerateLocation(t: dict) -> str:
    r_location_str = ""
    location_str = "location /{dirname}  {{proxy_pass http://{dirname};}}"
    for dirname in t:
        if dirname == "TPFrame":
            temp_location_str = '''location /TPFrame {
            proxy_connect_timeout 75s;
            proxy_read_timeout 120s;
            proxy_send_timeout 120s;
            proxy_pass http://TPFrame;
        }

        location /TPFrame/websocket {
            proxy_pass     http://TPFrame;
            proxy_set_header Host $http_host;
            ##############添加对websocket的配置支持
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_connect_timeout 4s; #配置点1
            proxy_read_timeout 60s; #配置点2，如果没效，可以考虑这个时间配置长一点
            proxy_send_timeout 12s; #配置点3
        }'''
        elif dirname == "TPBidder":
            temp_location_str = '''        location /TPBidder {
            proxy_connect_timeout 75s;
            proxy_read_timeout 120s;
            proxy_send_timeout 120s;
            proxy_pass http://TPBidder;
        }
        location /TPBidder/websocket {
            proxy_pass     http://TPBidder;
            proxy_set_header Host $http_host;
            ##############添加对websocket的配置支持
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }'''

        elif dirname == "EpointWebService":
            temp_location_str = '''        location /EpointWebService {
            proxy_connect_timeout 75s;
            proxy_read_timeout 120s;
            proxy_send_timeout 120s;
            proxy_pass http://EpointWebService;
        }'''

        elif dirname == "ZtbFileWebServerJava":
            temp_location_str = '''        location /ZtbFileWebServerJava {
            proxy_connect_timeout 75s;
            proxy_read_timeout 120s;
            proxy_send_timeout 120s;
            proxy_pass http://ZtbFileWebServerJava;
        }'''

        elif dirname == "BSTool":
            temp_location_str = '''        location /BSTool {
            proxy_connect_timeout 600s;
            proxy_read_timeout 600s;
            proxy_send_timeout 600s;
            proxy_pass http://BSTool;
        }'''

        elif dirname == "TPPingBiao":
            temp_location_str = '''        #评标系统
	    location /TPPingBiao {
            proxy_connect_timeout 600s;
            proxy_read_timeout 600s;
            proxy_send_timeout 600s;
            proxy_pass http://TPPingBiao;
        }
        location /TPPingBiao/ws2/message {
            proxy_connect_timeout 75s;
            proxy_read_timeout 75s;
            proxy_send_timeout 75s;
            proxy_pass http://TPPingBiao;
            proxy_set_header Host $http_host;
            ##############添加对websocket的配置支持
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }'''

        elif dirname == "EpointBid_JingJia":
            temp_location_str = '''        location /EpointBid_JingJia {
            proxy_pass     http://EpointBid_JingJia;
        }
        location /EpointBid_JingJia/websocket {
            proxy_pass     http://EpointBid_JingJia;
            proxy_set_header Host $http_host;
            ##############添加对websocket的配置支持
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }'''

        elif dirname == "BidOpening":
            temp_location_str = '''        location /BidOpening {
            proxy_connect_timeout 600s;
            proxy_read_timeout 600s;
            proxy_send_timeout 600s;
            proxy_pass http://BidOpening;
        }
        location /BidOpening/websocket {
            proxy_connect_timeout 75s;
            proxy_read_timeout 75s;
            proxy_send_timeout 75s;
            proxy_pass http://BidOpening;
            proxy_set_header Host $http_host;
            ##############添加对websocket的配置支持
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }'''

        elif dirname == "BidOpeningHall":
            temp_location_str = '''        location /BidOpeningHall {
            proxy_connect_timeout 600s;
            proxy_read_timeout 600s;
            proxy_send_timeout 600s;
            proxy_pass http://BidOpeningHall;
        }
        location /BidOpeningHall/ws2 {
            proxy_connect_timeout 75s;
            proxy_read_timeout 75s;
            proxy_send_timeout 75s;
            proxy_pass http://BidOpeningHall;
            ##############添加对websocket的配置支持
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
        }'''

        elif dirname == "EpointWebBuilder":
            temp_location_str = '''        #网站大师
    	location /EpointWebBuilder {
            proxy_pass http://EpointWebBuilder;
            proxy_redirect off;
    		add_header Cache-Control no-cache;
    		proxy_set_header HOST $host;
    		proxy_set_header X-Real-IP $remote_addr;
    		proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    		client_max_body_size 10m;
    		client_body_buffer_size 128k;
    		proxy_connect_timeout 90;
    		proxy_send_timeout 90;
    		proxy_read_timeout 90;
    		proxy_buffer_size 4k;
    		proxy_buffers 4 32k;
    		proxy_busy_buffers_size 64k;
    		proxy_temp_file_write_size 64k;
        }'''
        elif dirname == "ASPFrame":
            temp_location_str = '''        location /ASPFrame{
            proxy_connect_timeout 75s;
            proxy_read_timeout 60s;
            proxy_send_timeout 60s;
            proxy_pass http://ASPFrame;
        }'''

        elif dirname == "EpointBI":
            temp_location_str = '''        location /EpointBI{
            proxy_connect_timeout 75s;
            proxy_read_timeout 60s;
            proxy_send_timeout 60s;
            proxy_pass http://EpointBI;
        }'''

        elif dirname == "EpointCBA":
            temp_location_str = '''        location /EpointCBA{
            proxy_connect_timeout 75s;
            proxy_read_timeout 60s;
            proxy_send_timeout 60s;
            proxy_pass http://EpointCBA;
        }'''

        else:
            temp_location_str = location_str.format(dirname=dirname)
        r_location_str += temp_location_str

    return r_location_str


def ztbJoinNginxConf(ztb_str_upstream: str, ztb_str_location: str,
                     ztb_str_nginx_conf_head: str, ztb_str_nginx_conf_content: str,
                     ztb_str_nginx_conf_tail: str) -> str:
    ztb_str_nginx_conf = ztb_str_nginx_conf_head + ztb_str_upstream + \
        ztb_str_nginx_conf_content + ztb_str_location + ztb_str_nginx_conf_tail
    return ztb_str_nginx_conf


def joinNginxConf(str_upstream: str, str_location: str,
                  str_nginx_conf_head: str, str_nginx_conf_content: str,
                  str_nginx_conf_tail: str) -> str:
    str_nginx_conf = str_nginx_conf_head + str_upstream + \
        str_nginx_conf_content + str_location + str_nginx_conf_tail
    return str_nginx_conf


def writeNginxConf(str_nginx_conf: str):
    file_write = open("nginx.conf", mode="w", encoding='utf8')
    file_write.write(str_nginx_conf)
    file_write.close()


def formatNginxConf(str_nginx_conf: str):
    f = nginxfmt.Formatter()
    formatted_text = f.format_string(str_nginx_conf)
    return formatted_text


def startConf(url_str: str):
    url = getUrl(url_str)
    t = praseUrl(url)
    str_upstream = generateUpstream(t)
    str_location = generateLocation(t)
    str_nginx_conf = joinNginxConf(
        str_upstream, str_location, str_nginx_conf_head, str_nginx_conf_content, str_nginx_conf_tail)

    str_nginx_conf = formatNginxConf(str_nginx_conf)
    writeNginxConf(str_nginx_conf)
    # print(str_nginx_conf)
    return str_nginx_conf


def ztbStartConf(url_str: str):
    url = getUrl(url_str)
    t = praseUrl(url)
    ztb_str_upstream = generateUpstream(t)
    ztb_str_location = ztbGenerateLocation(t)
    ztb_str_nginx_conf = ztbJoinNginxConf(
        ztb_str_upstream, ztb_str_location, ztb_str_nginx_conf_head, ztb_str_nginx_conf_content, ztb_str_nginx_conf_tail)

    ztb_str_nginx_conf = formatNginxConf(ztb_str_nginx_conf)
    writeNginxConf(ztb_str_nginx_conf)
    # writeNginxConf(str_nginx_conf)
    # print(str_nginx_conf)
    return ztb_str_nginx_conf

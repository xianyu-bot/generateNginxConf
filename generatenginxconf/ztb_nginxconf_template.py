ztb_str_nginx_conf_head = '''
user  nginx;
worker_processes  auto;
daemon off;
error_log  logs/error.log;
pid        /usr/local/nginx/nginx.pid;
events {
    worker_connections  65535;
}
worker_rlimit_nofile 65535;

http {
    include       mime.types;
    default_type  application/octet-stream;
    client_max_body_size 0;
    #charset utf-8;
    vhost_traffic_status_zone;
    log_format main '$time_local  $remote_addr:$remote_port  $request_method '
                  '$request_uri  $uri  $request_time '
                  '$status   $body_bytes_sent ' 
                  '$geoip2_data_country_name  $geoip2_data_subdivisions_name  $geoip2_data_city_name '
                  '$http_referer  $upstream_addr  $upstream_response_time ' 
                  '$http_user_agent  $http_x_forwarded_for  $content_length';

    access_log  logs/access.log  main;
    sendfile        on;
    tcp_nopush      on;
    tcp_nodelay     on;
    keepalive_timeout  65;
    gzip  on;
    server_tokens off;

    geoip2 /usr/local/nginx/conf/GeoLite2-Country.mmdb {
            $geoip2_data_country_code default=CN country iso_code;
            $geoip2_data_country_name default=CountryPrivate country names en;
    }
    
    geoip2 /usr/local/nginx/conf/GeoLite2-City.mmdb {
            $geoip2_data_city_name default=CityPrivate city names en;
            $geoip2_data_subdivisions_name default=ProvincePrivate subdivisions 0 names en;
    }
'''

ztb_str_nginx_conf_content = '''
    server {
        listen 80;
        server_name localhost;
        charset uft-8;
        client_max_body_size 64M; #修改文件的上传大小
        ###################后端RS服务器响应时间设置-START##################################
        proxy_connect_timeout 750s; #后端服务器连接的超时时间_发起握手等候响应超时时间
        proxy_read_timeout 600s; #连接成功后等候后端服务器响应时间其实已经进入后端的排队之中等候处理（也可以说是后端服务器处理请求的时间）  
        proxy_send_timeout 600s; #后端服务器数据回传时间_就是在规定时间之内后端服务器必须传完所有的数据
        #注：上面的配置主要是应对页面处理时间确实很长防止nginx主动关闭连接等导致客户请求4xx和5xx请求,但是不是设置的越长越好，应该针对页面的请求路径具体优化单独配置
        ###################后端RS服务器响应时间设置-END##################################
        ########################设置Nginx客户端IP透明专递 START##########################
        proxy_set_header Host $host:$server_port;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        ########################设置Nginx客户端IP透明专递 END##########################
        #proxy_set_header Connection "";
        #proxy_set_header X-Forwarded-Proto  $scheme;
        #charset koi8-r;
        #access_log  logs/host.access.log  main;#日志记录
        #log_format中电子交易加的特殊标记必须有
        set $EPUID "";
        if ($http_cookie ~* "EPUID=(.+?)(?=;|$)") {
	        set $EPUID $1;
        }       
        #WEB-INF禁止访问
        location ~ ^/(WEB-INF)/ { 
            deny all; 
        }    

        location = /50x.html {
            root   html;
        }
'''

ztb_str_nginx_conf_tail = '''
        #location ~ /\.ht {
        #    deny  all;
        #}
    }

}
'''



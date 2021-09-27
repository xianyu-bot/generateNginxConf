str_nginx_conf_head = '''
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
    log_format main '$time_local ^A $remote_addr ^A $request_method '
    ^A '$request_uri ^A $uri ^A $request_time '
    ^A '$status ^A  $body_bytes_sent '
    ^A '$geoip2_data_country_name ^A $geoip2_data_subdivisions_name ^A $geoip2_data_city_name '
    ^A '$http_referer ^A $upstream_addr ^A $upstream_response_time '
    ^A '$http_user_agent ^A $http_x_forwarded_for';

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

str_nginx_conf_content = '''
    server {
        listen       80;
        server_name  localhost;
        proxy_http_version 1.1;
        proxy_set_header Connection "";
        proxy_connect_timeout 75s; 
        proxy_read_timeout 60s; 
        proxy_send_timeout 60s;
		    proxy_set_header Host $http_host;
		    proxy_set_header X-Real-IP $remote_addr;
		    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto  $scheme;

        location / {
            root   html;
            index  index.html index.htm;
        }

        location  ~ ^(.*)\/\.svn\/  {
            return 404;
        }

        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }

        location /epoint_base_status {
                    auth_basic "epointsafe";
                    auth_basic_user_file /usr/local/nginx/conf/htpasswd;
                    vhost_traffic_status_display;
                    vhost_traffic_status_display_format html;
        }
'''

str_nginx_conf_tail = '''
        #location ~ /\.ht {
        #    deny  all;
        #}
    }

}
'''

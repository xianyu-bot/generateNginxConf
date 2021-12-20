# generateNginxConf

## 1.安装方法
下载压缩包解压即可，需要python3环境

## 2.使用方法
解压包后，进入目录下，在url.txt中输入url，然后执行
```bash
pip3 install flask
python3 generateNginxConf.py
# windows环境下使用
pip install flask
python generateNginxConf.py
```
配置文件会生成至nginx.conf中，复制即可。

## 3.注意事项

1. 即使端口为默认端口80或者443，在输入url时，也不要省略端口号
2. 目前版本仅支持匹配第一级路径，未来考虑支持多级路径。
from flask import Flask,render_template,request,url_for,redirect,flash
from generatenginxconf.generateconf import startConf


app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def index():
    str_nginx_conf = "This is template"
    if request.method == 'POST':
        url_str = request.form.get('url_str')
        str_nginx_conf = startConf(url_str)

    
    return render_template('index.html', str_nginx_conf=str_nginx_conf)


if __name__ == '__main__':
    app.run(debug=True)
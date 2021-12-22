from flask import Flask,render_template,request,url_for,redirect,flash,send_from_directory
from generatenginxconf.generateconf import startConf, ztbStartConf


app = Flask(__name__)


@app.route('/',methods=['GET','POST'])
def index():
    str_nginx_conf = "This is template"
    if request.method == 'POST':
        url_str = request.form.get('url_str')
        project_type = request.form.get('project_type')
        if project_type == "非电子交易" :
            str_nginx_conf = startConf(url_str)
        else:
            str_nginx_conf = ztbStartConf(url_str)

    
    return render_template('index.html', str_nginx_conf=str_nginx_conf)

@app.route('/download')
def download():
    return send_from_directory("./", "nginx.conf", as_attachment=True)


if __name__ == '__main__':
    app.run(debug=False)

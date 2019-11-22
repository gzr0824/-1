# coding:utf-8
from flask import Flask
from app import app
import index
from index import bp
from werkzeug.serving import run_simple

# 引入蓝图
app.register_blueprint(bp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False,threaded=True,port=8000)
    # run_simple("0.0.0.0",5000,app,threaded=True);
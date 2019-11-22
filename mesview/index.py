# coding:utf-8
# User: HunterK
# DateTime: 10/17/2019 20:00 PM
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, Markup ,Response
)
import pymysql
from werkzeug.wrappers import Request, Response
from decimal import Decimal
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import extract,func
from app import app
from Request import *
import json, time, random
from flask_socketio import SocketIO, emit, send
import cv2

camera_root = app.config.get('CAMERA_ROOT')
camera_pwd = app.config.get('CAMERA_PWD')
camera_ip = app.config.get('CAMERA_IP')
station_ip = app.config.get('STATION_IP')
rfid_ip = app.config.get('RFID_IP')
# camera = cv2.VideoCapture(0)
bp = Blueprint('index', __name__, url_prefix='')

@bp.route('/index')
@bp.route('/')
def index():
    return render_template('index.html')


def gen_frames():
    camera = cv2.VideoCapture('rtsp://' + camera_root + ':' + camera_pwd + '@' + camera_ip + ':554/cam/realmonitor?channel=1&subtype=0')
    while True:
        success, frame = camera.read()
        if not success:
            camera = cv2.VideoCapture('rtsp://' + camera_root + ':' + camera_pwd + '@' + camera_ip + ':554/cam/realmonitor?channel=1&subtype=0')
            continue
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/mesview/get_all_data',methods=["POST"])
def get_all_data():
    try:
        db = SQLAlchemy(app)
        class DeviceInformation(db.Model):
            ''' 机床数据更新
            '''
            __tablename__ = 'device_information'
            id = db.Column(db.Integer, primary_key=True)
            ip = db.Column(db.Unicode(50))
            network_status = db.Column(db.Integer)
            info = db.Column(db.Unicode(1024))
            info_remark = db.Column(db.Unicode(1024))
            update_time = db.Column(db.DateTime)

        db.create_all()
        nc_ip = station_ip
        obj1 = DeviceInformation.query.filter_by(ip=nc_ip).first()

        if obj1.network_status == 1:
            obj1_list = json.loads(obj1.info)
            data1 = obj1_list['data1'] # 机床模式
            data2 = obj1_list['data2'] # 机床灯
            data3 = obj1_list['data3'] # 主轴转速
            data4 = obj1_list['data4'] # 夹具状态
            data5 = obj1_list['data5'] # 门开状态
            data6 = obj1_list['data6'] # 报警状态
            data7 = obj1_list['data7'] # 完成状态
            data8 = obj1_list['data8'] # x轴坐标
            data9 = obj1_list['data9'] # y轴坐标
            data10 = obj1_list['data10'] # 生产效率

            obj1_remark_list = json.loads(obj1.info_remark)
            data1_remark = obj1_remark_list['data1_remark']
            data2_remark = obj1_remark_list['data2_remark']
            data3_remark = obj1_remark_list['data3_remark']
            data4_remark = obj1_remark_list['data4_remark']
            data5_remark = obj1_remark_list['data5_remark']
            data6_remark = obj1_remark_list['data6_remark']
            data7_remark = obj1_remark_list['data7_remark']
            data8_remark = obj1_remark_list['data8_remark']
            data9_remark = obj1_remark_list['data9_remark']
            data10_remark = obj1_remark_list['data10_remark']

            nc_update = {'network_status':obj1.network_status,'data1':data1,'data2':data2,'data3':data3,'data4':data4,'data5':data5,'data6':data6,'data7':data7,'data8':data8,'data9':data9,'data10':data10,'data1_remark':data1_remark,'data2_remark':data2_remark,'data3_remark':data3_remark,'data4_remark':data4_remark,'data5_remark':data5_remark,'data6_remark':data6_remark,'data7_remark':data7_remark,'data8_remark':data8_remark,'data9_remark':data9_remark,'data10_remark':data10_remark,'update_time':str(obj1.update_time)}
        else:
            nc_update = {'network_status':obj1.network_status}

    except Exception as err:
        print(err)
        nc_update = {'network_status':0}

    rs = Request.req_get("http://"+rfid_ip+"/api/rfid/get_rfid_data")
    if rs:
        if rs['status'] == "success":
            rfid_update = {'rfid1_material_id':rs['data']['ant1']['material_id'],'rfid1_id':rs['data']['ant1']['rfid_id'],'rfid2_material_id':rs['data']['ant2']['material_id'],'rfid2_id':rs['data']['ant2']['rfid_id']}
        elif rs['status'] == "error":
            rfid_update = {'rfid1_material_id':'0','rfid1_id':'0','rfid2_material_id':'0','rfid2_id':'0'}
    else:
        rfid_update = {'rfid1_material_id':'0','rfid1_id':'0','rfid2_material_id':'0','rfid2_id':'0'}

    rs = {"nc_update":nc_update,'rfid_update':rfid_update}

    return json.dumps(rs)

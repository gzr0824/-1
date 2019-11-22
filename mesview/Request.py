0# coding:utf-8
# User: HunterK
# DateTime: 6/18/2019 20:00 PM
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, abort, Markup
)
from app import app
import urllib.request
import urllib.parse
import json
import requests

class Request(object):
    # get请求
    def req_get(url):
        try:
            response = urllib.request.urlopen(url,timeout=3)
            rs = response.read().decode("utf-8")
        except:
            return False
        if rs == None or rs == '':
            return False
        return json.loads(rs)
    
    # post请求
    def req_send(url,value):
        try:
            data = bytes(urllib.parse.urlencode(value), encoding='utf8')
            response = urllib.request.urlopen(url, data=data,timeout=3)
            rs = response.read().decode("utf-8")
        except:
            return False
        if rs == None or rs == '':
            return False
        return json.loads(rs)

    # 传文件
    def req_file(url,file_path):
        try:
            files = {"nc_file":open(file_path, "rb")}
            rs = requests.post(url, files=files,timeout=5)
        except:
            return False
        if rs == None or rs == '':
            return False
        return json.loads(rs.text)

    def req_get_door(url):
        try:
            response = urllib.request.urlopen(url,timeout=3)
            rs = response.read().decode("utf-8")
        except:
            return False
        if rs == None or rs == '':
            return False
        return json.loads(rs)


        
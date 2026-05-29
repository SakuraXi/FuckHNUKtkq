# -*- coding: utf-8 -*-
# @Time    : 2026.5.28
# @Author  : xlxlSakura
# @FileName: fuckHNU.py
# @Software: PyCharm
# @Description: Automatically FUCK the attendance system of HNU and CRACK the reg-token violently.
# @Version: 0.1

import time
import requests
import payLoadsUtils
import signUtils
from flask import Flask, render_template, redirect, url_for
from datetime import datetime
import json

app = Flask(__name__)
privateKey = "00f661332f70969150a8ea126943958a914cc05abc7e3ad3d96570cc4fd01a9ce4"
serverUrl = "https://ktkq.hainanu.edu.cn/app"

def send_post(apiurl,postpayload):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 26_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.73(0x18004935) NetType/WIFI Language/zh_CN",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Referer": "https://servicewechat.com/wxa1e3abcd201139a2/35/page-frame.html"
    }
    try:
        response = requests.post(url=serverUrl + "/" + apiurl, data=postpayload, headers=headers, timeout=10)
        response.raise_for_status()
        print("请求成功！")
        print("返回结果:", response.text)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求发送失败: {e}")

@app.route('/')
def index():
    # 1. 获取当前时间并格式化
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    time_str = now.strftime("%H:%M:%S")
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday_str = week_list[now.weekday()]

    # 2. 将时间变量传给网页
    return render_template('index.html',
                           schedule=today_schedule,
                           today_date=date_str,
                           today_time=time_str,
                           weekday=weekday_str)

@app.route('/signin/<int:course_id>')
def signin_page(course_id):
    # 根据 ID 找到对应的课程
    course = next((item for item in today_schedule if item["id"] == course_id), None)
    if course:
        return render_template('signin.html', course=course)
    return "课程未找到", 404

@app.route('/do_signin/<int:course_id>')
def do_signin(course_id):
    # 在内存中修改变量状态
    for course in today_schedule:
        if course["id"] == course_id:
            course["status"] = "已签到"
            break
    # 签到成功后跳回主页
    return redirect(url_for('index'))

if __name__ == "__main__":
    timestamp = int(time.time() * 1000)
    sts = str(timestamp)
    sign = signUtils.sm2_sign(sts, privateKey)
    signUtils.sm2_valid(sign, privateKey, sts)
    print(f"SM2 签名结果: {sign}")

    pl_getQdKbList = {
        "sign": sign,
        "timestamp": sts,
        "userType": "1",
        "userCode": "20253002390",
        "unitCode": "10589",
        "userName": "刘宸铄",
        "roleCode": "0",
        "bm": "null",
        "xyMc": "环境科学与工程学院",
        "zy": "环境科学",
        "bj": "环境科学2025-4",
        "xsCc": "1",
        "scene": "1",
        "key": "1"
    }

    qdkblist = payLoadsUtils.process_GetQdKbList(send_post("getQdKbList", pl_getQdKbList))
    print(qdkblist[0])
    # xsqdinfo = payLoadsUtils.process_GetXsQdInfo(qdkblist)
    # print(xsqdinfo)

    today_schedule = [{
        "id" : 0,
        "name": "大学英语",
        "status": "未签到",
        "location": "教B-204",
        "time": "10:00 - 11:35",
        "period": "第3-4节",
        "teacher": "李老师"
    },]

    for lec in qdkblist:
        lec_info = {"id": qdkblist.index(lec)+ 1}
        for i in lec:
            if i == "kcMc":
                lec_info["name"] = lec[i]
            elif i == "xsQdQkMc":
                lec_info["status"] = str(lec[i]) + "到"
            elif i == "skDd":
                lec_info["location"] = lec[i]
            elif i == "skSj":
                lec_info["time"] = str(lec[i]).split("(")[1].replace(")","")
                lec_info["period"] = str(lec[i]).split("(")[0]
            elif i == "skJs":
                lec_info["teacher"] = lec[i]
        today_schedule.append(lec_info)
    print(today_schedule)
    app.run(debug=True, port=5000)
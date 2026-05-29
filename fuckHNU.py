# -*- coding: utf-8 -*-
# @Time    : 2026.5.28
# @Author  : xlxlSakura
# @FileName: fuckHNU.py
# @Software: PyCharm
# @Description: Automatically FUCK the attendance system of HNU and CRACK the reg-token violently.
# @Version: 0.1

import re
import time
import requests
import payLoadsUtils
import signUtils
from flask import Flask, render_template, redirect, url_for, request
from datetime import datetime
import json

app = Flask(__name__)
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

def signWithCode(classId, code, location):
    pl = payLoadsUtils.process_GetXsQdInfo(qdkblist[classId-1])
    print("getXsQdInfo", pl)

    pl1 = payLoadsUtils.process_GetGpsWzJl(qdkblist[classId-1]["qdId"],location)
    print("getGpsWzJl", pl1)

    pl2 = payLoadsUtils.process_SaveXsQdInfo(qdkblist[classId-1],code,location)
    print("saveXsQdInfo", pl2)

@app.route('/')
def index():
    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    time_str = now.strftime("%H:%M:%S")
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday_str = week_list[now.weekday()]
    return render_template('index.html', schedule=today_schedule, today_date=date_str, today_time=time_str, weekday=weekday_str)

@app.route('/signin/<int:course_id>')
def signin_page(course_id):
    course = next((item for item in today_schedule if item["id"] == course_id), None)
    if course:
        reloc = "3号教学楼"

        return render_template('signin.html', course=course, locations=payLoadsUtils.location_options.keys(), recommend_loc=reloc)
    return "课程未找到", 404


@app.route('/do_signin/<int:course_id>', methods=['POST'])
def do_signin(course_id):
    selected_location = request.form.get('location')
    has_code = request.form.get('has_code')
    signin_code = request.form.get('signin_code')

    if has_code:
        if not signin_code or not re.match(r'^\d{4}$', signin_code):
            return "提交失败：签到码格式不正确（必须为4位数字）", 400

    print(f"--- 收到签到请求 ---")
    print(f"课程ID: {course_id}")
    print(f"确认地点: {selected_location}")
    print(f"是否有签到码: {'是' if has_code else '否'}")
    if has_code:
        print(f"签到码内容: {signin_code}")
    print(f"------------------")

    signWithCode(course_id, signin_code, selected_location)


    # 3. 更新内部变量状态
    for course in today_schedule:
        if course["id"] == course_id:
            course["status"] = "已签到"
            break

    return redirect(url_for('index'))

if __name__ == "__main__":
    sign = signUtils.getSignAndTimestamp()
    signUtils.sm2_valid(sign[0], signUtils.privateKey, sign[1])
    print(f"SM2 签名结果: {sign}")

    pl_getQdKbList = {
        "sign": sign[0],
        "timestamp": sign[1],
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

    today_schedule = [{
        "id" : 0,
        "name": "大学英语",
        "status": "未签到",
        "location": "(海甸)3-205",
        "time": "10:00~11:35",
        "period": "第3,4节",
        "teacher": "李老师"
    },]

    for lec in qdkblist:
        lec_info = {"id": qdkblist.index(lec)+ 1}
        for i in lec:
            if i == "kcMc":
                lec_info["name"] = lec[i]
            elif i == "xsQdQkMc":
                # lec_info["status"] = str(lec[i]) + "到"
                lec_info["status"] = "未签到"
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
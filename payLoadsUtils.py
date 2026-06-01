# -*- coding: utf-8 -*-
# @Time    : 2026-05-29
# @Author  : xlxlSakura
# @FileName: payLoadsUtils.py
# @Software: PyCharm
# @Description: API-Payloads processing utilities.
# @Version: 0.1

import studentInfo
import signUtils

location_options = {
    "3号教学楼" : ["110.32580068426542","20.05833084181918"]
    ,"4号教学楼" : ["110.32724389990553","20.05901300751073"]
    ,"5号教学楼" : ["110.3282317985653","20.062391497296275"]
    ,"6号教学楼": ["110.32937867587619","20.060006239101234"]
    ,"7号教学楼": ["110.32936868059865","20.06052579127188"]
    ,"9号教学楼": ["110.33123279466301","20.06002974783358"]
    ,"10号教学楼": ["110.33126289729519","20.060719236083752"]
    ,"实验楼" : ["110.33046102616181","20.05899912939425"]
    ,"一田" : ["110.3291079996823","20.05853693768231"]
    ,"二田" : ["110.32433736519832","20.056229821403946"]
}

pl_getXsQdInfo = {
    "sign": "",
    "timestamp": "",
    "unitCode": "",
    "userCode": "",
    "userName": "",
    "xkKh": "",
    "xqj": "",
    "djj": "",
    "djz": "",
    "qdId": "",
    "isFz": "",
    "fzMC": ""
}
pl_getQdKbList = {
    "sign": "",
    "timestamp": "",
    "userType": "",
    "userCode": "",
    "unitCode": "",
    "userName": "",
    "roleCode": "",
    "bm": "",
    "xyMc": "",
    "zy": "",
    "bj": "",
    "xsCc": "",
    "scene": "",
    "key": ""
}
pl_getGpsWzJl = {
    "sign": "",
    "userType": "",
    "userCode": "",
    "userName": "",
    "unitCode": "",
    "wzJd": "",
    "wzWd": "",
    "wzJd2": "",
    "wzWd2": "",
    "qdId": "",
    "type": ""
}
pl_saveXsQdInfo = {
    "sign": "",
    "timestamp": "",
    "unitCode": "",
    "userCode": "",
    "userName": "",
    "syMc": "",
    "syBjMc": "",
    "dsZgh": "",
    "dsXm": "",
    "fdyZgh": "",
    "fdyXm": "",
    "bjMc": "",
    "zyMc": "",
    "xyMc": "",
    "wzJd": "",
    "wzWd": "",
    "qdId": "",
    "xkKh": "",
    "skDd": "",
    "xqj": "",
    "djj": "",
    "djz": "",
    "isFace": "",
    "wzAcc": "",
    "bqMode": "",
    "isFz": "",
    "djc": "",
    "qdJc": "",
    "kcMc": "",
    "jsXm": "",
    "skCd": "",
    "kl": "",
    "wtDa": "",
    "qdLx": ""
}

def getStudentClassesPayload(student):
    payload = pl_getQdKbList
    stuInfo = studentInfo.getStudentInfo(student)
    for i in stuInfo:
        for o in payload:
            if o == i:
                payload[o] = stuInfo[i]
                break
    payload["zy"] = stuInfo["zyMc"]
    payload["bj"] = stuInfo["bjMc"]
    payload["userType"] = "1"
    payload["xsCc"] = "1"
    payload["scene"] = "1"
    payload["key"] = "1"
    payload["roleCode"] = "0"
    payload["bm"] = "null"
    sign = signUtils.getSignAndTimestamp()
    payload["sign"] = sign[0]
    payload["timestamp"] = sign[1]
    return payload

def process_GetUserOpenId(raw_json):
    info = {}
    userBindInfo = raw_json["userBindInfo"]
    info["unitCode"] = userBindInfo["unitCode"]
    info["userCode"] = userBindInfo["userCode"]
    info["userName"] = userBindInfo["userName"]
    info["syMc"] = userBindInfo["syMc"]
    info["syBjMc"] = userBindInfo["syBjMc"]
    info["dsZgh"] = userBindInfo["dsZgh"]
    info["dsXm"] = userBindInfo["dsXm"]
    info["fdyZgh"] = userBindInfo["fdyZgh"]
    info["fdyXm"] = userBindInfo["fdyXm"]
    info["bjMc"] = userBindInfo["bj"]
    info["zyMc"] = userBindInfo["zy"]
    info["xyMc"] = userBindInfo["xy"]
    info["xn"] = "2025-2026"
    info["wxSign"] = userBindInfo["sign"]
    return info

def process_GetQdKbList(raw):
    raw_data = raw["Rows"]
    return raw_data

def process_GetXsQdInfo(student,raw_data):
    payload = pl_getXsQdInfo
    stuInfo = studentInfo.getStudentInfo(student)
    for i in raw_data:
        for o in payload:
            if o == i:
                payload[o] = raw_data[i]
                break
    for i in stuInfo:
        for o in payload:
            if o == i:
                payload[o] = stuInfo[i]
                break
    payload["fzMC"] = "全部"
    sign = signUtils.getSignAndTimestamp()
    payload["sign"] = sign[0]
    payload["timestamp"] = sign[1]
    return payload

def process_GetGpsWzJl(student,qdId,location):
    payload = pl_getGpsWzJl
    stuInfo = studentInfo.getStudentInfo(student)
    for i in stuInfo:
        for o in payload:
            if o == i:
                payload[o] = stuInfo[i]
                break
    payload["userType"] = "1"
    payload["type"] = "2"
    payload["wzJd"] = location_options[location][0]
    payload["wzWd"] = location_options[location][1]
    payload["wzJd2"] = "0.0"
    payload["wzWd2"] = "0.0"
    payload["qdId"] = qdId
    payload["sign"] = stuInfo["wxSign"]
    return payload

def process_SaveXsQdInfo(student,qdKcInfo, code, location):
    payload = pl_saveXsQdInfo
    stuInfo = studentInfo.getStudentInfo(student)
    for i in qdKcInfo:
        for o in payload:
            if o == i:
                payload[o] = qdKcInfo[i]
                break
    for i in stuInfo:
        for o in payload:
            if o == i:
                payload[o] = stuInfo[i]
                break
    payload["jsXm"] = qdKcInfo["skJs"]
    payload["kl"] = code
    payload["wzJd"] = location_options[location][0]
    payload["wzWd"] = location_options[location][1]
    payload["fzMC"] = "全部"
    payload["isFace"] = "undefined"
    payload["isFz"] = "undefined"
    payload["wzAcc"] = "5"
    payload["wtDa"] = ""
    sign = signUtils.getSignAndTimestamp()
    payload["sign"] = sign[0]
    payload["timestamp"] = sign[1]
    return payload
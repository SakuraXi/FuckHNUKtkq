# -*- coding: utf-8 -*-
# @Time    : 2026-05-29
# @Author  : xlxlSakura
# @FileName: payLoadsUtils.py
# @Software: PyCharm
# @Description: API-Payloads processing utilities.
# @Version: 0.1

import studentInfo
import signUtils

location_options = {"3号教学楼" : [3,3], "4号教学楼" : [4,4], "5号教学楼" : [5,5], "实验楼" : [6,6], "一田" : [1,1], "二田" : [2,2]}

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

stuInfo = studentInfo.infos

def process_GetQdKbList(raw):
    raw_data = raw["Rows"]
    return raw_data

def process_GetXsQdInfo(raw_data):
    payload = pl_getXsQdInfo
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

def process_GetGpsWzJl(qdId,location):
    payload = pl_getGpsWzJl
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
    sign = signUtils.getSignAndTimestamp()
    payload["sign"] = sign[0]
    return payload

def process_SaveXsQdInfo(raw_data):
    payload = pl_saveXsQdInfo
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
    return payload
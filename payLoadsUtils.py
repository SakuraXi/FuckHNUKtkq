# -*- coding: utf-8 -*-
# @Time    : 2026-05-29
# @Author  : xlxlSakura
# @FileName: payLoadsUtils.py
# @Software: PyCharm
# @Description: API-Payloads processing utilities.
# @Version: 0.1

import studentInfo

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
    "type2": ""
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
    return payload

def process_GetGpsWzJl(raw_data):
    payload = pl_getGpsWzJl
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
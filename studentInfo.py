# -*- coding: utf-8 -*-
# @Time    : 2026-05-29
# @Author  : xlxlSakura
# @FileName: studentInfo.py
# @Software: PyCharm
# @Description: 
# @Version: 1.0

import signUtils
import json
import logging

def get_infos():
    with open(signUtils.resource_path("studentsInfo.json"), "r", encoding="utf-8") as f:
        raw = f.read()
    data = json.loads(raw)
    return data["infos"]

def get_users():
    with open(signUtils.resource_path("studentsInfo.json"), "r", encoding="utf-8") as f:
        raw = f.read()
    data = json.loads(raw)
    return data["users"]

def getStudentInfo(student) :
    users_list = get_users()
    infos = get_infos()
    if student not in users_list.keys() :
        logging.error("无效用户")
        return None
    for i in infos:
        if i["userCode"] == users_list[student]:
            return i

def getStudentInfoByCode(student_code) :
    users_list = get_users()
    infos = get_infos()
    if student_code not in users_list.values() :
        logging.error("无效用户")
        return None
    for i in infos:
        if i["userCode"] == student_code:
            return i

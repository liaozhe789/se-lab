# -*- coding: utf-8 -*-
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _lib_usecase import draw

actors = {
    "F": (11, 92, "家属\n(FamilyMember)"),
    "D": (11, 60, "医生\n(Doctor)"),
    "E": (11, 16, "老人\n(Elder)"),
    "R": (89, 92, "机器人\n(Robot)"),
    "T": (89, 56, "时钟\n(Timer)"),
    "A": (89, 10, "管理员\n(Administrator)"),
}

usecases = {
    "UC01": (38, 88, "控制机器人"),
    "UC02": (38, 72, "监视老人"),
    "UC03": (38, 48, "用户登录"),
    "UC04": (38, 26, "视频/语音交互"),
    "UC05": (62, 88, "自主跟随老人"),
    "UC06": (62, 72, "获取老人信息"),
    "UC07": (62, 56, "检测异常状况"),
    "UC08": (62, 40, "通知异常状况"),
    "UC09": (62, 22, "提醒服务"),
    "UC10": (62, 10, "系统设置"),
}

links = [
    ("F", "UC01"), ("F", "UC02"), ("F", "UC03"),
    ("D", "UC02"), ("D", "UC03"), ("D", "UC06"), ("D", "UC04"),
    ("E", "UC03"), ("E", "UC04"), ("E", "UC09"),
    ("R", "UC05"), ("R", "UC06"),
    ("T", "UC07"), ("T", "UC09"),
    ("A", "UC10"),
]

rels = [
    ("UC04", "UC03", "include"),
    ("UC02", "UC06", "include"),
    ("UC02", "UC07", "include"),
    ("UC07", "UC08", "include"),
    ("UC09", "UC08", "include"),
    ("UC05", "UC06", "include"),
    ("UC01", "UC05", "extend"),
]

draw(actors, usecases, links, rels,
     box=(26, 4, 74, 96),
     figsize=(8.6, 5.6),
     title=None,
     out=os.path.join(os.path.dirname(os.path.abspath(__file__)), "01_系统整体用例图.png"))

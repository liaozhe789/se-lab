# -*- coding: utf-8 -*-
"""生成 5 个功能模块的用例图。"""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _lib_usecase import draw

OUT = HERE

# ---------- 模块一：用户与权限管理 ----------
draw(
    actors={
        "E": (10, 70, "老人\n(Elder)"),
        "F": (10, 44, "家属\n(FamilyMember)"),
        "D": (10, 18, "医生\n(Doctor)"),
        "A": (90, 44, "管理员\n(Administrator)"),
    },
    usecases={
        "U1": (48, 62, "用户登录"),
        "U2": (48, 24, "系统设置"),
    },
    links=[("E", "U1"), ("F", "U1"), ("D", "U1"), ("A", "U1"), ("A", "U2")],
    rels=[("U2", "U1", "include")],
    box=(26, 10, 76, 84),
    box_label="用户与权限管理模块",
    title=None,
    figsize=(6.2, 3.7), uc_w=8.0, uc_h=3.2,
    out=os.path.join(OUT, "02_模块用例图_用户与权限.png"),
)

# ---------- 模块二：视频语音交互 ----------
draw(
    actors={
        "E": (10, 66, "老人\n(Elder)"),
        "F": (10, 34, "家属\n(FamilyMember)"),
        "D": (90, 50, "医生\n(Doctor)"),
    },
    usecases={
        "U1": (50, 62, "视频/语音交互"),
        "U2": (50, 24, "用户登录"),
    },
    links=[("E", "U1"), ("F", "U1"), ("D", "U1")],
    rels=[("U1", "U2", "include")],
    box=(28, 10, 74, 84),
    box_label="视频语音交互模块",
    title=None,
    figsize=(6.2, 3.7), uc_w=9.0, uc_h=3.2,
    out=os.path.join(OUT, "03_模块用例图_视频语音交互.png"),
)

# ---------- 模块三：老人看护监控 ----------
draw(
    actors={
        "F": (10, 88, "家属\n(FamilyMember)"),
        "D": (10, 50, "医生\n(Doctor)"),
        "T": (90, 44, "时钟\n(Timer)"),
        "R": (90, 16, "机器人\n(Robot)"),
    },
    usecases={
        "U1": (44, 82, "监视老人"),
        "U2": (72, 62, "获取老人信息"),
        "U3": (44, 44, "检测异常状况"),
        "U4": (72, 22, "通知异常状况"),
    },
    links=[("F", "U1"), ("D", "U2"), ("T", "U3"), ("R", "U2")],
    rels=[("U1", "U2", "include"), ("U1", "U3", "include"), ("U3", "U4", "include")],
    box=(28, 8, 86, 94),
    box_label="老人看护监控模块",
    title=None,
    figsize=(6.8, 4.0), uc_w=8.4, uc_h=3.2,
    out=os.path.join(OUT, "04_模块用例图_看护监控.png"),
)

# ---------- 模块四：机器人控制 ----------
draw(
    actors={
        "F": (10, 72, "家属\n(FamilyMember)"),
        "R": (90, 46, "机器人\n(Robot)"),
    },
    usecases={
        "U1": (44, 72, "控制机器人"),
        "U2": (44, 38, "自主跟随老人"),
        "U3": (72, 55, "获取老人信息"),
    },
    links=[("F", "U1"), ("R", "U2"), ("R", "U3")],
    rels=[("U1", "U2", "extend"), ("U2", "U3", "include")],
    box=(26, 18, 86, 86),
    box_label="机器人控制模块",
    title=None,
    figsize=(6.5, 3.7), uc_w=8.4, uc_h=3.2,
    out=os.path.join(OUT, "05_模块用例图_机器人控制.png"),
)

# ---------- 模块五：定时提醒 ----------
draw(
    actors={
        "E": (10, 66, "老人\n(Elder)"),
        "F": (10, 24, "家属\n(FamilyMember)"),
        "T": (90, 66, "时钟\n(Timer)"),
    },
    usecases={
        "U1": (48, 62, "提醒服务"),
        "U2": (48, 24, "通知异常状况"),
    },
    links=[("E", "U1"), ("T", "U1"), ("F", "U2")],
    rels=[("U1", "U2", "include")],
    box=(26, 10, 76, 84),
    box_label="定时提醒模块",
    title=None,
    figsize=(6.2, 3.7), uc_w=8.4, uc_h=3.2,
    out=os.path.join(OUT, "06_模块用例图_定时提醒.png"),
)

# -*- coding: utf-8 -*-
"""填充实验三报告正文（类图与状态图）。"""
import os, copy
import docx
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.text.paragraph import Paragraph

BASE = r"C:\Users\qiyong\Desktop\实验报告\软件工程"
DOC = os.path.join(BASE, "240531142祁勇-实验三.docx")
DIA = os.path.join(BASE, "se-lab", "实验三", "diagrams")

d = docx.Document(DOC)
t = d.tables[0]


def set_cell(cell, text):
    p = cell.paragraphs[0]
    if p.runs:
        p.runs[0].text = text
        for r in p.runs[1:]:
            r.text = ""
    else:
        p.add_run(text)


def reset(cell, keep=1):
    for p in cell.paragraphs[keep:]:
        p._p.getparent().remove(p._p)


def body(cell, text, tpl, no_num=False):
    newp = copy.deepcopy(tpl._p)
    for r in newp.findall(qn("w:r")):
        newp.remove(r)
    if no_num:
        pPr = newp.find(qn("w:pPr"))
        if pPr is not None:
            for np_ in pPr.findall(qn("w:numPr")):
                pPr.remove(np_)
    cell._tc.append(newp)
    p = Paragraph(newp, cell)
    run = p.add_run(text)
    tpl_r = tpl.runs[0]._element
    rPr = tpl_r.find(qn("w:rPr"))
    if rPr is not None:
        run._element.insert(0, copy.deepcopy(rPr))
    return p


def pic(cell, name, width_cm, caption):
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.first_line_indent = Pt(0)
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(os.path.join(DIA, name), width=Cm(width_cm))
    c = cell.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.first_line_indent = Pt(0)
    c.paragraph_format.space_after = Pt(6)
    r = c.add_run(caption)
    r.font.name = "宋体"
    r.font.size = Pt(10.5)
    r._element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")


# ---------- 封面 ----------
set_cell(t.rows[1].cells[1], "空巢老人看护软件需求分析")
set_cell(t.rows[2].cells[3], "设计性")
set_cell(t.rows[3].cells[5], "2026年11月18日")

BODY_TPL = t.rows[4].cells[0].paragraphs[1]

# ---------- 一、实验目的和要求 ----------
c = t.rows[4].cells[0]
reset(c, keep=1)
body(c, "（1）掌握类图、状态图的核心要素与绘制方法，能按 UML 规范完成静态结构与动态行为的建模。", BODY_TPL)
body(c, "（2）以空巢老人看护软件为对象，完成从需求到模型的转化，并通过一致性检查验证两类模型之间没有矛盾。", BODY_TPL)

# ---------- 二、实验环境 ----------
c = t.rows[5].cells[0]
reset(c, keep=1)
body(c, "Windows 11 专业版；Python 3.13；PlantUML 1.2024.7（JDK 25 运行）；Git 2.55.0；"
        "远程仓库 GitHub se-lab。", BODY_TPL, no_num=True)

# ---------- 三、实验内容 ----------
c = t.rows[6].cells[0]
reset(c, keep=1)
body(c, "（1）静态结构分析。识别系统中的核心类，定义各类的属性与操作，分析继承、组合与关联关系，绘制类图。", BODY_TPL)
body(c, "（2）动态行为分析。针对状态变化复杂的机器人与紧急警报两个对象绘制状态图，标明状态、迁移事件与条件。", BODY_TPL)
body(c, "（3）模型整合与验证。检查类图与状态图的对应关系，确认状态名、迁移动作都能在类图中找到依据。", BODY_TPL)

# ---------- 四、实验步骤 ----------
c = t.rows[7].cells[0]
HEAD_TPL = c.paragraphs[1]
reset(c, keep=1)
body(c, "（一）类的识别", HEAD_TPL)
body(c, "从实验二的用例图和顺序图反推参与交互的对象。人员角色都有账号、密码与登录行为，归入抽象类用户，"
        "老人、家属、医生、管理员作为它的子类；机器人、紧急警报、视频通话、监测记录属于业务实体，各自独立成类。"
        "最终得到九个类，其中一个是抽象类。", BODY_TPL)
body(c, "（二）类图建模", HEAD_TPL)
body(c, "属性按可见性区分：账号、密码哈希设为受保护供子类继承，业务属性设为私有。关系上，"
        "用户与四类角色是继承；机器人与监测记录是组合，记录随采集产生、随清理消亡；"
        "监测记录触发紧急警报是单向关联；紧急警报与家属、医生之间是多对多；老人与视频通话是一对多。", BODY_TPL)
body(c, "（三）状态图建模", HEAD_TPL)
body(c, "机器人取待机、巡检、跟随、充电、紧急处理五个状态，以待机为中枢，巡检、跟随、紧急处理三个状态都回到待机，"
        "电量低于两成时从巡检或跟随转入充电。紧急警报取触发、通知、确认、处理、解决五个状态，"
        "主干为线性推进，另设两条分支：确认阶段判定为误报直接转入解决，处理阶段险情未解除则退回触发重新呼救。", BODY_TPL)
body(c, "（四）一致性验证", HEAD_TPL)
body(c, "按三条规则逐项核对：状态图中的每个状态名都能在类图中找到对应的状态属性；每条迁移的动作都能对应到类图中的一个操作；"
        "类图中的每个类至少出现在一条关系上，不留孤立类。核对中发现紧急警报类缺少解决操作，"
        "而状态图有解决状态，已在类图中补上。", BODY_TPL)

# ---------- 五、实验结果 ----------
c = t.rows[8].cells[0]
reset(c, keep=1)
body(c, "（1）类图。九个类，一处继承、一处组合、七处关联，关系均标注多重性，见图 1。", BODY_TPL)
pic(c, "01_类图_看护系统.png", 15.5, "图 1  空巢老人看护软件类图")
brk = c.add_paragraph()
brk.paragraph_format.first_line_indent = Pt(0)
brk.paragraph_format.space_before = Pt(0)
brk.paragraph_format.space_after = Pt(0)
brk.add_run().add_break(WD_BREAK.PAGE)
body(c, "（2）机器人状态图。五个状态、十一条迁移，待机为中枢状态，见图 2。", BODY_TPL)
pic(c, "02_状态图_机器人.png", 13.6, "图 2  机器人状态图")
body(c, "（3）紧急警报状态图。五个状态、九条迁移，含误报与再次呼救两条分支，见图 3。", BODY_TPL)
pic(c, "03_状态图_紧急警报.png", 7.2, "图 3  紧急警报状态图")
body(c, "（4）验证结果。两张状态图的十个状态分别落在机器人的运行状态属性和紧急警报的状态属性上；"
        "迁移动作中，电量低于 20%、电量达到 90%、收到紧急警报对应机器人类的回充、执行指令与自主跟随，"
        "触发、通知、确认、解决对应紧急警报类的同名操作。九个类均参与至少一条关系，无孤立类。", BODY_TPL)

# ---------- 六、问题与体会 ----------
c = t.rows[9].cells[0]
reset(c, keep=1)
body(c, "组合和关联容易混。机器人与监测记录是整体和部分的关系，记录离开机器人就没有意义，用实心菱形；"
        "机器人与老人只是配备关系，机器人撤走老人仍然存在，用普通关联。判断依据是部分能否独立于整体存在，"
        "而不是两者在业务上是否紧密。", BODY_TPL)
body(c, "迁移的命名一开始写成了状态描述，例如“检测到异常”，读图时分不清是谁检测、检测什么。"
        "改成事件加条件的写法后，例如“收到紧急警报”“电量低于 20%”，每条迁移都能直接落到类图的某个操作上，"
        "一致性检查也就变成了机械的对照工作。", BODY_TPL)

d.save(DOC)
print("saved", DOC)

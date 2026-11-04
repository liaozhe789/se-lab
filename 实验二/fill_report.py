# -*- coding: utf-8 -*-
"""填充实验二报告正文（v2：修缩进、去自动编号、图改两张）。"""
import os, copy
import docx
from docx.oxml.ns import qn
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.text.paragraph import Paragraph

BASE = r"C:\Users\qiyong\Desktop\实验报告\软件工程"
DOC = os.path.join(BASE, "240531142祁勇-实验二.docx")
DIA = os.path.join(BASE, "se-lab", "实验二", "diagrams")

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
set_cell(t.rows[3].cells[5], "2026年11月4日")

# 正文缩进模板：取自“实验目的”的正文段
BODY_TPL = t.rows[4].cells[0].paragraphs[1]

# ---------- 一、实验目的和要求 ----------
c = t.rows[4].cells[0]
reset(c, keep=1)
body(c, "（1）掌握用例图、顺序图、类图、状态图的核心要素与绘制方法，理解各图在需求分析阶段的分工。", BODY_TPL)
body(c, "（2）完成空巢老人看护软件的需求获取、分析与建模，输出一份结构完整、可供设计与验收使用的软件需求规格说明书。", BODY_TPL)

# ---------- 二、实验环境 ----------
c = t.rows[5].cells[0]
reset(c, keep=1)
body(c, "Windows 11 专业版；Python 3.13 与 python-docx；PlantUML 1.2024.7（JDK 25 运行）；Git 2.55.0；"
        "远程仓库 GitHub se-lab。", BODY_TPL, no_num=True)

# ---------- 三、实验内容 ----------
c = t.rows[6].cells[0]
reset(c, keep=1)
body(c, "（1）分组讨论需求，确定老人、家属、医生、机器人、时钟、管理员六个角色及其职责边界。", BODY_TPL)
body(c, "（2）梳理登录、视频语音交互、获取老人信息、自主跟随老人、提醒服务、控制机器人、监视老人、"
        "检测与通知异常状况、系统设置共十项功能。", BODY_TPL)
body(c, "（3）绘制系统整体用例图，并按功能内聚拆分为五个模块，逐模块绘制用例图与顺序图。", BODY_TPL)
body(c, "（4）补充类图与状态图，撰写软件需求规格说明书。", BODY_TPL)

# ---------- 四、实验步骤 ----------
c = t.rows[7].cells[0]
HEAD_TPL = c.paragraphs[1]
reset(c, keep=1)
body(c, "（一）需求获取", HEAD_TPL)
body(c, "从三类人员角色分别整理诉求：家属关心老人是否安全、有无异常，医生关心体征数据与历史记录，"
        "老人关心操作是否简单、能否一键联系家人。机器人负责采集数据与执行移动指令，时钟负责周期触发，"
        "二者不是人，但同样与系统交互，作为系统角色纳入参与者，最终得到六个参与者和十个用例。", BODY_TPL)
body(c, "（二）用例建模", HEAD_TPL)
body(c, "先画整体用例图划定系统边界，边界内是移动端、平台服务端与机器人终端三部分，边界外是六类参与者。"
        "再按功能内聚拆成用户与权限、视频语音交互、看护监控、机器人控制、定时提醒五个模块，逐模块画用例图。"
        "用例之间的包含与扩展关系在图上标注，例如监视老人包含获取老人信息与检测异常状况，"
        "自主跟随老人是控制机器人的扩展。", BODY_TPL)
body(c, "（三）顺序建模", HEAD_TPL)
body(c, "每个模块选一条主成功场景画顺序图，明确参与者、边界对象、控制对象与实体之间的消息顺序。"
        "异常分支用 alt 片段表达，例如登录的校验失败与通过、巡检的指标正常与越界。", BODY_TPL)
body(c, "（四）静态与状态建模", HEAD_TPL)
body(c, "用类图描述九个核心实体及其多重性关系，账户作为四类人员角色的公共父类；"
        "用状态图描述异常事件从检测到归档的六个状态，以及超时升级与自动关闭两条迁移。", BODY_TPL)
body(c, "（五）文档编写", HEAD_TPL)
body(c, "按 GB/T 8567 的结构撰写需求规格说明书，依次为引言、总体描述、功能需求、非功能需求、"
        "外部接口需求与验收标准，十三张图嵌入对应章节。", BODY_TPL)

# ---------- 五、实验结果 ----------
c = t.rows[8].cells[0]
reset(c, keep=1)
body(c, "（1）系统边界与角色定义。六个参与者，其中机器人与时钟为系统角色；"
        "系统边界限定在移动端应用、平台服务端与机器人终端三部分，不含医疗诊断功能。", BODY_TPL)
body(c, "（2）功能模型。十个用例分属五个模块，整体用例图见图 1。", BODY_TPL)
pic(c, "01_系统整体用例图.png", 15.0, "图 1  空巢老人看护软件系统用例图")
body(c, "（3）动态模型。五张顺序图覆盖登录、视频通话、异常检测与通知、机器人控制、定时提醒五条主流程，"
        "其中异常检测与通知的顺序图见图 2。", BODY_TPL)
pic(c, "09_顺序图_异常检测与通知.png", 12.6, "图 2  异常检测与通知顺序图")
body(c, "（4）静态模型与状态模型。九个实体类及其关系、异常事件的六个状态及迁移，"
        "见需求规格说明书的图 3-13 与图 3-8。", BODY_TPL)
body(c, "（5）交付文档。需求规格说明书共 13 页，含 13 张图、6 张表，覆盖六个角色、十个用例、"
        "五类非功能需求与五个对外接口。", BODY_TPL)

# ---------- 六、问题与体会 ----------
c = t.rows[9].cells[0]
reset(c, keep=1)
body(c, "第一个问题是包含与扩展容易混。包含是每次执行都必然调用的子流程，扩展是满足条件才发生的分支。"
        "本系统里检测异常状况是监视老人的包含用例，因为每次监视都要判定；"
        "自主跟随老人是控制机器人的扩展，因为只有家属选择跟随时才触发。分清楚之后，"
        "用例图上的虚线方向也就不会画反。", BODY_TPL)
body(c, "第二个问题是六个参与者放进一张用例图后连线交叉严重。试过让绘图工具自动布局，"
        "排出来的图角色散在四周、连线横穿用例，基本没法读。最后改成固定坐标手工排布，"
        "人员角色放左侧、系统角色放右侧、用例分两列，交叉明显减少，图也能直接印在 A4 上。", BODY_TPL)

d.save(DOC)
print("saved", DOC)

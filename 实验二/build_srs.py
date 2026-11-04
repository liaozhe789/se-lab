# -*- coding: utf-8 -*-
"""生成《空巢老人看护软件需求规格说明书》docx。"""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn

HERE = os.path.dirname(os.path.abspath(__file__))
DIA = os.path.join(HERE, "diagrams")
OUT = os.path.join(HERE, "空巢老人看护软件需求规格说明书.docx")

doc = Document()

# 页面
sec = doc.sections[0]
sec.page_width = Cm(21.0)
sec.page_height = Cm(29.7)
sec.left_margin = Cm(2.8)
sec.right_margin = Cm(2.6)
sec.top_margin = Cm(2.5)
sec.bottom_margin = Cm(2.5)

# 正文样式
st = doc.styles["Normal"]
st.font.name = "宋体"
st.font.size = Pt(10.5)
st.element.rPr.rFonts.set(qn("w:eastAsia"), "宋体")
st.paragraph_format.line_spacing = 1.5
st.paragraph_format.space_before = Pt(0)
st.paragraph_format.space_after = Pt(0)


def set_font(run, name="宋体", size=10.5, bold=False, color=None):
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    if color:
        run.font.color.rgb = color


def h(text, level=1):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(12 if level == 1 else 8)
    pf.space_after = Pt(6 if level == 1 else 4)
    pf.line_spacing = 1.5
    r = p.add_run(text)
    set_font(r, "黑体", {1: 15, 2: 13, 3: 11.5}.get(level, 11), bold=True)
    return p


def para(text, indent=True, size=10.5, spacing=1.5):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.line_spacing = spacing
    pf.space_after = Pt(3)
    if indent:
        pf.first_line_indent = Pt(size * 2)
    r = p.add_run(text)
    set_font(r, "宋体", size)
    return p


def bullet(text, size=10.5):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.left_indent = Pt(21)
    pf.first_line_indent = Pt(0)
    pf.line_spacing = 1.4
    pf.space_after = Pt(2)
    r = p.add_run(text)
    set_font(r, "宋体", size)
    return p


def figure(name, caption, width_cm=14.5):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.add_run().add_picture(os.path.join(DIA, name), width=Cm(width_cm))
    c = doc.add_paragraph()
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.paragraph_format.space_after = Pt(8)
    r = c.add_run(caption)
    set_font(r, "宋体", 9)


def table(headers, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(headers))
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, hd in enumerate(headers):
        cell = t.rows[0].cells[i]
        cell.text = ""
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(hd)
        set_font(r, "黑体", 9.5, bold=True)
    for row in rows:
        cells = t.add_row().cells
        for i, v in enumerate(row):
            cells[i].text = ""
            p = cells[i].paragraphs[0]
            p.paragraph_format.line_spacing = 1.2
            r = p.add_run(v)
            set_font(r, "宋体", 9)
    if widths:
        for row in t.rows:
            for i, w in enumerate(widths):
                row.cells[i].width = Cm(w)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


# ============ 封面 ============
for _ in range(3):
    doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("空巢老人看护软件")
set_font(r, "黑体", 26, bold=True)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("软件需求规格说明书")
set_font(r, "黑体", 22, bold=True)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.paragraph_format.space_before = Pt(10)
r = p.add_run("Software Requirements Specification")
set_font(r, "Times New Roman", 12)
r.font.color.rgb = RGBColor(0x59, 0x59, 0x59)

for _ in range(6):
    doc.add_paragraph()

info = [
    ("课程名称", "软件工程"),
    ("实验项目", "实验二  空巢老人看护软件需求分析"),
    ("专业班级", "2405311"),
    ("学　　号", "240531142"),
    ("姓　　名", "祁勇"),
    ("指导教师", "王春波"),
    ("编写日期", "2026 年 11 月 4 日"),
]
t = doc.add_table(rows=0, cols=2)
t.alignment = WD_TABLE_ALIGNMENT.CENTER
for k, v in info:
    cells = t.add_row().cells
    cells[0].width = Cm(3.2)
    cells[1].width = Cm(9.6)
    p0 = cells[0].paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p0.add_run(k + "：")
    set_font(r, "宋体", 12)
    p1 = cells[1].paragraphs[0]
    r = p1.add_run(v)
    set_font(r, "宋体", 11)

doc.add_page_break()

# ============ 1 引言 ============
h("1  引言", 1)

h("1.1  编写目的", 2)
para("本说明书面向空巢老人看护软件的设计、开发与验收环节，明确系统的角色边界、功能需求与非功能需求，"
     "作为后续概要设计、详细设计与测试用例编写的依据。预期读者为项目组开发人员、指导教师与验收人员。")

h("1.2  项目范围", 2)
para("系统由移动端应用、看护平台服务端、机器人终端三部分组成。移动端供老人、家属、医生与管理员使用，"
     "提供登录、视频语音通话、看护监控、机器人控制与提醒服务；服务端负责鉴权、数据存储、规则判定与消息推送；"
     "机器人终端负责采集老人的位置、姿态与生命体征数据，并执行移动与跟随指令。")
para("本期范围不含医疗诊断功能，系统只做异常识别与通知，不给出治疗建议；也不含第三方支付与电商模块。")

h("1.3  术语与缩写", 2)
table(
    ["术语", "含义"],
    [
        ["看护平台", "部署在云端的服务端系统，承担鉴权、存储、规则判定与推送"],
        ["机器人终端", "具备摄像头、麦克风与移动底盘的可移动设备，视为系统参与者"],
        ["时钟", "系统内部的定时触发装置，按周期触发巡检与提醒，视为系统参与者"],
        ["异常事件", "监测指标超出阈值后由系统生成的一条待处置记录"],
        ["SRS", "Software Requirements Specification，软件需求规格说明书"],
    ],
    widths=[4.0, 11.5],
)

h("1.4  参考资料", 2)
bullet("[1] GB/T 8567—2006  计算机软件文档编制规范")
bullet("[2] 教材《软件工程导论》第 5 章  需求分析与 UML 建模")
bullet("[3] OMG Unified Modeling Language Specification 2.5.1")

# ============ 2 总体描述 ============
h("2  总体描述", 1)

h("2.1  系统定位", 2)
para("系统面向独居或白天无人陪伴的老年人家庭。家属与医生通过手机随时了解老人状态，"
     "老人通过语音或视频与家属沟通，机器人承担室内巡视与跟随任务，"
     "系统在检测到跌倒、久卧不动、心率异常等情况时主动通知家属与签约医生。")

h("2.2  用户角色", 2)
para("系统共识别出六个参与者，其中四个为人员角色，两个为系统角色。")
table(
    ["角色", "类型", "职责与特征"],
    [
        ["老人", "人员", "系统的被看护对象，操作能力有限，以语音交互为主，界面需大字号、少层级"],
        ["家属", "人员", "老人的直系亲属，负责绑定老人、查看监测、接收告警、控制机器人"],
        ["医生", "人员", "签约社区医生，查看老人健康档案与异常记录，对异常事件给出处置结论"],
        ["管理员", "人员", "系统运维人员，维护账号、配置提醒规则与阈值参数"],
        ["机器人", "系统", "可移动终端，采集传感器数据，执行移动、跟随与转向指令"],
        ["时钟", "系统", "系统内部定时器，按周期触发巡检任务与定时提醒"],
    ],
    widths=[2.6, 2.0, 11.0],
)

h("2.3  假设与依赖", 2)
bullet("假设 1：老人家中有稳定的 Wi-Fi 覆盖，机器人可在室内自主移动。")
bullet("假设 2：家属与医生均持有可安装移动端应用的智能手机。")
bullet("假设 3：老人基础档案与健康数据在开户时由家属录入，医生可补充。")
bullet("依赖 1：短信或推送通道由第三方云服务提供。")
bullet("依赖 2：机器人硬件由合作厂商提供，其固件提供数据采集与指令执行的开放接口。")

h("2.4  约束", 2)
bullet("老人端界面必须支持纯语音操作，且在任何页面均可一键呼叫家属。")
bullet("涉及健康的个人数据须加密存储，传输使用 TLS 1.2 以上版本。")
bullet("系统须在 4G 网络下保持视频通话可用，最低带宽按 512 kbps 设计。")

# ============ 3 功能需求 ============
h("3  功能需求", 1)

h("3.1  系统整体用例模型", 2)
para("系统共抽象出十个用例，由六个参与者触发。用例之间的包含与扩展关系在图中标注："
     "视频语音交互包含用户登录，监视老人包含获取老人信息与检测异常状况，"
     "检测异常状况与提醒服务均包含通知异常状况，自主跟随老人是控制机器人的扩展。")
figure("01_系统整体用例图.png", "图 3-1  空巢老人看护软件系统用例图", 15.0)

h("3.2  用户与权限管理", 2)
para("本模块负责身份认证与参数配置。老人、家属、医生、管理员四类角色共用同一登录入口，"
     "登录成功后按角色加载不同的功能菜单；管理员在登录后可进入系统设置修改提醒规则、异常阈值与推送对象。")
figure("02_模块用例图_用户与权限.png", "图 3-2  用户与权限管理模块用例图", 12.5)
para("登录的交互过程如下：移动端提交账号密码，服务端查库并校验哈希，失败返回 401，成功签发访问令牌并回传角色。")
figure("07_顺序图_用户登录.png", "图 3-3  用户登录顺序图", 12.8)

h("3.3  视频语音交互", 2)
para("老人、家属、医生三方均可发起或接听通话。通话建立前必须完成登录，因此该用例包含用户登录。"
     "通话媒体流由机器人终端采集后经服务端转发，避免移动端之间直连失败。")
figure("03_模块用例图_视频语音交互.png", "图 3-4  视频语音交互模块用例图", 12.5)
figure("08_顺序图_视频语音交互.png", "图 3-5  视频语音交互顺序图", 12.8)

h("3.4  老人看护监控", 2)
para("本模块是系统的核心。时钟每 30 秒触发一次巡检，服务端向机器人索取心率、位置与姿态数据，"
     "按阈值判定是否异常；正常则落库为监测记录，异常则生成事件并推送家属与医生，家属确认后事件进入处置流程。")
figure("04_模块用例图_看护监控.png", "图 3-6  老人看护监控模块用例图", 13.5)
figure("09_顺序图_异常检测与通知.png", "图 3-7  异常检测与通知顺序图", 12.8)
para("异常事件在系统内部有明确的生命周期，从检测到归档共经历六个状态，"
     "超时未确认会自动升级或关闭，避免事件长期悬挂。")
figure("13_状态图_异常事件.png", "图 3-8  异常事件状态图", 8.8)

h("3.5  机器人控制", 2)
para("家属在获得控制权后可下发移动、转向、跟随等指令。控制权需校验家属与老人的绑定关系，"
     "校验通过后下发一次性控制令牌，防止越权操作。自主跟随是控制机器人的一种扩展模式，"
     "启动后机器人持续获取老人位置并保持安全距离。")
figure("05_模块用例图_机器人控制.png", "图 3-9  机器人控制模块用例图", 12.5)
figure("10_顺序图_控制机器人.png", "图 3-10  控制机器人顺序图", 12.8)

h("3.6  定时提醒", 2)
para("管理员为每位老人配置服药、饮水、作息等提醒任务。时钟到达提醒时刻后，服务端查询到期任务并推送，"
     "老人确认后标记完成并同步家属；超时未确认则二次推送并提醒家属关注。")
figure("06_模块用例图_定时提醒.png", "图 3-11  定时提醒模块用例图", 12.5)
figure("11_顺序图_定时提醒.png", "图 3-12  定时提醒顺序图", 12.8)

h("3.7  领域模型", 2)
para("系统的核心实体共九个。账户是四类人员角色的公共父类，家属与老人、医生与老人之间均为多对多关系，"
     "一名老人配备一台机器人，机器人采集的监测记录可触发零到一条异常事件，"
     "异常事件向家属广播，老人拥有多条提醒任务。")
figure("12_类图_领域模型.png", "图 3-13  领域模型类图", 15.5)

h("3.8  用例清单", 2)
table(
    ["编号", "用例名称", "主要参与者", "简要说明"],
    [
        ["UC01", "用户登录", "老人、家属、医生、管理员", "校验账号密码并签发令牌"],
        ["UC02", "视频/语音交互", "老人、家属、医生", "三方音视频通话，包含登录"],
        ["UC03", "监视老人", "家属", "按周期获取状态并判定异常"],
        ["UC04", "获取老人信息", "医生、机器人", "读取档案与实时体征"],
        ["UC05", "检测异常状况", "时钟", "按阈值规则判定是否异常"],
        ["UC06", "通知异常状况", "家属、医生", "推送告警并跟踪确认"],
        ["UC07", "自主跟随老人", "机器人", "保持距离跟随，扩展自控制机器人"],
        ["UC08", "控制机器人", "家属", "下发移动与转向指令"],
        ["UC09", "提醒服务", "老人、时钟", "定时播报提醒并记录确认"],
        ["UC10", "系统设置", "管理员", "配置阈值、提醒规则与推送对象"],
    ],
    widths=[1.6, 3.4, 4.6, 5.6],
)

# ============ 4 非功能需求 ============
h("4  非功能需求", 1)

h("4.1  性能需求", 2)
table(
    ["指标", "要求"],
    [
        ["告警时延", "从指标越界到家属收到推送不超过 5 秒"],
        ["视频首帧", "4G 网络下不超过 3 秒"],
        ["并发能力", "单节点支持 500 路并发视频会话"],
        ["巡检周期", "默认 30 秒，可由管理员在 10 至 120 秒之间调整"],
        ["页面响应", "移动端主要页面加载不超过 1.5 秒"],
    ],
    widths=[4.0, 11.5],
)

h("4.2  可靠性需求", 2)
bullet("服务端按双节点部署，单节点故障时自动切换，切换时间不超过 30 秒。")
bullet("监测数据本地缓存 10 分钟，网络中断恢复后补传，不丢数据。")
bullet("异常事件推送失败时按 1、5、15 分钟三次重试。")

h("4.3  安全性需求", 2)
bullet("密码使用加盐哈希存储，禁止明文与可逆加密。")
bullet("健康数据在数据库中字段级加密，密钥与数据分离存放。")
bullet("控制指令需携带一次性令牌，令牌有效期 5 分钟。")
bullet("所有接口做越权校验，家属只能访问已绑定老人的数据。")

h("4.4  易用性需求", 2)
bullet("老人端字号不小于 20 pt，主要按钮直径不小于 1.2 cm。")
bullet("老人端任一页面均可通过长按屏幕 2 秒呼出紧急呼叫。")
bullet("关键操作提供语音反馈，避免老人误触后无感知。")

h("4.5  可维护性需求", 2)
bullet("阈值、提醒规则、推送对象均通过配置下发，修改不需发版。")
bullet("服务端保留最近 90 天的调用日志，便于问题回溯。")

# ============ 5 外部接口 ============
h("5  外部接口需求", 1)

h("5.1  用户界面", 2)
para("移动端分四个角色视图：老人端为单页大按钮布局，家属端为监控看板布局，"
     "医生端为档案与事件列表布局，管理员端为配置表单布局。")

h("5.2  硬件接口", 2)
para("机器人终端通过 Wi-Fi 接入，向平台上报传感器数据，接收控制指令；"
     "摄像头与麦克风由机器人统一管理，移动端不直接连接设备。")

h("5.3  软件接口", 2)
table(
    ["接口", "方向", "说明"],
    [
        ["POST /api/login", "移动端 → 服务端", "账号密码登录，返回令牌与角色"],
        ["GET /api/elder/{id}/monitor", "移动端 → 服务端", "查询指定时段的监测记录"],
        ["POST /api/robot/{id}/command", "移动端 → 服务端", "下发机器人控制指令"],
        ["POST /api/event/{id}/confirm", "移动端 → 服务端", "确认异常事件"],
        ["POST /api/robot/report", "机器人 → 服务端", "上报传感器数据"],
    ],
    widths=[6.2, 4.6, 6.2],
)

h("5.4  通信接口", 2)
para("移动端与服务端之间使用 HTTPS，媒体流使用 WebRTC，推送使用第三方推送服务的 HTTP 接口。")

# ============ 6 验收标准 ============
h("6  验收标准", 1)
bullet("六个角色的用例全部可在测试环境走通，无阻塞性缺陷。")
bullet("模拟心率越界后，家属端在 5 秒内收到推送，事件状态按状态图流转。")
bullet("断开网络 10 分钟后恢复，监测数据补传完整。")
bullet("家属账号访问未绑定老人的数据时被拒绝，返回 403。")

# ============ 附录 ============
h("附录 A  建模工具说明", 1)
para("本说明书中的用例图由 Python 脚本按坐标绘制，顺序图、类图与状态图由 PlantUML 生成，"
     "均为标准 UML 2.x 画法。源文件与图片保存在仓库 se-lab/实验二/diagrams 目录下，可重新生成。")

doc.save(OUT)
print("saved", OUT)

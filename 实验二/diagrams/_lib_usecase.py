# -*- coding: utf-8 -*-
"""用例图绘制工具：按给定坐标精确排版，输出 PNG。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch, Rectangle
import matplotlib.font_manager as fm

FONT = "Microsoft YaHei"
plt.rcParams["font.sans-serif"] = [FONT, "SimHei"]
plt.rcParams["axes.unicode_minus"] = False

BLUE = "#2E6DA4"
FILL = "#EAF3FB"
GREY = "#555555"


def stick_figure(ax, x, y, label, scale=1.0):
    """在 (x, y) 处画火柴人，y 为脚底位置。"""
    s = scale
    head_r = 1.15 * s
    head_y = y + 7.2 * s
    ax.add_patch(Ellipse((x, head_y), head_r * 2, head_r * 2,
                         fill=False, ec=GREY, lw=1.3, zorder=5))
    ax.plot([x, x], [y + 4.0 * s, head_y - head_r], color=GREY, lw=1.3, zorder=5)
    ax.plot([x - 1.8 * s, x + 1.8 * s], [y + 5.0 * s, y + 5.0 * s], color=GREY, lw=1.3, zorder=5)
    ax.plot([x, x - 1.6 * s], [y + 4.0 * s, y], color=GREY, lw=1.3, zorder=5)
    ax.plot([x, x + 1.6 * s], [y + 4.0 * s, y], color=GREY, lw=1.3, zorder=5)
    ax.text(x, y - 1.6 * s, label, ha="center", va="top", fontsize=10.5,
            color="#222222", linespacing=1.35, zorder=6)


def draw(actors, usecases, links, rels, box, title, out, figsize=(11.6, 7.6),
         uc_w=8.6, uc_h=3.3, note=None, box_label="空巢老人看护软件"):
    fig, ax = plt.subplots(figsize=figsize, dpi=170)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")

    if box:
        x0, y0, x1, y1 = box
        ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, fill=False,
                               ec=BLUE, lw=1.4, zorder=1))
        ax.text(x0 + 1.6, y1 - 1.2, box_label, ha="left", va="top",
                fontsize=10.5, color="#1F4E79", zorder=6)

    for key, (x, y, label) in actors.items():
        stick_figure(ax, x, y - 4, label)

    uc_pos = {}
    for key, (x, y, label) in usecases.items():
        ax.add_patch(Ellipse((x, y), uc_w * 2, uc_h * 2, facecolor=FILL,
                             edgecolor=BLUE, lw=1.2, zorder=3))
        ax.text(x, y, label, ha="center", va="center", fontsize=10.5,
                color="#1A1A1A", linespacing=1.3, zorder=4)
        uc_pos[key] = (x, y)

    def edge_point(p_from, p_to, w, h):
        """求椭圆边界上的交点。"""
        import math
        dx, dy = p_to[0] - p_from[0], p_to[1] - p_from[1]
        if dx == 0 and dy == 0:
            return p_from
        t = 1.0 / math.sqrt((dx / w) ** 2 + (dy / h) ** 2)
        return (p_from[0] + dx * t, p_from[1] + dy * t)

    for a, u in links:
        ax0, ay0, _ = actors[a]
        ay = ay0 - 4 + 4.5
        ux, uy = uc_pos[u]
        p1 = (ax0, ay)
        p2 = edge_point((ux, uy), p1, uc_w, uc_h)
        # 从角色一侧再缩一点，避免压住火柴人
        import math
        dx, dy = p2[0] - p1[0], p2[1] - p1[1]
        n = math.hypot(dx, dy) or 1
        p1s = (p1[0] + dx / n * 2.2, p1[1] + dy / n * 2.2)
        ax.add_patch(FancyArrowPatch(p1s, p2, arrowstyle="-", color=GREY, lw=1.0,
                                     shrinkA=0, shrinkB=0, zorder=2))

    for a, b, kind in rels:
        pa, pb = uc_pos[a], uc_pos[b]
        p2 = edge_point(pb, pa, uc_w, uc_h)
        p1 = edge_point(pa, pb, uc_w, uc_h)
        style = "-|>" if kind == "include" else "-|>"
        ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, color=BLUE, lw=1.0,
                                     linestyle=(0, (4, 3)), mutation_scale=11,
                                     shrinkA=1, shrinkB=1,
                                     connectionstyle="arc3,rad=0.12", zorder=2))
        mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
        if abs(p2[0] - p1[0]) < 4:
            ax.text(mx + 1.8, my, "«%s»" % kind, ha="left", va="center",
                    fontsize=9.5, color=BLUE, zorder=6)
        else:
            ax.text(mx, my + 1.3, "«%s»" % kind, ha="center", va="bottom",
                    fontsize=9.5, color=BLUE, zorder=6)

    if note:
        nx, ny, text = note
        ax.text(nx, ny, text, ha="left", va="top", fontsize=9.5, color="#444444",
                bbox=dict(boxstyle="round,pad=0.4", fc="#FFFDF0", ec="#D9C86B", lw=0.9),
                zorder=6)

    if title:
        ax.set_title(title, fontsize=13, color="#1F4E79", pad=6)
    fig.tight_layout(pad=0.4)
    fig.savefig(out, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("saved", out)

#!/usr/bin/env python3
"""
远程伤害模拟器 —— 拖动滑块，实时看命中率 & 伤害分布

完整链路：
  impact = bow_dmg + arrow_amount
  dispersion = U(dex) + U(skill_penalty) + N(weapon_disp)
  missed_by = iso_tangent(dispersion, range) / target_size
  goodhit = missed_by + dodge
  → 决定 damage_mult 区间
  → 护甲减法 → constant_damage_multiplier
"""

import tkinter as tk
from tkinter import ttk
import math
# 只用 math.erf 替代 scipy.stats.norm.cdf，零依赖
def _norm_cdf(x):
    """标准正态累积分布"""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

# ── 数学工具 ──────────────────────────────────────────────

def iso_tangent(distance: float, dispersion_arcmin: float) -> float:
    """missed_by_tiles, 与 C++ iso_tangent 等价的连续版本"""
    rad = dispersion_arcmin / 60.0 * math.pi / 180.0  # arcmin → rad
    return math.tan(rad / 2.0) * distance * 2.0


def missed_by_to_goodhit(missed_by: float, dodge: float) -> float:
    return min(missed_by + dodge, 2.0)


def damage_mult_for_goodhit(goodhit: float, crit_mult: float, crit_mod: float) -> float:
    """返回 damage_mult 中值（取随机区间的中点）"""
    std_hit = math.sqrt(2.0 * crit_mult)
    if goodhit >= 1.0:
        return 0.0  # miss
    elif goodhit < 0.1:  # HEADSHOT
        r1 = 0.5 + 0.45 * crit_mod
        r2 = 0.75 + 0.3 * crit_mod
        first = (r1 + r2) / 2.0
        second = std_hit + (crit_mult - std_hit) * crit_mod
        return first * second
    elif goodhit < 0.2:  # CRITICAL
        first = (0.75 + 1.0) / 2.0
        second = std_hit + (crit_mult - std_hit) * crit_mod
        return first * second
    elif goodhit < 0.5:  # GOOD HIT
        first = (0.5 + 0.75) / 2.0
        return first * std_hit
    elif goodhit < 0.8:  # STANDARD
        return (0.5 + 1.0) / 2.0
    else:  # GRAZING
        return (0.0 + 0.25) / 2.0


def damage_mult_range_for_interval(interval: str, crit_mult: float, crit_mod: float) -> tuple:
    """返回 (min, max, mid) damage_mult"""
    std_hit = math.sqrt(2.0 * crit_mult)
    second_hs_crit = std_hit + (crit_mult - std_hit) * crit_mod

    ranges = {
        "HEADSHOT": (0.95 * second_hs_crit, 1.05 * second_hs_crit),
        "CRITICAL": (0.75 * second_hs_crit, 1.0 * second_hs_crit),
        "GOOD HIT": (0.5 * std_hit, 0.75 * std_hit),
        "STANDARD":  (0.5, 1.0),
        "GRAZING":   (0.0, 0.25),
    }
    lo, hi = ranges[interval]
    return lo, hi, (lo + hi) / 2.0


# ── 模型 ──────────────────────────────────────────────────

def calc_dispersion_params(
    skill: float,
    json_dispersion: float,
    skill_constant: float,
    dispersion_divider: float,
    dex: float = 10.0,
) -> tuple:
    """
    返回 total dispersion 的 (mean, stddev)
    模拟 C++ dispersion_sources.roll() 的分布
    """
    # weapon_dispersion → normal_source (被 N 取用)
    w_disp = json_dispersion / dispersion_divider  # gun_dispersion() 返回值

    # ranged_dex_mod → linear_source
    dex_penalty = max((20.0 - dex) * 0.5, 0.0)
    dex_mean = dex_penalty / 2.0
    dex_var = dex_penalty ** 2 / 12.0

    # dispersion_from_skill → linear_source
    wc = skill_constant / dispersion_divider  # 传给 disp_from_skill 的 weapon_dispersion
    if skill >= 10:
        skill_penalty = 0.0
    elif skill >= 5:
        shortfall = 10.0 - skill
        skill_penalty = 10.0 * shortfall + wc * shortfall * 1.25 / 5.0
    else:
        shortfall = 10.0 - skill
        pre_short = 5.0 - skill
        skill_penalty = 10.0 * shortfall + wc * (1.25 + pre_short * 10.0 / 5.0)
    skill_mean = skill_penalty / 2.0
    skill_var = skill_penalty ** 2 / 12.0

    # normal_source: rng_normal(w_disp) → truncated normal, mean≈w_disp/2, std≈w_disp/4
    normal_mean = w_disp / 2.0
    normal_std = w_disp / 4.0

    total_mean = dex_mean + skill_mean + normal_mean
    total_var = dex_var + skill_var + normal_std ** 2
    total_std = math.sqrt(total_var)

    return total_mean, total_std


def hit_quality_probabilities(
    mean: float, std: float, target_size: float, range_tiles: float, dodge: float
) -> dict:
    """返回各命中品质 + miss 的概率"""
    # goodhit = missed_by + dodge
    # missed_by ≈ disp × range / (3437.7 × target_size)  (精确用 iso_tangent)
    # 对于概率计算，反求 disp 阈值

    def disp_for_goodhit(gh: float) -> float:
        """goodhit=gh 对应的 dispersion 阈值 (二分求解)"""
        if gh <= dodge:
            return 0.0
        target_mb = gh - dodge  # 需要的 missed_by
        # 二分求解 iso_tangent(disp) / target_size = target_mb
        lo, hi = 0.0, 2000.0
        for _ in range(50):
            mid = (lo + hi) / 2.0
            mb = iso_tangent(range_tiles, mid)
            if target_size > 0:
                mb /= target_size
            if mb < target_mb:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2.0

    thresholds = {
        "HEADSHOT": disp_for_goodhit(0.1),
        "CRITICAL": disp_for_goodhit(0.2),
        "GOOD HIT": disp_for_goodhit(0.5),
        "STANDARD": disp_for_goodhit(0.8),
        "GRAZING": disp_for_goodhit(1.0),
    }

    # 用正态近似计算累积概率
    cdf = lambda x: _norm_cdf((x - mean) / std) if std > 0 else (1.0 if x >= mean else 0.0)

    probs = {}
    probs["HEADSHOT"] = cdf(thresholds["HEADSHOT"])
    probs["CRITICAL"] = max(0, cdf(thresholds["CRITICAL"]) - cdf(thresholds["HEADSHOT"]))
    probs["GOOD HIT"] = max(0, cdf(thresholds["GOOD HIT"]) - cdf(thresholds["CRITICAL"]))
    probs["STANDARD"] = max(0, cdf(thresholds["STANDARD"]) - cdf(thresholds["GOOD HIT"]))
    probs["GRAZING"] = max(0, cdf(thresholds["GRAZING"]) - cdf(thresholds["STANDARD"]))
    probs["MISS"] = 1.0 - cdf(thresholds["GRAZING"])
    return probs


# ── GUI ───────────────────────────────────────────────────

class RangedDamageSimulator:
    def __init__(self, root):
        self.root = root
        root.title("Cataclysm-Medieval 远程伤害模拟器")
        root.geometry("1200x850")

        # ── 参数默认值 ──
        self.params = {
            # 武器/弹药
            "bow_dmg":             tk.DoubleVar(value=6.0),
            "arrow_amount":        tk.DoubleVar(value=0.0),
            "arrow_cdm":           tk.DoubleVar(value=1.0),   # constant_damage_multiplier
            "arrow_arpen":         tk.DoubleVar(value=3.0),
            "arrow_crit_mult":     tk.DoubleVar(value=10.0),
            # 系统参数
            "json_dispersion":     tk.DoubleVar(value=150.0),
            "skill_constant":      tk.DoubleVar(value=60.0),
            "dispersion_divider":  tk.DoubleVar(value=15.0),
            # 角色
            "skill":               tk.DoubleVar(value=10.0),
            "dex":                 tk.DoubleVar(value=10.0),
            # 场景
            "range":               tk.DoubleVar(value=8.0),
            "target_armor":        tk.DoubleVar(value=0.0),
            "target_hp":           tk.DoubleVar(value=75.0),
            "target_size":         tk.DoubleVar(value=0.5),
            "dodge":               tk.DoubleVar(value=0.0),
            # crit_mod (目标护甲覆盖率)
            "crit_mod":            tk.DoubleVar(value=1.0),
        }

        self._build_ui()
        self._update()

    def _build_ui(self):
        main = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main.pack(fill=tk.BOTH, expand=True)

        # ── 左侧：参数面板 ──
        left = ttk.Frame(main, width=420)
        main.add(left, weight=1)

        canvas = tk.Canvas(left, highlightthickness=0)
        scrollbar = ttk.Scrollbar(left, orient=tk.VERTICAL, command=canvas.yview)
        scroll_frame = ttk.Frame(canvas)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # 鼠标滚轮
        canvas.bind("<Enter>", lambda e: canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*e.delta/60), "units")))
        canvas.bind("<Leave>", lambda e: canvas.unbind_all("<MouseWheel>"))

        self._add_slider_group(scroll_frame, "🎯 武器 & 弹药", [
            ("长弓基础伤害", "bow_dmg", 1, 20, 1),
            ("箭 damage.amount", "arrow_amount", 0, 15, 1),
            ("箭 constant_dmg_mult", "arrow_cdm", 0.1, 3.0, 0.1),
            ("箭 armor_penetration", "arrow_arpen", 0, 20, 1),
            ("箭 critical_multiplier", "arrow_crit_mult", 2, 15, 1),
        ])

        self._add_slider_group(scroll_frame, "⚙️ 系统常量", [
            ("JSON dispersion (武器)", "json_dispersion", 10, 1500, 10),
            ("Archery 技能常数 (C++)", "skill_constant", 10, 500, 10),
            ("DISPERSION_DIVIDER", "dispersion_divider", 1, 30, 1),
        ])

        self._add_slider_group(scroll_frame, "👤 角色", [
            ("技能等级", "skill", 0, 10, 1),
            ("敏捷 DEX", "dex", 4, 20, 1),
        ])

        self._add_slider_group(scroll_frame, "🎪 场景", [
            ("距离 (格)", "range", 1, 30, 1),
            ("目标护甲 (stab)", "target_armor", 0, 30, 1),
            ("目标 HP", "target_hp", 20, 300, 5),
            ("目标体型", "target_size", 0.2, 1.5, 0.1),
            ("闪避因子", "dodge", 0.0, 1.0, 0.05),
        ])

        self._add_slider_group(scroll_frame, "🛡️ 暴击因子", [
            ("crit_mod (0=铁罐 1=裸体)", "crit_mod", 0.0, 1.0, 0.05),
        ])

        ttk.Button(scroll_frame, text="重置默认值", command=self._reset).pack(pady=10)

        # ── 右侧：输出面板 ──
        right = ttk.Frame(main, width=750)
        main.add(right, weight=3)

        # 摘要行
        self.summary_var = tk.StringVar()
        ttk.Label(right, textvariable=self.summary_var,
                  font=("Courier", 11), justify=tk.LEFT).pack(pady=5, anchor=tk.W)

        # Canvas 绘制柱状图
        self.chart_canvas = tk.Canvas(right, height=200, bg="white", highlightthickness=1)
        self.chart_canvas.pack(fill=tk.X, padx=5, pady=5)

        # 伤害表
        self.dmg_text = tk.Text(right, height=18, font=("Courier", 10), state=tk.DISABLED)
        self.dmg_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def _add_slider_group(self, parent, title, sliders):
        frame = ttk.LabelFrame(parent, text=title, padding=5)
        frame.pack(fill=tk.X, padx=5, pady=3)

        for label, key, lo, hi, step in sliders:
            row = ttk.Frame(frame)
            row.pack(fill=tk.X, pady=1)
            ttk.Label(row, text=label, width=24).pack(side=tk.LEFT)

            val = self.params[key]
            display_var = tk.StringVar()

            def make_cmd(k, dv, fmt):
                def cmd(v):
                    dv.set(float(v))
                    display_var.set(fmt.format(float(v)))
                    self._update()
                return cmd

            if isinstance(step, int) or step == int(step):
                fmt = "{:.0f}"
            elif step >= 0.1:
                fmt = "{:.1f}"
            else:
                fmt = "{:.2f}"

            scale = ttk.Scale(row, from_=lo, to=hi, variable=val,
                              command=make_cmd(key, val, fmt),
                              length=160)

            # 初始化显示
            display_var.set(fmt.format(val.get()))

            ttk.Label(row, textvariable=display_var, width=6).pack(side=tk.RIGHT)
            scale.pack(side=tk.RIGHT, fill=tk.X, expand=True)

    def _reset(self):
        defaults = {
            "bow_dmg": 6.0, "arrow_amount": 0.0, "arrow_cdm": 1.0,
            "arrow_arpen": 3.0, "arrow_crit_mult": 10.0,
            "json_dispersion": 150.0, "skill_constant": 60.0, "dispersion_divider": 15.0,
            "skill": 10.0, "dex": 10.0,
            "range": 8.0, "target_armor": 0.0, "target_hp": 75.0,
            "target_size": 0.5, "dodge": 0.0, "crit_mod": 1.0,
        }
        for k, v in defaults.items():
            self.params[k].set(v)
        self._update()

    def _update(self, *args):
        p = {k: v.get() for k, v in self.params.items()}

        # ── dispersion ──
        disp_mean, disp_std = calc_dispersion_params(
            p["skill"], p["json_dispersion"],
            p["skill_constant"], p["dispersion_divider"],
            p["dex"]
        )

        # ── 概率 ──
        probs = hit_quality_probabilities(
            disp_mean, disp_std, p["target_size"], p["range"], p["dodge"]
        )

        # ── 伤害计算 ──
        impact = p["bow_dmg"] + p["arrow_amount"]
        crit_mult = p["arrow_crit_mult"]
        crit_mod = p["crit_mod"]
        eff_armor = max(0.0, p["target_armor"] - p["arrow_arpen"])
        cdm = p["arrow_cdm"]
        target_hp = p["target_hp"]

        intervals = ["HEADSHOT", "CRITICAL", "GOOD HIT", "STANDARD", "GRAZING"]
        results = []
        total_kill_prob = 0.0  # P(伤害 ≥ HP)

        for interval in intervals:
            lo, hi, mid = damage_mult_range_for_interval(interval, crit_mult, crit_mod)
            pre_armor_lo = impact * lo
            pre_armor_hi = impact * hi
            pre_armor_mid = impact * mid
            post_armor_lo = max(0.0, pre_armor_lo - eff_armor)
            post_armor_hi = max(0.0, pre_armor_hi - eff_armor)
            post_armor_mid = max(0.0, pre_armor_mid - eff_armor)
            final_lo = post_armor_lo * cdm
            final_hi = post_armor_hi * cdm
            final_mid = post_armor_mid * cdm

            # 该区间内的 kill 概率近似：(区间内 >HP 的比例)
            prob_this = probs.get(interval, 0)
            if final_hi > final_lo and prob_this > 0:
                kill_frac = max(0.0, min(1.0, (final_hi - target_hp) / (final_hi - final_lo)))
            else:
                kill_frac = 1.0 if final_lo >= target_hp else 0.0
            total_kill_prob += prob_this * kill_frac

            avg_dmg_in_interval = final_mid
            results.append((interval, prob_this, lo, hi, final_lo, final_hi, avg_dmg_in_interval))

        # 平均伤害（考虑概率加权）
        avg_dmg = sum(r[6] * r[1] for r in results)
        hit_prob = 1.0 - probs.get("MISS", 0)

        # ── 更新 UI ──
        # 摘要
        self.summary_var.set(
            f"dispersion: μ={disp_mean:.1f} σ={disp_std:.1f} arcmin  |  "
            f"impact: {impact:.0f}  |  "
            f"命中率: {hit_prob*100:.1f}%  |  "
            f"秒杀率: {total_kill_prob*100:.1f}%  |  "
            f"平均伤害/箭: {avg_dmg:.1f}"
        )

        # 柱状图
        self._draw_chart(probs, total_kill_prob, hit_prob)

        # 伤害表
        self._draw_damage_table(results, impact, eff_armor, cdm, target_hp, avg_dmg, hit_prob, total_kill_prob)

    def _draw_chart(self, probs, kill_prob, hit_prob):
        c = self.chart_canvas
        c.delete("all")
        w = c.winfo_width()
        h = c.winfo_height()
        if w < 100 or h < 50:
            return

        intervals = ["HEADSHOT", "CRITICAL", "GOOD HIT", "STANDARD", "GRAZING", "MISS"]
        colors = ["#e74c3c", "#e67e22", "#f1c40f", "#2ecc71", "#95a5a6", "#34495e"]
        labels = ["HEAD", "CRIT", "GOOD", "STD", "GRAZE", "MISS"]

        margin_l, margin_r = 60, 20
        margin_t, margin_b = 20, 30
        bar_w = (w - margin_l - margin_r) / len(intervals) * 0.7
        gap = (w - margin_l - margin_r) / len(intervals) * 0.3

        max_y = max(probs.values()) * 1.15 if probs else 0.5
        chart_h = h - margin_t - margin_b

        for i, (interval, color, label) in enumerate(zip(intervals, colors, labels)):
            prob = probs.get(interval, 0)
            x0 = margin_l + i * (bar_w + gap)
            x1 = x0 + bar_w
            bar_top = margin_t + chart_h * (1.0 - prob / max_y) if max_y > 0 else margin_t
            y0 = margin_t + chart_h
            y1 = bar_top

            c.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
            # 百分比标签
            pct_text = f"{prob*100:.0f}%"
            c.create_text((x0 + x1) / 2, y1 - 10, text=pct_text,
                          fill="white" if prob > 0.08 else "black",
                          font=("Helvetica", 9, "bold"))
            # 底部标签
            c.create_text((x0 + x1) / 2, y0 + 15, text=label,
                          font=("Helvetica", 8))

        # kill prob 线
        kill_y = margin_t + chart_h * (1.0 - kill_prob) if max_y > 0 else margin_t
        c.create_line(margin_l, kill_y, w - margin_r, kill_y, fill="red", dash=(5, 3), width=2)
        c.create_text(w - margin_r - 30, kill_y - 8, text=f"秒杀 {kill_prob*100:.0f}%",
                      fill="red", font=("Helvetica", 8, "bold"), anchor=tk.E)

    def _draw_damage_table(self, results, impact, eff_armor, cdm, target_hp, avg_dmg, hit_prob, kill_prob):
        self.dmg_text.config(state=tk.NORMAL)
        self.dmg_text.delete("1.0", tk.END)

        lines = []
        lines.append(f"{'命中品质':<12} {'概率':>7} {'dmg_mult':>12} {'伤害范围':>14} {'中值':>6}")
        lines.append("-" * 55)

        for interval, prob, mult_lo, mult_hi, dmg_lo, dmg_hi, dmg_mid in results:
            mult_str = f"{mult_lo:.2f}–{mult_hi:.2f}" if mult_lo != mult_hi else f"{mult_lo:.2f}"
            dmg_str = f"{dmg_lo:.0f}–{dmg_hi:.0f}" if abs(dmg_hi - dmg_lo) > 0.5 else f"{dmg_lo:.0f}"
            kill_marker = " 💀" if dmg_mid >= target_hp else ""
            lines.append(
                f"{interval:<12} {prob*100:>6.1f}% {mult_str:>12} {dmg_str:>14} {dmg_mid:>5.0f}{kill_marker}"
            )

        lines.append("-" * 55)
        lines.append(f"impact: {impact:.0f} | 有效护甲: {eff_armor:.0f} | cdm: {cdm:.2f} | 目标HP: {target_hp:.0f}")
        lines.append(f"命中率: {hit_prob*100:.1f}% | 秒杀率: {kill_prob*100:.1f}% | 平均伤害: {avg_dmg:.1f}")

        self.dmg_text.insert("1.0", "\n".join(lines))
        self.dmg_text.config(state=tk.DISABLED)


# ── CLI ───────────────────────────────────────────────────

def _cli_single(params: dict) -> str:
    """单组参数计算，返回格式化字符串"""
    disp_mean, disp_std = calc_dispersion_params(
        params["skill"], params["json_dispersion"],
        params["skill_constant"], params["dispersion_divider"],
        params["dex"]
    )
    probs = hit_quality_probabilities(
        disp_mean, disp_std, params["target_size"], params["range"], params["dodge"]
    )
    impact = params["bow_dmg"] + params["arrow_amount"]
    crit_mult = params["arrow_crit_mult"]
    crit_mod = params["crit_mod"]
    eff_armor = max(0.0, params["target_armor"] - params["arrow_arpen"])
    cdm = params["arrow_cdm"]
    target_hp = params["target_hp"]

    intervals = ["HEADSHOT", "CRITICAL", "GOOD HIT", "STANDARD", "GRAZING"]
    lines = []
    lines.append(f"  impact={impact:.0f}  crit_mult={crit_mult:.0f}  crit_mod={crit_mod:.2f}  "
                 f"eff_armor={eff_armor:.0f}  cdm={cdm:.2f}  HP={target_hp:.0f}")
    lines.append(f"  dispersion μ={disp_mean:.1f} σ={disp_std:.1f} arcmin")
    def _fmt_prob(p: float) -> str:
        if p > 0.9995: return " ~100%"
        if p < 0.0005: return "   ~0%"
        return f"{p*100:>5.1f}%"

    lines.append(f"  {'Quality':<12} {'Prob':>7}  {'dmg_mult':>10}  {'dmg_range':>12}  {'mid':>5}")
    lines.append(f"  {'-'*50}")

    total_kill = 0.0
    avg_dmg = 0.0
    for interval in intervals:
        lo, hi, mid = damage_mult_range_for_interval(interval, crit_mult, crit_mod)
        dmg_lo = max(0.0, impact * lo - eff_armor) * cdm
        dmg_hi = max(0.0, impact * hi - eff_armor) * cdm
        dmg_mid = max(0.0, impact * mid - eff_armor) * cdm
        prob = probs.get(interval, 0)
        avg_dmg += dmg_mid * prob
        kill_frac = max(0.0, min(1.0, (dmg_hi - target_hp) / (dmg_hi - dmg_lo))) if dmg_hi > dmg_lo else (1.0 if dmg_lo >= target_hp else 0.0)
        total_kill += prob * kill_frac
        dmg_str = f"{dmg_lo:.0f}-{dmg_hi:.0f}" if abs(dmg_hi - dmg_lo) > 0.5 else f"{dmg_lo:.0f}"
        marker = " 💀" if dmg_mid >= target_hp else ""
        lines.append(f"  {interval:<12} {_fmt_prob(prob):>7}  {lo:.2f}-{hi:<6.2f}  {dmg_str:>12}  {dmg_mid:>5.0f}{marker}")

    hit_p = 1.0 - probs.get("MISS", 0)
    lines.append(f"  {'-'*50}")
    lines.append(f"  命中率: {hit_p*100:.1f}%  秒杀率: {total_kill*100:.1f}%  均伤: {avg_dmg:.1f}")
    return "\n".join(lines)


def _cli_compare_skills(params: dict):
    print("═" * 55)
    print(f"  长弓 {params['bow_dmg']:.0f}dmg + broadhead箭 (cdm={params['arrow_cdm']})  "
          f"disp={params['json_dispersion']:.0f}  距离{params['range']:.0f}格  无甲\n")
    for skill, label in [(3, "入门"), (5, "熟练"), (10, "精英")]:
        p = dict(params)
        p["skill"] = skill
        print(f"── {label} (skill={skill}) ──")
        print(_cli_single(p))
        print()


def _cli_compare_ranges(params: dict):
    print("═" * 55)
    print(f"  长弓 {params['bow_dmg']:.0f}dmg + broadhead箭  skill={params['skill']:.0f}  无甲\n")
    for rng in [4, 8, 12, 16, 20]:
        p = dict(params)
        p["range"] = rng
        print(f"── {rng} 格 ──")
        print(_cli_single(p))
        print()


def _cli_compare_weapons(params: dict):
    print("═" * 55)
    print(f"  skill={params['skill']:.0f}  bodkin箭  距离{params['range']:.0f}格  无甲\n")
    weapons = [
        ("生存弓", 1, 300), ("短弓", 4, 200),
        ("长弓", 6, 150), ("巨弓", 11, 120),
        ("手弩", 3, 100), ("木弩", 4, 80), ("复合弩", 13, 60),
    ]
    for name, dmg, disp in weapons:
        p = dict(params)
        p["bow_dmg"] = dmg
        p["json_dispersion"] = disp
        p["arrow_cdm"] = 1.0  # bodkin
        print(f"── {name} (dmg={dmg}, disp={disp}) ──")
        print(_cli_single(p))
        print()


def _cli_sweep(params: dict, var: str, values: list[float]):
    print("═" * 55)
    print(f"  扫描 {var}:\n")
    header = f"  {'Value':>6}  {'HEAD':>6}  {'CRIT':>6}  {'GOOD':>6}  {'MISS':>6}  {'kill%':>6}  {'avg_dmg':>7}"
    print(header)
    print(f"  {'-'*55}")
    for val in values:
        p = dict(params)
        p[var] = val
        disp_mean, disp_std = calc_dispersion_params(
            p["skill"], p["json_dispersion"],
            p["skill_constant"], p["dispersion_divider"], p["dex"]
        )
        probs = hit_quality_probabilities(disp_mean, disp_std, p["target_size"], p["range"], p["dodge"])
        impact = p["bow_dmg"] + p["arrow_amount"]
        crit_mult = p["arrow_crit_mult"]
        crit_mod = p["crit_mod"]
        eff_armor = max(0.0, p["target_armor"] - p["arrow_arpen"])
        cdm = p["arrow_cdm"]
        hp = p["target_hp"]
        total_kill = 0.0
        avg_dmg = 0.0
        for interval in ["HEADSHOT", "CRITICAL", "GOOD HIT", "STANDARD", "GRAZING"]:
            lo, hi, mid = damage_mult_range_for_interval(interval, crit_mult, crit_mod)
            dmg_lo = max(0.0, impact * lo - eff_armor) * cdm
            dmg_hi = max(0.0, impact * hi - eff_armor) * cdm
            dmg_mid = max(0.0, impact * mid - eff_armor) * cdm
            prob = probs.get(interval, 0)
            avg_dmg += dmg_mid * prob
            kill_frac = max(0.0, min(1.0, (dmg_hi - hp) / (dmg_hi - dmg_lo))) if dmg_hi > dmg_lo else (1.0 if dmg_lo >= hp else 0.0)
            total_kill += prob * kill_frac
        hs = probs.get("HEADSHOT", 0) * 100
        crit = probs.get("CRITICAL", 0) * 100
        good = probs.get("GOOD HIT", 0) * 100
        miss = probs.get("MISS", 0) * 100
        def _f(p: float) -> str:
            if p > 99.95: return " ~100%"
            if p < 0.05: return "   ~0%"
            return f"{p:>5.1f}%"
        print(f"  {val:>6.0f}  {_f(hs):>6}  {_f(crit):>6}  {_f(good):>6}  {_f(miss):>6}  {_f(total_kill*100):>6}  {avg_dmg:>7.1f}")


def _cli_main():
    import argparse
    ap = argparse.ArgumentParser(description="Cataclysm-Medieval 远程伤害计算器")
    ap.add_argument("--cli", action="store_true", help="命令行模式")
    ap.add_argument("--compare-skills", action="store_true", help="对比入门/熟练/精英")
    ap.add_argument("--compare-ranges", action="store_true", help="对比不同距离")
    ap.add_argument("--compare-weapons", action="store_true", help="对比不同弓弩")
    ap.add_argument("--sweep", type=str, default="", help="扫描参数(如 range, skill, json_dispersion)")
    ap.add_argument("--sweep-values", type=str, default="", help="扫描值列表(逗号分隔, 如 1,2,4,8,16)")
    # 所有参数
    ap.add_argument("--bow-dmg", type=float, default=6.0)
    ap.add_argument("--arrow-amount", type=float, default=0.0)
    ap.add_argument("--arrow-cdm", type=float, default=1.5)
    ap.add_argument("--arrow-arpen", type=float, default=3.0)
    ap.add_argument("--arrow-crit-mult", type=float, default=10.0)
    ap.add_argument("--json-dispersion", type=float, default=150.0)
    ap.add_argument("--skill-constant", type=float, default=60.0)
    ap.add_argument("--dispersion-divider", type=float, default=15.0)
    ap.add_argument("--skill", type=float, default=10.0)
    ap.add_argument("--dex", type=float, default=10.0)
    ap.add_argument("--range", type=float, default=8.0)
    ap.add_argument("--target-armor", type=float, default=0.0)
    ap.add_argument("--target-hp", type=float, default=75.0)
    ap.add_argument("--target-size", type=float, default=0.5)
    ap.add_argument("--dodge", type=float, default=0.0)
    ap.add_argument("--crit-mod", type=float, default=1.0)

    args = ap.parse_args()

    params = {
        "bow_dmg": args.bow_dmg, "arrow_amount": args.arrow_amount,
        "arrow_cdm": args.arrow_cdm, "arrow_arpen": args.arrow_arpen,
        "arrow_crit_mult": args.arrow_crit_mult,
        "json_dispersion": args.json_dispersion,
        "skill_constant": args.skill_constant,
        "dispersion_divider": args.dispersion_divider,
        "skill": args.skill, "dex": args.dex,
        "range": args.range, "target_armor": args.target_armor,
        "target_hp": args.target_hp, "target_size": args.target_size,
        "dodge": args.dodge, "crit_mod": args.crit_mod,
    }

    if args.compare_skills:
        _cli_compare_skills(params)
    elif args.compare_ranges:
        _cli_compare_ranges(params)
    elif args.compare_weapons:
        _cli_compare_weapons(params)
    elif args.sweep:
        vals = [float(v.strip()) for v in args.sweep_values.split(",")] if args.sweep_values else []
        _cli_sweep(params, args.sweep, vals)
    elif args.cli:
        print(_cli_single(params))
    else:
        # GUI mode
        import tkinter as tk
        root = tk.Tk()
        RangedDamageSimulator(root)
        root.mainloop()


if __name__ == "__main__":
    _cli_main()

# -*- coding: utf-8 -*-
"""Day3 打卡统计脚本

读取 checkins.json 中的打卡记录，输出：
    1. 累计打卡天数（去重后的日期数）
    2. 连续打卡最长天数（历史中最长的一段连续打卡）
    3. 一份简单的文字报告
"""

import json
import os
from datetime import date, timedelta

# 数据文件与脚本放在同一目录
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkins.json")


def load_records(path=DATA_FILE):
    """从 JSON 文件读取打卡记录，文件不存在或损坏时返回空列表。"""
    if not os.path.exists(path):
        return []
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def unique_dates(records):
    """提取并排序所有不重复的打卡日期（返回 date 对象列表）。"""
    dates = set()
    for r in records:
        raw = r.get("date", "")
        try:
            dates.add(date.fromisoformat(raw))
        except ValueError:
            continue  # 跳过日期不合法或缺失的记录
    return sorted(dates)


def total_days(dates):
    """累计打卡天数 = 去重后的日期数量。"""
    return len(dates)


def longest_streak(dates):
    """连续打卡最长天数：历史中相邻日期连续的最长一段。"""
    if not dates:
        return 0
    longest = 1
    current = 1
    for prev, cur in zip(dates, dates[1:]):
        if cur - prev == timedelta(days=1):
            current += 1
            longest = max(longest, current)
        else:
            current = 1
    return longest


def total_hours(records):
    """累计学习时长（小时），容错处理非数字或缺失的时长。"""
    total = 0.0
    for r in records:
        try:
            total += float(r.get("duration", 0))
        except (TypeError, ValueError):
            continue
    return total


def build_report(records):
    """根据打卡记录生成一份简单的文字报告。"""
    if not records:
        return "暂无打卡记录，快去添加一条吧～"

    dates = unique_dates(records)
    lines = [
        "========== 打卡统计报告 ==========",
        f"打卡记录数：{len(records)} 条",
        f"累计打卡天数：{total_days(dates)} 天",
        f"连续打卡最长天数：{longest_streak(dates)} 天",
        f"累计学习时长：{total_hours(records):g} 小时",
    ]
    if dates:
        lines.append(f"首次打卡：{dates[0].isoformat()}")
        lines.append(f"最近打卡：{dates[-1].isoformat()}")
    lines.append("==================================")
    return "\n".join(lines)


def main():
    records = load_records()
    print(build_report(records))


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""命令行学习打卡程序

功能：
    1. 添加今日打卡记录
    2. 查看历史记录
    3. 查看统计（总时长 / 打卡天数 / 连续打卡）
    4. 记录自动保存到本地 checkins.json 文件
"""

import json
import os
from datetime import date, datetime, timedelta

# 数据文件与脚本放在同一目录
DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "checkins.json")


def load_records():
    """从本地文件读取打卡记录，文件不存在或损坏时返回空列表。"""
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_records(records):
    """把打卡记录写入本地文件。"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


def add_checkin(records):
    """添加一条今日打卡记录。"""
    print("\n========== 添加今日打卡 ==========")
    content = input("学习内容（如：背单词、刷题）: ").strip()
    if not content:
        print("学习内容不能为空，已取消。")
        return

    while True:
        raw = input("学习时长（小时，可为小数）: ").strip()
        try:
            duration = float(raw)
            if duration <= 0:
                print("时长需大于 0，请重新输入。")
                continue
            break
        except ValueError:
            print("请输入数字，例如 1.5 表示一个半小时。")

    note = input("备注（可选，直接回车跳过）: ").strip()

    record = {
        "date": date.today().isoformat(),  # 例如 2026-09-20
        "content": content,
        "duration": duration,
        "note": note,
    }
    records.append(record)
    save_records(records)
    print(f"✅ 打卡成功！今天已记录 {content}，时长 {duration:g} 小时。")


def view_history(records):
    """按日期顺序查看所有历史记录。"""
    print("\n========== 历史记录 ==========")
    if not records:
        print("暂无打卡记录，先去添加一条吧～")
        return

    # 按日期 + 录入顺序排序（最新的在最下面，方便连续阅读）
    ordered = sorted(records, key=lambda r: (r.get("date", ""),))
    print(f"{'日期':<12}{'内容':<20}{'时长':>8}  备注")
    print("-" * 60)
    for r in ordered:
        note = r.get("note", "") or ""
        print(f"{r.get('date', ''):<12}{r.get('content', ''):<20}"
              f"{r.get('duration', 0):>7g}h  {note}")
    print("-" * 60)


def show_stats(records):
    """统计总时长、打卡天数与连续打卡天数。"""
    print("\n========== 学习统计 ==========")
    if not records:
        print("暂无数据。")
        return

    total_hours = sum(float(r.get("duration", 0)) for r in records)
    days = {r.get("date") for r in records}

    # 计算连续打卡天数：从今天（或昨天）往前数连续的天
    dates = {date.fromisoformat(d) for d in days if d}
    today = date.today()
    if today not in dates:
        # 今天还没打卡时，从昨天开始算连续
        anchor = today - timedelta(days=1)
        if anchor not in dates:
            anchor = today  # 昨天也没打卡，则从今天开始（结果为 0）
    else:
        anchor = today

    streak = 0
    while anchor in dates:
        streak += 1
        anchor -= timedelta(days=1)

    print(f"累计打卡天数：{len(days)} 天")
    print(f"累计学习时长：{total_hours:g} 小时")
    print(f"连续打卡：{streak} 天")


MENU = """
========== 学习打卡 ==========
  1. 添加今日打卡
  2. 查看历史记录
  3. 查看统计
  0. 退出
==============================
"""


def main():
    records = load_records()
    while True:
        print(MENU)
        choice = input("请选择操作（0-3）: ").strip()
        if choice == "1":
            add_checkin(records)
        elif choice == "2":
            view_history(records)
        elif choice == "3":
            show_stats(records)
        elif choice == "0":
            print("再见，坚持就是胜利！👋")
            break
        else:
            print("输入有误，请输入 0-3 之间的数字。")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n已退出。")

# holiday-study 学习打卡仓库

Git + Python 学习打卡练习仓库，按天推进。

## 文件说明
- checkin.py      Day1/Day2：交互式打卡程序（添加 / 查看历史 / 统计）
- stats.py        Day3：统计脚本（读取记录，输出总天数、最长连续打卡、文字报告）
- checkins.json   打卡数据文件（由 checkin.py 自动生成）

## 环境要求
- Python 3.7+（用到 date.fromisoformat）

## 怎么运行

1. 添加打卡记录（交互式，会写入 checkins.json）：

    python checkin.py

2. 查看统计报告（Day3 脚本，读取 checkins.json）：

    python stats.py

输出示例：

    ========== 打卡统计报告 ==========
    打卡记录数：3 条
    累计打卡天数：3 天
    连续打卡最长天数：3 天
    累计学习时长：5.5 小时
    首次打卡：2026-09-19
    最近打卡：2026-09-21
    ==================================

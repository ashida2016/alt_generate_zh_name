#!/usr/bin/env python3
"""数据分析示例：对生成的学生信息进行统计分析。

演示如何用 pandas 对 generate() 的输出做分组统计和基本可视化准备。

运行方式::

    python examples/data_analysis.py
"""

import pandas as pd

from alt_generate_zh_name import generate

# ── 1) 生成大批量数据 ─────────────────────────────────────────
N = 1000
df = generate(N, seed=0)
print(f"=== 生成 {N} 名学生数据 ===\n")

# ── 2) 性别分布 ──────────────────────────────────────────────
gender_counts = df["gender"].value_counts()
print("【性别分布】")
for g, c in gender_counts.items():
    label = "男" if g == "M" else "女"
    bar = "█" * (c // 10)
    print(f"  {label} ({g}): {c:>4d}  {bar}")
print()

# ── 3) 姓氏 Top-10 ──────────────────────────────────────────
df["surname"] = df["name"].str[0]  # 取第一个字作为姓氏（简化处理）
top10 = df["surname"].value_counts().head(10)
print("【姓氏 Top-10】")
for surname, count in top10.items():
    pct = count / N * 100
    bar = "█" * int(pct)
    print(f"  {surname}: {count:>3d} ({pct:.1f}%)  {bar}")
print()

# ── 4) 出生年份分布 ──────────────────────────────────────────
df["birth_year"] = pd.to_datetime(df["birthday"]).dt.year
year_dist = df["birth_year"].value_counts().sort_index()
print("【出生年份分布】")
for year, count in year_dist.items():
    bar = "█" * (count // 5)
    print(f"  {year}: {count:>3d}  {bar}")
print()

# ── 5) 名字长度统计 ──────────────────────────────────────────
df["name_len"] = df["name"].str.len()
print("【姓名长度（含姓氏）】")
for length, count in df["name_len"].value_counts().sort_index().items():
    print(f"  {length} 字: {count:>4d}")
print()

print(f"✅ 分析完成。共 {N} 条记录。")

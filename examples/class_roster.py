#!/usr/bin/env python3
"""生成模拟班级花名册：带学号、随机成绩，并导出 CSV。

运行方式::

    python examples/class_roster.py

生成文件::

    examples/class_roster.csv
"""

from pathlib import Path

import numpy as np
import pandas as pd

from alt_generate_zh_name import generate

SEED = 2024
CLASS_SIZE = 45
OUTPUT = Path(__file__).parent / "class_roster.csv"

# ── 1) 生成学生基础信息 ───────────────────────────────────────
df = generate(CLASS_SIZE, birth_start="2008", birth_end="2010", seed=SEED)

# ── 2) 添加学号 ──────────────────────────────────────────────
df.insert(0, "student_id", [f"2024{i+1:03d}" for i in range(len(df))])

# ── 3) 添加随机成绩 ──────────────────────────────────────────
rng = np.random.default_rng(SEED)
df["语文"] = rng.integers(60, 101, size=len(df))
df["数学"] = rng.integers(50, 101, size=len(df))
df["英语"] = rng.integers(55, 101, size=len(df))
df["总分"] = df[["语文", "数学", "英语"]].sum(axis=1)

# ── 4) 按总分排名 ────────────────────────────────────────────
df = df.sort_values("总分", ascending=False).reset_index(drop=True)
df.insert(1, "rank", range(1, len(df) + 1))

# ── 5) 打印 & 导出 ───────────────────────────────────────────
print(f"=== 班级花名册 ({CLASS_SIZE} 人) ===")
print(df.to_string(index=False))
print()

df.to_csv(OUTPUT, index=False)
print(f"✅ 已导出到 {OUTPUT}")

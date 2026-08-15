#!/usr/bin/env python3
"""最简示例：生成 10 个学生信息并打印。

运行方式::

    python examples/basic_usage.py
"""

from alt_generate_zh_name import generate

# 生成 10 个随机学生
df = generate(10, seed=42)

print("=== 随机生成 10 个学生 ===")
print(df.to_string(index=False))
print()

# ── 指定姓氏 + 双名 ──────────────────────────────────────────
df_li = generate(5, surname="李", name_length=2, seed=7)

print("=== 李姓双名学生 ===")
print(df_li.to_string(index=False))
print()

# ── 指定出生年份范围 ──────────────────────────────────────────
df_range = generate(5, birth_start="2006", birth_end="2008", seed=99)

print("=== 2006–2008 年出生 ===")
print(df_range.to_string(index=False))
print()

# ── 可复现性验证 ──────────────────────────────────────────────
df1 = generate(3, seed=123)
df2 = generate(3, seed=123)
assert df1.equals(df2), "相同 seed 应产生完全一致的结果"
print("✅ 可复现性验证通过：seed=123 两次生成结果一致")

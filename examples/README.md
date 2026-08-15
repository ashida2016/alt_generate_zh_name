# examples — alt_generate_zh_name 示例脚本

可直接运行的示例，展示 `alt_generate_zh_name` 的典型用法。

## 运行方式

先安装包：

```bash
pip install -e ".[dev]"     # 从项目根目录安装
```

然后运行任一示例：

```bash
python examples/basic_usage.py      # 基础用法
python examples/class_roster.py     # 班级花名册（需 numpy）
python examples/data_analysis.py    # 数据分析统计
```

## 示例说明

| 文件 | 描述 | 额外依赖 |
|------|------|----------|
| `basic_usage.py` | 最简用法：随机生成、指定姓氏、指定年份、可复现性 | — |
| `class_roster.py` | 模拟班级花名册：学号 + 随机成绩 + CSV 导出 | numpy |
| `data_analysis.py` | 统计分析：性别/姓氏/年份/名字长度分布 | — |

# alt_generate_zh_name

一个能自动生成中国学生个人基础信息（姓名、性别、生日）的 Python 包。

## ✨ 特性

- 🎲 **姓氏按真实人口占比分配概率**：覆盖百家姓，李/王/张等大姓出现频率更高
- 📝 **200 个精选常用汉字**：按性别分组，均为正面、美好含义的字
- 📊 **返回 pandas DataFrame**：方便后续数据分析和处理
- 🔧 **灵活的参数控制**：可指定姓氏、名字长度、生日范围
- 🎯 **可复现**：支持随机种子

## 📦 安装

```bash
pip install .
```

开发模式安装（含测试依赖）：

```bash
pip install -e ".[dev]"
```

## 帮助文档

[ver0.2.2](https://alt-generate-zh-name.readthedocs.io/zh-cn/ver0.2.2/)  

## 🚀 快速上手

```python
from alt_generate_zh_name import generate

# 生成 10 个学生信息
df = generate(10)
print(df)
```

输出示例：

```
     姓名 性别         生日
0   张浩宇   男   2003-07-22
1   李静怡   女   2007-11-03
2   王明轩   男   2001-05-18
3   刘婷婷   女   2009-02-14
4   陈思远   男   2005-08-30
...
```

## 📖 API

### `generate(n, *, surname, name_length, birth_start, birth_end, seed)`

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `n` | `int` | `1` | 生成学生数量 |
| `surname` | `str \| None` | `None` | 指定姓氏，`None` 则按人口占比随机 |
| `name_length` | `1 \| 2 \| None` | `None` | 单名(1)/双名(2)，`None` 则随机 |
| `birth_start` | `str \| date \| None` | `None` | 生日起始（含），默认 2000-01-01 |
| `birth_end` | `str \| date \| None` | `None` | 生日结束（含），默认 2010-12-31 |
| `seed` | `int \| None` | `None` | 随机种子 |

**日期格式支持**：`"2005"`、`"2005-03"`、`"2005-03-15"` 或 `datetime.date` 对象。

**返回**：`pandas.DataFrame`，列为 `["姓名", "性别", "生日"]`。

## 📋 使用示例

```python
from alt_generate_zh_name import generate

# 指定姓氏 + 双名
df = generate(5, surname="李", name_length=2)

# 指定出生年份范围
df = generate(10, birth_start="2005", birth_end="2008")

# 可复现结果
df1 = generate(5, seed=42)
df2 = generate(5, seed=42)
assert df1.equals(df2)
```

## 🧪 测试

```bash
pytest tests/ -v
```

## 📄 许可证

Apache License 2.0

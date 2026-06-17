"""alt_generate_zh_name — 自动生成中国学生个人基础信息。

快速上手::

    from alt_generate_zh_name import generate

    df = generate(10)
    print(df)
"""

from alt_generate_zh_name.generator import generate

__version__ = "0.2.0"
__all__ = ["generate"]

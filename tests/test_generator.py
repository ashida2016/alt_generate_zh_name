"""alt_generate_zh_name 单元测试。"""

from __future__ import annotations

import datetime
from collections import Counter

import pandas as pd
import pytest

from alt_generate_zh_name import generate


class TestBasicGeneration:
    """基础生成功能测试。"""

    def test_default_generates_one_row(self) -> None:
        df = generate(seed=0)
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 1

    def test_column_names(self) -> None:
        df = generate(seed=0)
        assert df.columns.tolist() == ["姓名", "性别", "生日"]

    def test_column_types(self) -> None:
        df = generate(seed=0)
        row = df.iloc[0]
        assert isinstance(row["姓名"], str)
        assert row["性别"] in ("男", "女")
        assert isinstance(row["生日"], datetime.date)

    def test_generate_multiple(self) -> None:
        df = generate(100, seed=1)
        assert len(df) == 100

    def test_name_length_default(self) -> None:
        """默认名字长度为 2-3 个字符（姓1 + 名1-2）。"""
        df = generate(50, seed=2)
        for name in df["姓名"]:
            assert 2 <= len(name) <= 3

    def test_gender_distribution(self) -> None:
        """大样本下性别应该大致均匀。"""
        df = generate(1000, seed=3)
        counts = df["性别"].value_counts()
        # 允许一定偏差：每种性别至少 400
        assert counts["男"] >= 400
        assert counts["女"] >= 400


class TestSurnameOption:
    """指定姓氏测试。"""

    def test_fixed_surname(self) -> None:
        df = generate(20, surname="王", seed=10)
        for name in df["姓名"]:
            assert name.startswith("王")

    def test_fixed_surname_zhao(self) -> None:
        df = generate(10, surname="赵", seed=11)
        for name in df["姓名"]:
            assert name.startswith("赵")


class TestNameLength:
    """指定名字字数测试。"""

    def test_single_char_name(self) -> None:
        df = generate(20, name_length=1, seed=20)
        for name in df["姓名"]:
            assert len(name) == 2  # 姓1 + 名1

    def test_double_char_name(self) -> None:
        df = generate(20, name_length=2, seed=21)
        for name in df["姓名"]:
            assert len(name) == 3  # 姓1 + 名2

    def test_invalid_name_length(self) -> None:
        with pytest.raises(ValueError, match="name_length"):
            generate(1, name_length=3, seed=22)  # type: ignore[arg-type]


class TestBirthRange:
    """生日范围测试。"""

    def test_year_only(self) -> None:
        df = generate(50, birth_start="2005", birth_end="2005", seed=30)
        for birthday in df["生日"]:
            assert birthday.year == 2005

    def test_year_month(self) -> None:
        df = generate(50, birth_start="2006-03", birth_end="2006-03", seed=31)
        for birthday in df["生日"]:
            assert birthday.year == 2006
            assert birthday.month == 3

    def test_full_date(self) -> None:
        start = datetime.date(2007, 6, 1)
        end = datetime.date(2007, 6, 30)
        df = generate(50, birth_start=start, birth_end=end, seed=32)
        for birthday in df["生日"]:
            assert start <= birthday <= end

    def test_mixed_formats(self) -> None:
        df = generate(
            50,
            birth_start="2003",
            birth_end=datetime.date(2005, 6, 15),
            seed=33,
        )
        for birthday in df["生日"]:
            assert datetime.date(2003, 1, 1) <= birthday <= datetime.date(2005, 6, 15)

    def test_invalid_range_raises(self) -> None:
        with pytest.raises(ValueError, match="不能晚于"):
            generate(1, birth_start="2010", birth_end="2005", seed=34)


class TestSeed:
    """随机种子可复现性测试。"""

    def test_same_seed_same_result(self) -> None:
        df1 = generate(10, seed=99)
        df2 = generate(10, seed=99)
        pd.testing.assert_frame_equal(df1, df2)

    def test_different_seed_different_result(self) -> None:
        df1 = generate(10, seed=100)
        df2 = generate(10, seed=101)
        # 理论上不同种子应产生不同结果（极小概率相同）
        assert not df1.equals(df2)


class TestSurnameDistribution:
    """姓氏分布统计测试。"""

    def test_top_surnames_appear_frequently(self) -> None:
        """大样本下，李/王/张应出现在最高频的几个姓中。"""
        df = generate(5000, seed=50)
        # 提取姓氏（每个名字的第一个字）
        surnames = [name[0] for name in df["姓名"]]
        counter = Counter(surnames)
        top_10 = {s for s, _ in counter.most_common(10)}
        # 李、王、张至少应出现在前 10
        assert "李" in top_10
        assert "王" in top_10
        assert "张" in top_10


class TestEdgeCases:
    """边界情况测试。"""

    def test_n_zero_raises(self) -> None:
        with pytest.raises(ValueError, match="n 必须"):
            generate(0)

    def test_n_negative_raises(self) -> None:
        with pytest.raises(ValueError, match="n 必须"):
            generate(-1)

    def test_single_day_range(self) -> None:
        target = datetime.date(2005, 6, 15)
        df = generate(10, birth_start="2005-06-15", birth_end="2005-06-15", seed=60)
        for birthday in df["生日"]:
            assert birthday == target

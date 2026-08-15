"""核心生成逻辑：随机生成中国学生基础信息。"""

from __future__ import annotations

import calendar
import datetime
import random
from typing import Literal

import pandas as pd

from alt_generate_zh_name.data.given_names import FEMALE_CHARS, MALE_CHARS, NEUTRAL_CHARS
from alt_generate_zh_name.data.surnames import SURNAMES

# ── 预处理姓氏数据 ────────────────────────────────────────────
_SURNAME_NAMES: list[str] = [s for s, _ in SURNAMES]
_SURNAME_WEIGHTS: list[float] = [w for _, w in SURNAMES]

# ── 按性别合并字池 ────────────────────────────────────────────
_MALE_POOL: list[str] = MALE_CHARS + NEUTRAL_CHARS
_FEMALE_POOL: list[str] = FEMALE_CHARS + NEUTRAL_CHARS

_DEFAULT_BIRTH_START = datetime.date(2000, 1, 1)
_DEFAULT_BIRTH_END = datetime.date(2010, 12, 31)


def _parse_date(value: str | datetime.date, *, as_end: bool = False) -> datetime.date:
    """将灵活的日期输入解析为 ``datetime.date``。

    支持格式：
    - ``"2005"``        → 2005-01-01 或 2005-12-31
    - ``"2005-03"``     → 2005-03-01 或 2005-03-31
    - ``"2005-03-15"``  → 2005-03-15
    - ``datetime.date`` → 直接返回

    Args:
        value: 日期字符串或 ``datetime.date`` 对象。
        as_end: 若为 ``True``，对于年份/年月格式取该时段最后一天。

    Examples:
        >>> _parse_date("2005")
        datetime.date(2005, 1, 1)
        >>> _parse_date("2005", as_end=True)
        datetime.date(2005, 12, 31)
        >>> _parse_date("2005-03")
        datetime.date(2005, 3, 1)
        >>> _parse_date("2005-03", as_end=True)
        datetime.date(2005, 3, 31)
        >>> _parse_date("2005-03-15")
        datetime.date(2005, 3, 15)
        >>> import datetime
        >>> _parse_date(datetime.date(2008, 6, 1))
        datetime.date(2008, 6, 1)
    """
    if isinstance(value, datetime.date):
        return value

    parts = value.strip().split("-")
    if len(parts) == 1:
        # 仅年份
        year = int(parts[0])
        if as_end:
            return datetime.date(year, 12, 31)
        return datetime.date(year, 1, 1)
    elif len(parts) == 2:
        # 年-月
        year, month = int(parts[0]), int(parts[1])
        if as_end:
            last_day = calendar.monthrange(year, month)[1]
            return datetime.date(year, month, last_day)
        return datetime.date(year, month, 1)
    elif len(parts) == 3:
        # 年-月-日
        return datetime.date(int(parts[0]), int(parts[1]), int(parts[2]))
    else:
        raise ValueError(
            f"无法解析日期 '{value}'，支持格式：'2005'、'2005-03'、'2005-03-15'"
        )


def _random_birthday(
    rng: random.Random,
    start: datetime.date,
    end: datetime.date,
) -> datetime.date:
    """在 [start, end] 范围内随机生成一个日期。

    Args:
        rng: 随机数生成器实例。
        start: 日期范围起始（含）。
        end: 日期范围结束（含）。

    Returns:
        在 ``[start, end]`` 内均匀随机选取的 ``datetime.date``。

    Raises:
        ValueError: 如果 ``start`` 晚于 ``end``。

    Examples:
        >>> import random, datetime
        >>> rng = random.Random(0)
        >>> _random_birthday(rng, datetime.date(2005, 1, 1), datetime.date(2005, 12, 31))
        datetime.date(2005, 9, 10)
        >>> _random_birthday(rng, datetime.date(2000, 6, 1), datetime.date(2000, 6, 1))
        datetime.date(2000, 6, 1)
    """
    delta_days = (end - start).days
    if delta_days < 0:
        raise ValueError(
            f"生日起始日期 ({start}) 不能晚于结束日期 ({end})"
        )
    return start + datetime.timedelta(days=rng.randint(0, delta_days))


def generate(
    n: int = 1,
    *,
    surname: str | None = None,
    name_length: Literal[1, 2] | None = None,
    birth_start: str | datetime.date | None = None,
    birth_end: str | datetime.date | None = None,
    seed: int | None = None,
) -> pd.DataFrame:
    """随机生成 *n* 个学生的基础信息。

    Args:
        n: 生成学生数量，默认 ``1``。
        surname: 指定姓氏（如 ``"王"``）。为 ``None`` 时按中国人口姓氏占比随机选取。
        name_length: 指定名字字数：``1`` 为单名，``2`` 为双名。
            为 ``None`` 时随机选取 1 或 2。
        birth_start: 生日起始范围（含），支持 ``"2000"``、``"2000-09"``、
            ``"2000-09-01"`` 等格式，或 ``datetime.date`` 对象。默认
            ``2000-01-01``。
        birth_end: 生日结束范围（含），格式同上。默认 ``2010-12-31``。
        seed: 随机种子，用于可复现结果。

    Returns:
        ``pd.DataFrame``，列：``["name", "gender", "birthday"]``

        - **name** (*str*) — 如 ``"王明伟"``
        - **gender** (*str*) — ``"M"`` 或 ``"F"``
        - **birthday** (*datetime.date*) — 如 ``datetime.date(2005, 3, 15)``

    Raises:
        ValueError: 如果 ``n < 1``，``name_length`` 不是 1 或 2，
            或生日起始日期晚于结束日期。

    Examples:
        生成 3 个学生并查看列名：

        >>> from alt_generate_zh_name import generate
        >>> df = generate(3, seed=42)
        >>> df.columns.tolist()
        ['name', 'gender', 'birthday']

        指定姓氏和单名：

        >>> df = generate(2, surname="李", name_length=1, seed=0)
        >>> all(name.startswith("李") for name in df["name"])
        True
        >>> all(len(name) == 2 for name in df["name"])
        True

        限定出生年份范围：

        >>> import datetime
        >>> df = generate(5, birth_start="2008", birth_end="2008", seed=7)
        >>> all(d.year == 2008 for d in df["birthday"])
        True

        使用 ``seed`` 保证可复现：

        >>> generate(1, seed=99)["name"].iloc[0] == generate(1, seed=99)["name"].iloc[0]
        True
    """
    if n < 1:
        raise ValueError(f"n 必须 ≥ 1，收到 {n}")

    if name_length is not None and name_length not in (1, 2):
        raise ValueError(f"name_length 必须是 1 或 2，收到 {name_length}")

    # ── 解析日期范围 ──────────────────────────────────────────
    start = (
        _parse_date(birth_start, as_end=False)
        if birth_start is not None
        else _DEFAULT_BIRTH_START
    )
    end = (
        _parse_date(birth_end, as_end=True)
        if birth_end is not None
        else _DEFAULT_BIRTH_END
    )

    rng = random.Random(seed)

    records: list[dict[str, object]] = []

    for _ in range(n):
        # 性别
        gender: str = rng.choice(["M", "F"])

        # 姓氏
        if surname is not None:
            chosen_surname = surname
        else:
            chosen_surname = rng.choices(_SURNAME_NAMES, weights=_SURNAME_WEIGHTS, k=1)[0]

        # 名字长度
        length = name_length if name_length is not None else rng.choice([1, 2])

        # 名字汉字
        pool = _MALE_POOL if gender == "M" else _FEMALE_POOL
        given_chars = rng.choices(pool, k=length)

        # 姓名
        full_name = chosen_surname + "".join(given_chars)

        # 生日
        birthday = _random_birthday(rng, start, end)

        records.append({
            "name": full_name,
            "gender": gender,
            "birthday": birthday,
        })

    return pd.DataFrame(records)

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

    Parameters
    ----------
    value:
        日期字符串或 ``datetime.date`` 对象。
    as_end:
        若为 ``True``，对于年份/年月格式取该时段最后一天。
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
    """在 [start, end] 范围内随机生成一个日期。"""
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

    Parameters
    ----------
    n:
        生成学生数量，默认 ``1``。
    surname:
        指定姓氏（如 ``"王"``）。为 ``None`` 时按中国人口姓氏占比随机选取。
    name_length:
        指定名字字数：``1`` 为单名，``2`` 为双名。
        为 ``None`` 时随机选取 1 或 2。
    birth_start:
        生日起始范围（含），支持 ``"2000"``、``"2000-09"``、``"2000-09-01"``
        等格式，或 ``datetime.date`` 对象。默认 ``2000-01-01``。
    birth_end:
        生日结束范围（含），格式同上。默认 ``2010-12-31``。
    seed:
        随机种子，用于可复现结果。

    Returns
    -------
    pd.DataFrame
        列：``["姓名", "性别", "生日"]``

        - **姓名** (*str*) — 如 ``"王明伟"``
        - **性别** (*str*) — ``"男"`` 或 ``"女"``
        - **生日** (*datetime.date*) — 如 ``datetime.date(2005, 3, 15)``

    Examples
    --------
    >>> from alt_generate_zh_name import generate
    >>> df = generate(3, seed=42)
    >>> df.columns.tolist()
    ['姓名', '性别', '生日']
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
        gender: str = rng.choice(["男", "女"])

        # 姓氏
        if surname is not None:
            chosen_surname = surname
        else:
            chosen_surname = rng.choices(_SURNAME_NAMES, weights=_SURNAME_WEIGHTS, k=1)[0]

        # 名字长度
        length = name_length if name_length is not None else rng.choice([1, 2])

        # 名字汉字
        pool = _MALE_POOL if gender == "男" else _FEMALE_POOL
        given_chars = rng.choices(pool, k=length)

        # 姓名
        full_name = chosen_surname + "".join(given_chars)

        # 生日
        birthday = _random_birthday(rng, start, end)

        records.append({
            "姓名": full_name,
            "性别": gender,
            "生日": birthday,
        })

    return pd.DataFrame(records)

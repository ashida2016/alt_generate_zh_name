# AI Usage Guide — alt_generate_zh_name

This document helps AI agents (Copilot, Cursor, Antigravity, etc.) understand
how to use, extend, and contribute to `alt_generate_zh_name`.

## What This Package Does

Generates realistic fake Chinese student records — each containing a full name
(姓名), gender (M/F), and birthday — returned as a `pandas.DataFrame`.

Designed for **education scenarios** where you need plausible sample data
(course rosters, exam score sheets, teaching demos) without privacy concerns.

## Key API

```python
from alt_generate_zh_name import generate

df = generate(
    n=100,                        # number of students
    surname="王",                  # optional: fix surname
    name_length=2,                # optional: 1 (single-char) or 2 (double-char)
    birth_start="2005",           # optional: inclusive start
    birth_end="2008-06",          # optional: inclusive end
    seed=42,                      # optional: for reproducibility
)
# Returns: pd.DataFrame with columns ["name", "gender", "birthday"]
```

## Conventions & Design Decisions

| Topic | Convention |
|-------|-----------|
| **Public surface** | Only `generate()` is public (`__all__`). Everything else is internal. |
| **Surname weighting** | `data/surnames.py` stores `(surname, weight)` tuples based on real Chinese population proportions. Do not assume uniform distribution. |
| **Given-name pools** | `data/given_names.py` has three lists: `MALE_CHARS`, `FEMALE_CHARS`, `NEUTRAL_CHARS`. Gender-neutral chars are merged into both pools at runtime. |
| **Date parsing** | `_parse_date()` accepts `"2005"`, `"2005-03"`, `"2005-03-15"`, or `datetime.date`. When used as an end bound, partial dates expand to the last day of the period. |
| **RNG** | Uses a per-call `random.Random(seed)` instance — no global state mutation. |
| **Return type** | Always `pd.DataFrame`. The `birthday` column contains `datetime.date` objects (not strings, not `pd.Timestamp`). |

## Common Integration Patterns

### Generate a class roster with sequential IDs

```python
import pandas as pd
from alt_generate_zh_name import generate

df = generate(40, birth_start="2008", birth_end="2010", seed=1)
df.insert(0, "student_id", range(2024001, 2024001 + len(df)))
```

### Combine with random scores

```python
import numpy as np
from alt_generate_zh_name import generate

df = generate(30, seed=7)
rng = np.random.default_rng(7)
df["math_score"] = rng.integers(40, 101, size=len(df))
df["chinese_score"] = rng.integers(50, 101, size=len(df))
```

### Export to Excel / CSV

```python
df = generate(50)
df.to_csv("students.csv", index=False)
df.to_excel("students.xlsx", index=False)
```

## Gotchas for AI Agents

1. **Don't import internals.** `from alt_generate_zh_name.generator import _parse_date`
   works but is private; prefer the public `generate()` function.
2. **`birthday` is `datetime.date`, not a string.** If you need string formatting,
   do `df["birthday"].astype(str)` or `df["birthday"].apply(str)`.
3. **`n` must be ≥ 1.** Passing `n=0` raises `ValueError`.
4. **`name_length` accepts only `1`, `2`, or `None`.** Other integers raise
   `ValueError`.
5. **Seed gives exact reproducibility** only within the same package version.
   Internal pool ordering may change across versions.
6. **The package is pure Python** — no C extensions, no network calls, no filesystem
   I/O. Safe to run in sandboxed environments.

## Development

```bash
# Install in editable mode with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Build docs
pip install -e ".[docs]"
cd docs && make html
```

## File Map

```
src/alt_generate_zh_name/
├── __init__.py          # re-exports generate(); defines __version__
├── generator.py         # core logic: generate(), _parse_date(), _random_birthday()
├── py.typed             # PEP 561 marker
└── data/
    ├── __init__.py
    ├── surnames.py      # SURNAMES: list[tuple[str, float]] — 百家姓 with weights
    └── given_names.py   # MALE_CHARS, FEMALE_CHARS, NEUTRAL_CHARS: list[str]
```

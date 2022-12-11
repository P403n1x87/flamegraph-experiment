import typing as t
from pathlib import Path

from flamegraph import AustinFlameGraph, compare

PREFIX = Path("data")


def maybe_from_austin(file: str) -> t.Optional[AustinFlameGraph]:
    try:
        return AustinFlameGraph.from_austin(PREFIX / file)
    except Exception:
        return None


def collect(file: str) -> t.List[AustinFlameGraph]:
    return [
        _
        for _ in (maybe_from_austin(f"{file}_{i}.austin") for i in range(101))
        if _ is not None
    ]


base = collect("base")
regression = collect("regression")


dp, dm, f, p = compare(regression, base, threshold=5)
print("p-value:", p)
print("\nΔ+:", dp)
print("\nΔ-:", dm)

import typing as t
from collections import Counter
from itertools import chain
from pathlib import Path

from austin.stats import AustinStats, Sample

from map import Map


class AustinFlameGraph(Map):
    def norm(self):
        return sum(abs(v) for v in self.values())

    @classmethod
    def from_austin(cls, austinfile: Path) -> "AustinFlameGraph":
        fg = cls()

        for l in austinfile.open():
            l = l.strip()
            if not l or l.startswith("# "):
                continue
            stack, _, m = l.rpartition(" ")

            # Remove PID and TID
            _, _, stack = stack.partition(";")
            _, _, stack = stack.partition(";")

            fg += cls({stack: int(m)})

        return fg

    def to_austin_stats(self) -> AustinStats:
        stats = AustinStats()

        for stack, m in self.items():
            stats.update(Sample.parse(f"P0;T0;{stack} {m}"))

        return stats

    def to_list(self, domain: list) -> list:
        return [self(v) for v in domain]

    @classmethod
    def from_list(cls, values: list, domain: list) -> "AustinFlameGraph":
        return cls({k: v for k, v in zip(domain, values) if v})

    def to_austin(self, prefix: str = "") -> str:
        return "\n".join((f"{prefix}{s} {round(v)}" for s, v in self.items() if v))


def parts(delta: AustinFlameGraph) -> t.Tuple[AustinFlameGraph, AustinFlameGraph]:
    return (
        AustinFlameGraph({k: v for k, v in delta.items() if v > 0}),
        AustinFlameGraph({k: -v for k, v in delta.items() if v < 0}),
    )


def diff(
    f1: AustinFlameGraph, f2: AustinFlameGraph
) -> t.Tuple[AustinFlameGraph, AustinFlameGraph]:
    return parts(f1 - f2)


def compare(
    x: t.List[AustinFlameGraph],
    y: t.List[AustinFlameGraph],
    threshold: t.Optional[float] = None,
) -> t.Tuple[AustinFlameGraph, AustinFlameGraph, float, float]:
    domain = list(set().union(*(_.supp() for _ in chain(x, y))))

    if threshold is not None:
        c = Counter()
        for _ in chain(x, y):
            c.update(_.supp())
        domain = sorted([k for k, v in c.items() if v >= threshold])

    import numpy as np

    from stats import hotelling_two_sample_test

    X = np.array([f.to_list(domain) for f in x], dtype=np.int32)
    Y = np.array([f.to_list(domain) for f in y], dtype=np.int32)

    d, f, p, m = hotelling_two_sample_test(X, Y)

    delta = AustinFlameGraph({k: v for k, v, a in zip(domain, d, m) if v and a})

    return *parts(delta), f, p


def joint_average(
    x: t.List[AustinFlameGraph],
    y: t.List[AustinFlameGraph],
    threshold: t.Optional[float] = None,
) -> t.Tuple[AustinFlameGraph, AustinFlameGraph]:
    domain = list(set().union(*(_.supp() for _ in chain(x, y))))

    if threshold is not None:
        c = Counter()
        for _ in chain(x, y):
            c.update(_.supp())
        domain = sorted([k for k, v in c.items() if v >= threshold])

    import numpy as np

    X = np.array([f.to_list(domain) for f in x], dtype=np.int32)
    Y = np.array([f.to_list(domain) for f in y], dtype=np.int32)

    return AustinFlameGraph(zip(domain, np.mean(X, axis=0))), AustinFlameGraph(
        zip(domain, np.mean(Y, axis=0))
    )


if __name__ == "__main__":
    gs = [
        _
        for _ in (
            AustinFlameGraph.from_austin(f"samples/sample{i}.austin")
            for i in range(100)
        )
        if _
    ]
    c = len(gs)

    dp, dm, f, p = compare(gs[: c // 2], gs[c // 2 :], threshold=0.5 * c)

    print("No difference" if p > 0.01 else "Difference")

from random import randint as r

from tikz import Picture, node, rectangle

DY = 0.25
NODESCALE = 0.5


class FlameGraphDrawer(Picture):
    def __init__(
        self,
        width=8.0,
        threshold=0.001,
        color=lambda: f"red!{r(10,67)}",
        pdf=None,
        phony=False,
    ):
        self.width = width
        self.threshold = threshold
        self.pdf = pdf
        self.phony = phony
        self.color = color

    def draw_frame(self, fs, x, y, s_x, threshold):
        total = fs.total.value

        label = f"{fs.label.function}:{fs.label.line}"[: int(s_x * total) * 16].replace(
            "_", "\_"
        )
        self.fill(
            (x, y),
            rectangle((x + s_x * total, y + DY)),
            node(label, midway=True, scale=NODESCALE),
            fill=self.color(),
        )

        for f in fs.children.values():
            if f.total.value < threshold:
                continue
            x += s_x * self.draw_frame(f, x, y + DY)

        return total

    def draw_thread(self, tid, ts, x, s_x, threshold):
        total = ts.total.value

        if not self.phony:
            self.fill(
                (x, DY),
                rectangle((x + s_x * total, DY * 2)),
                node(
                    f"Thread {tid}"[: int(s_x * total) * 16],
                    midway=True,
                    scale=NODESCALE,
                ),
                fill=COLOR(),
            )

        for fs in ts.children.values():
            if fs.total.value < threshold:
                continue
            x += s_x * self.draw_frame(
                fs, x, 0 if self.phony else DY * 2, s_x, threshold
            )

        return total

    def draw_process(self, pid, ps, x, s_x, threshold):
        total = sum(_.total.value for _ in ps.threads.values())

        if not self.phony:
            self.fill(
                (x, 0),
                rectangle((x + s_x * total, DY)),
                node(
                    f"Process {pid}"[: int(s_x * total) * 16],
                    midway=True,
                    scale=NODESCALE,
                ),
                fill=COLOR(),
            )

        for tid, ts in ps.threads.items():
            if ts.total.value < threshold:
                continue
            x += s_x * self.draw_thread(tid, ts, x, s_x, threshold)

        return total

    def draw(self, fg):
        stats = fg.to_austin_stats()
        x = 0
        n = fg.norm()
        s_x = self.width / n  # Scale factor

        for pid, ps in stats.processes.items():
            x += s_x * self.draw_process(pid, ps, x, s_x, self.threshold * n)

        print(self.code)

        if self.pdf is not None:
            self.write_image(self.pdf)


# x = 0
# for pid, ps in stats.processes.items():
#     x += s_x * draw_process(pid, ps, x)

# print(pic.code)
# pic.write_image("fg.pdf")

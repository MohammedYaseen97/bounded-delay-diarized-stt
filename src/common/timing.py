from __future__ import annotations

import time
from contextlib import contextmanager
from dataclasses import dataclass, field


@dataclass
class StageTimings:
    """
    Lightweight timing recorder.
    Intended for both offline runs and pseudo-streaming runs.
    """

    stages_ms: dict[str, list[float]] = field(default_factory=dict)

    def add(self, stage: str, ms: float) -> None:
        self.stages_ms.setdefault(stage, []).append(ms)

    @contextmanager
    def time(self, stage: str):
        t0 = time.perf_counter()
        try:
            yield
        finally:
            self.add(stage, (time.perf_counter() - t0) * 1000.0)

    def summary(self) -> dict[str, dict[str, float]]:
        out: dict[str, dict[str, float]] = {}
        for stage, vals in self.stages_ms.items():
            if not vals:
                continue
            out[stage] = {
                "count": float(len(vals)),
                "mean_ms": float(sum(vals) / len(vals)),
                "p50_ms": float(sorted(vals)[len(vals) // 2]),
                "max_ms": float(max(vals)),
            }
        return out


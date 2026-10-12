import time
from dataclasses import dataclass, field


@dataclass
class RequestMetrics:
    request_id: str
    started_at: float = field(default_factory=time.perf_counter)
    router_ms: float | None = None
    retrieval_ms: float | None = None
    model_ms: float | None = None

    def elapsed_ms(self) -> float:
        return (time.perf_counter() - self.started_at) * 1000

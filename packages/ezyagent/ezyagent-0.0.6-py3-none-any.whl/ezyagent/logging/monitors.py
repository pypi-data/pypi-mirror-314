import time
from typing import Any, Dict, List, Optional


class Metric:
    """Base class for metrics."""

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.value: Any = None

    def update(self, value: Any) -> None:
        """Update metric value."""
        self.value = value

    def get(self) -> Any:
        """Get current metric value."""
        return self.value


class Counter(Metric):
    """Counter metric type."""

    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.value = 0

    def increment(self, amount: int = 1) -> None:
        """Increment counter."""
        self.value += amount

    def reset(self) -> None:
        """Reset counter to zero."""
        self.value = 0


class Gauge(Metric):
    """Gauge metric type for values that can go up and down."""

    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.value = 0.0


class Timer(Metric):
    """Timer metric type."""

    def __init__(self, name: str, description: str):
        super().__init__(name, description)
        self.start_time: Optional[float] = None
        self.durations: List[float] = []

    def start(self) -> None:
        """Start the timer."""
        self.start_time = time.time()

    def stop(self) -> float:
        """Stop the timer and return duration."""
        if self.start_time is None:
            raise ValueError("Timer not started")

        duration = time.time() - self.start_time
        self.durations.append(duration)
        self.start_time = None
        return duration

    def get_average(self) -> float:
        """Get average duration."""
        if not self.durations:
            return 0.0
        return sum(self.durations) / len(self.durations)


class MetricsMonitor:
    """Monitor for collecting and managing metrics."""

    def __init__(self):
        self.metrics: Dict[str, Metric] = {}

    def register(self, metric: Metric) -> None:
        """Register a new metric."""
        self.metrics[metric.name] = metric

    def get_metric(self, name: str) -> Optional[Metric]:
        """Get a metric by name."""
        return self.metrics.get(name)

    def get_all_metrics(self) -> Dict[str, Any]:
        """Get all current metric values."""
        return {name: metric.get() for name, metric in self.metrics.items()}

    def reset_all(self) -> None:
        """Reset all metrics."""
        for metric in self.metrics.values():
            if isinstance(metric, Counter):
                metric.reset()
from typing import Callable
from torch import Tensor, mean, cat
from torch.utils.tensorboard import SummaryWriter


class Metric:
    def __init__(
        self, name: str, accumulator: Callable[..., Tensor] = mean, device=None
    ) -> None:
        self.name = name
        self.accumulator = accumulator
        self.device = device

        self.values = []
        self.sample_count = 0

    def accumulate(self, value: Tensor) -> None:
        self.values.append(value)
        self.sample_count += value.size(0)

    def aggregate(self) -> Tensor:
        combined = cat(self.values)
        return self.accumulator(combined)

    def reset(self) -> None:
        self.values = []
        self.sample_count = 0


class MetricManager:
    def __init__(self, writer: SummaryWriter, device: str) -> None:
        self.writer = writer
        self.device = device
        self.metrics: dict[str, Metric] = {}

    def register(self, name: str, accumulator: Callable[..., Tensor] = mean) -> None:
        self.metrics[name] = Metric(name, accumulator, self.device)

    def accumulate(self, name: str, value: Tensor) -> None:
        self.metrics[name].accumulate(value)

    def record(self, epoch: int) -> None:
        for name, metric in self.metrics.items():
            result = metric.aggregate()
            self.writer.add_scalar(name, result.item(), epoch)

    def reset(self) -> None:
        for metric in self.metrics.values():
            metric.reset()

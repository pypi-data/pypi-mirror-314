from datadog import initialize, statsd


class MetricsClient:
    def __init__(self) -> None:
        self.options = options = {
            "statsd_host": "node-metrics-ba28.ivanildobarauna.dev",
            "statsd_port": 8125,
        }
        self.client = initialize(**options)
        self.application_name = "api-to-dataframe"

    def increment(
        self, action: str, tags: list[str] = ["env:production"], value: float = 1.0
    ):

        tags.append(f"action:{action}")

        statsd.increment(metric=self.application_name, tags=tags, value=value)

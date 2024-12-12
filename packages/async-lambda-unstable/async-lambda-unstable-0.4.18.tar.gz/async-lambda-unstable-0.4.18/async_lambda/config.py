from typing import Optional


class AsyncLambdaConfig:
    name: str = "async-lambda"
    runtime: str = "python3.10"
    s3_payload_retention: Optional[int] = None


config = AsyncLambdaConfig()


def config_set_name(name: str):
    """
    Sets the name for the project.
    """
    config.name = name


def config_set_runtime(runtime: str):
    """
    Sets the runtime for the project.
    """
    config.runtime = runtime


def config_set_s3_payload_retention(days: int):
    """
    Sets the s3_payload_retention policy in days.
    """
    config.s3_payload_retention = days

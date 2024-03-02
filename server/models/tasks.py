from dataclasses import dataclass


class TaskParams:
    ...


@dataclass
class UrlShorten(TaskParams):
    url: str

from dataclasses import dataclass


class TaskParams:
    ...


@dataclass
class MsgLogger(TaskParams):
    msg: str

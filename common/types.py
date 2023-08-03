from dataclasses import dataclass


class ArgsType:
    model: str
    platform: str

@dataclass
class Environment:
    model: object
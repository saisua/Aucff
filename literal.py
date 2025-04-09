from dataclasses import dataclass


@dataclass(slots=True)
class Literal:
    t: str

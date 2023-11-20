import dataclasses
import logging


@dataclasses.dataclass
class Bid:
    fee: int
    execution_time: int
    valid_until: int

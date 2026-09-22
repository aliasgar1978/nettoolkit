
from typing import Any
from dataclasses import dataclass, field

from .common import Topology

@dataclass
class TopologyLayer(Topology):
    name: str
    nodes: list = field(default_factory=list)
    connectors: list = field(default_factory=list)
    remarks: Any=''     

    def __post_init__(self):
        self.set_remarks(self.remarks)

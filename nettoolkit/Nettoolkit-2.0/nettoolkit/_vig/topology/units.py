
# --------------------------------------------------------------------------------------------------------------- 
#  Imports
# --------------------------------------------------------------------------------------------------------------- 

from typing import Any
from dataclasses import dataclass

from .common import Topology

# --------------------------------------------------------------------------------------------------------------- 
#  An item
# --------------------------------------------------------------------------------------------------------------- 

@dataclass
class TopologyNode(Topology):
    hostname: str
    device_type: str           ## ex: reference for stencil lookup. Ex: ( router, switch, ap, pc, )
    ip: str=''                  ## ex: 192.168.1.1, 2002:1f0::1, etc.
    model: str=''               ## ex: Cisco 2960, Juniper EX4300, Fortinet FortiGate 60E, etc.
    # os: str=''                  ## ex: IOS, IOS-XE, NX-OS,
    serial: str=''              ## ex: FOC12345678, JNPR12345678, FGT12345678, etc.
    remarks: Any=''             ## ex: any additional information about the device, such as location, owner, etc.

    def __post_init__(self):
        self.set_remarks(self.remarks)
        self.width = 0
        self.height = 0
        self.position_ref_x = 0
        self.position_ref_y = 0
        self._layers = set()
        self._layer_to_group = {}

    @property
    def width(self): return self._width
    @width.setter
    def width(self, n: float): self._width=n
    @property
    def height(self): return self._height
    @height.setter
    def height(self, n: float): self._height=n
    @property
    def position_ref_x(self): return self._position_ref_x
    @position_ref_x.setter
    def position_ref_x(self, n: float): self._position_ref_x=n
    @property
    def position_ref_y(self): return self._position_ref_y
    @position_ref_y.setter
    def position_ref_y(self, n: float): self._position_ref_y=n

    ## decides device part of which drawing ##
    @property
    def layers(self):
        return self._layers

    def add_to_layers(self, layer: {str, int, tuple, list, set}): 
        if isinstance(layer, (str, int)):
            self._layers.add(layer)
            self._layer_to_group.setdefault(layer, None)
        elif isinstance(layer, (set, list, tuple)):
            self._layers.update(layer)
            self._layer_to_group.update( {x: None for x in layer if x not in self._layer_to_group} )

    ## decides whether this device is of which group/level eg. 
    ## (core/dist/access/security/sdwan/crossover etc)
    def group(self, layer): 
        return self._level
    def level(self, layer): 
        return self._level

    def set_level(self, **kwargs):
        for layer, level in kwargs.items():
            if layer not in self._layers:
                self.add_to_layers(layer)
            self._layer_to_group[layer] = level




# --------------------------------------------------------------------------------------------------------------- 
#  Usually known as TopologyEdge = TopologyConnector
# --------------------------------------------------------------------------------------------------------------- 

@dataclass
class TopologyConnector(Topology):
    src: TopologyNode
    dst: TopologyNode
    src_port: str           ## ex: Gi0/1, Ten0/1, xe-0/0/0, Fortygig0/1 etc. 
    dst_port: str           ## ex: Gi0/1, Ten0/1, xe-0/0/0, Fortygig0/1 etc.
    src_sfp: str=''         ## ex: GLC-T, GLC-SX-MMD, GLC-LH-SMD, SFP-10G-SR, SFP-10G-LR, SFP-10G-LRM, SFP-10G-ZR, etc
    dst_sfp: str=''         ## ex: GLC-T, GLC-SX-MMD, GLC-LH-SMD, SFP-10G-SR, SFP-10G-LR, SFP-10G-LRM, SFP-10G-ZR, etc

    medium: str=''           ## ex: copper, fiber, wireless, serial, etc
    cable_type: str=''       ## ex: cat5, cat6, cat6a, cat7, fiber, coaxial, etc 
    speed: str=''            ## ex: 1G, 10G, 25G, 40G, 100G, etc
    color: str='black'       ## ex: black, blue, red, green, yellow, etc
    weight: float=1          ## ex: 1.5, 2, 3.2, 4, 5, etc
    pattern: int=1           ## ex: 1, 2, 3, 4, 5, etc

    remarks: Any=''     

    def __str__(self):
        return self.connection_str

    def __post_init__(self):
        self.set_remarks(self.remarks)
        self.connection_str = f"{self.cable_type} {self.medium}"

    def get_connector(self):
        return {
            'src': {
                'device': self.src,
                'port': self.src_port,
                'sfp': self.src_sfp,
            },
            'dst': {
                'device': self.dst,
                'port': self.dst_port,
                'sfp': self.dst_sfp,
            },
            'connection': {
                'via': self.connection_str,
                'color': self.color,
                'speed': self.speed,
                'weight': self.weight,
                'pattern': self.pattern,
            } 
        }

TopologyEdge = TopologyConnector


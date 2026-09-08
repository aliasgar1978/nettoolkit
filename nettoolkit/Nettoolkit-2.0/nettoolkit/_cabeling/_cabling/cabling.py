
import os
from copy import deepcopy
from dataclasses import dataclass, field
from nettoolkit.cmn.fio import read_yaml
from nettoolkit.cmn.fdict import merge_dict

@dataclass
class DeviceData():
    conf_file: str = ''
    telemetry_file: str = ''

    _system_dict: dict = field(default_factory=dict, init=False)
    _intfs_dict: dict = field(default_factory=dict, init=False)
    conf_data: dict = field(default_factory=dict, init=False)
    telemetry_data: dict = field(default_factory=dict, init=False)


    def __post_init__(self):
        self.conf_data = {}
        self.telemetry_data = {}
        self._system_dict = {}
        self._intfs_dict = {}

        self.read_yaml()
        self.merge_system()
        self.merge_intf()

    @property
    def system_data(self):
        return self._system_dict
    @property
    def physical_interfaces(self):
        return self._intfs_dict.get('physical', {})

    @property
    def hostname(self):
        return self.system_data.get('identity', {}).get("hostname", "")
    @property
    def serial(self):
        return self.system_data.get('hardware', {}).get("serial_number", "")
    @property
    def hardware(self):
        return self.system_data.get('hardware', {}).get("model", "")
    @property
    def software(self):
        return self.system_data.get('software', {}).get("version", "")


    def physical_interface_data(self, intf):
        return self.physical_interfaces.get(intf, {})

    def neighbor(self, intf):
        return self.physical_interface_data(intf).get('neighbor', {})
    def neighbor_hostname(self, intf):
        return self.neighbor(intf).get('hostname', '')
    def neighbor_intf(self, intf):
        return self.neighbor(intf).get('interface', '')
    def neighbor_make(self, intf):
        return self.neighbor(intf).get('platform', '')

    def sfp(self, intf):
        return self.physical_interface_data(intf).get('hardware', {}).get('media_type', '')

    def read_yaml(self):
        self.conf_data = {}
        self.telemetry_data = {}
        if self.conf_file and os.path.exists(self.conf_file):
            self.conf_data = read_yaml(self.conf_file) or {}
        if self.telemetry_file and os.path.exists(self.telemetry_file):
            self.telemetry_data = read_yaml(self.telemetry_file) or {}

    def merge_system(self):
        self._system_dict = deepcopy(self.conf_data.get('system', {}))
        merge_dict(self._system_dict, self.telemetry_data.get('system', {}))

    def merge_intf(self):
        self._intfs_dict = deepcopy(self.conf_data.get('interfaces', {}))
        merge_dict(self._intfs_dict, self.telemetry_data.get('interfaces', {}))


# ===================================================================================
if __name__ == "__main__":
    pass
# ===================================================================================

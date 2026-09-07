from dataclasses import dataclass
from nettoolkit.cmn.fio import read_yaml, file_to_list
from nettoolkit.cmn.fdict import merge_dict

from pprint import pprint

@dataclass
class DeviceData():
    device: str

    device_file_suffix = "_devices-data.yaml"
    telemetry_file_suffix = "_devices-telemetry-data.yaml"

    def __post_init__(self):
        self.conf_file = self.device + self.device_file_suffix
        self.telemetry_file = self.device + self.telemetry_file_suffix

    def __call__(self, *args, **kwds):
        self.read_yaml()
        self.merge_intf()

    def read_yaml(self):
        self.conf_data = read_yaml(self.conf_file)
        self.telemetry_data = read_yaml(self.telemetry_file)

    def merge_intf(self):
        intfs_dict = self.conf_data['interfaces']
        merge_dict(intfs_dict, self.telemetry_data['interfaces'])
        print(intfs_dict)
        for k, v in intfs_dict.items():
            pprint(v)


# ===================================================================================
hn = '00h-ecd-a'

DD = DeviceData(hn)
DD()

# print(DD.telemetry_data)

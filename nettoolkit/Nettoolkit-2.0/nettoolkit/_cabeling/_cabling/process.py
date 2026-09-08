"""class-based cabling topography layout generator with physical port aggregation """

# ==============================================================================
#  Imports
# ==============================================================================
import os
import csv
import re

from .cabling import DeviceData
from .specs import CableSpecs

# ==============================================================================
#  MASTER TOPOLOGY REPORT COMPILER CLASS
# ==============================================================================
class CablingLayoutGenerator:
    """
    Orchestrates directory sweeps across split variables blocks 
    to parse and export clean, consolidated physical interface patching guides.
    """
    def __init__(self, data_directory):
        self.data_dir = data_directory
        self.cabling_matrix = []
        self.processed_connections = set()
        self.devices_data = {}
        self.staged_links = {}

    def __call__(self, *args, **kwds):
        self.load_data()
        self.get_staged_links()
        self.update_cabling_matrix()

    def load_data(self):
        if not os.path.isdir(self.data_dir):
            raise FileNotFoundError(f"Inventory directory not found: {self.data_dir}")
        all_files = os.listdir(self.data_dir)
        device_baselines = set()

        # Isolate clean system hostnames using regex match parameters
        for f in all_files:
            if f.endswith('_devices-data.yaml'):
                hostname = re.sub(r'_devices-data\.yaml$', '', f, flags=re.IGNORECASE)
                device_baselines.add(hostname)
            elif f.endswith('_devices-telemetry-data.yaml'):
                hostname = re.sub(r'_devices-telemetry-data\.yaml$', '', f, flags=re.IGNORECASE)
                device_baselines.add(hostname)

        for hostname in device_baselines:
            conf_file = os.path.join(self.data_dir, f"{hostname}_devices-data.yaml")
            tel_file = os.path.join(self.data_dir, f"{hostname}_devices-telemetry-data.yaml")            
            if not os.path.exists(conf_file):
                print(f"[-] {hostname} Device Data File missing, some data will be missing")
            if not os.path.exists(tel_file):
                print(f"[-] {hostname} Device Telemetry File missing, some data will be missing")
            self.devices_data[hostname] = DeviceData(conf_file=conf_file, telemetry_file=tel_file)

    def get_staged_links(self):
        for hostname, device_data in self.devices_data.items():
            hostname = hostname.lower()
            for raw_local_intf, intf_data in device_data.physical_interfaces.items():
                if not intf_data: continue
                remote_device = device_data.neighbor_hostname(raw_local_intf).lower()
                raw_remote_port = device_data.neighbor_intf(raw_local_intf)
                if not remote_device or not raw_remote_port: continue
                #
                phys_local_port = self._strip_logical_unit(raw_local_intf)
                phys_remote_port = self._strip_logical_unit(raw_remote_port)
                #
                local_unit = self._get_logical_unit(raw_local_intf)
                remote_unit = self._get_logical_unit(raw_remote_port)

                # unique lookup token & add interface units
                map_key = (hostname, phys_local_port, remote_device, phys_remote_port)
                if map_key not in self.staged_links:
                    self.staged_links[map_key] = {
                        'local_units': set(),
                        'remote_units': set(),
                        # 'metrics': intf_data,
                    }
                self.staged_links[map_key]['local_units'].add(local_unit)
                self.staged_links[map_key]['remote_units'].add(remote_unit)

    def update_cabling_matrix(self):
        for (local_host, local_port, remote_host, remote_port), data in self.staged_links.items():
            conn_token = frozenset( {(local_host, local_port), (remote_host, remote_port)} ) 
            if conn_token in  self.processed_connections: continue
            self.processed_connections.add(conn_token)    
            #
            local_sfp, remote_sfp = 'MISSING OPTIC', 'MISSING OPTIC'
            local_device_obj = self.devices_data.get(local_host, None)
            if isinstance(local_device_obj, DeviceData):
                local_sfp = local_device_obj.sfp(local_port)

            remote_device_obj = self.devices_data.get(remote_host, None)
            if isinstance(remote_device_obj, DeviceData):
                remote_sfp = remote_device_obj.sfp(remote_port)
            else:
                remote_sfp = 'MISSING REMOTE FILE'
            #
            specs = CableSpecs(local_sfp)
            if specs.medium == "Unknown Medium" and remote_sfp.upper().strip() not in ['MISSING OPTIC', 'MISSING REMOTE FILE']:
                specs = CableSpecs(remote_sfp)
            #

            local_units_str = ",".join(self.sort_units(list(data['local_units'])))
            remote_units_str = ",".join(self.sort_units(list(data['remote_units'])))
            #
            cable_record = {
                'local_device': local_host,
                'local_interface': local_port,
                'local_units': local_units_str,
                'local_sfp_type': local_sfp,
                'remote_device': remote_host,
                'remote_interface': remote_port,
                'remote_units': remote_units_str,
                'remote_sfp_type': remote_sfp,
                'cable_medium_type': specs.medium,
                'link_speed_capacity': specs.speed,
                'physical_cable_type': specs.cable_type,
                'cable_color_code': specs.color
            }
            self.cabling_matrix.append(cable_record)

    def sort_units(self, units):
        return sorted(units, key=lambda x: int(x) if str(x).isdigit() else x)                

    def _get_logical_unit(self, interface_name):
        return str(interface_name).split(".")[-1] if "." in interface_name else "0"

    def _strip_logical_unit(self, interface_name):
        """
        Slices trailing unit dot notation values securely while preserving
        high-speed channelised breakout paths completely intact.
        """
        if not interface_name:
            return ""
        if "." in str(interface_name):
            return str(interface_name).split(".")[0].strip()
        return str(interface_name).strip()

    def export_to_csv(self, output_filename="cabling_layout_matrix.csv"):
        """Dumps compiled matrix entries out to a presentation-ready spreadsheet document."""
        if not self.cabling_matrix:
            print("[-] Analysis complete: No data collected. Please Run topology_engine() first.")
            return

        headers = [
            'Local Device Name', 'Local Port', 'Local Units', 'Local SFP',
            'Remote Device Name', 'Remote Port', 'Remote Units', 'Remote SFP',
            'Cable Medium', 'Link Speed', 'Required Physical Patch Cable Type', 'Suggested Cable Color'
        ]

        try:
            with open(output_filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                
                for row in self.cabling_matrix:
                    writer.writerow([
                        row['local_device'], row['local_interface'], row['local_units'], row['local_sfp_type'],
                        row['remote_device'], row['remote_interface'], row['remote_units'], row['remote_sfp_type'],
                        row['cable_medium_type'], row['link_speed_capacity'],
                        row['physical_cable_type'], row['cable_color_code']
                    ])
            print(f"[+] SUCCESS: Cable matrix built successfully with port aggregation! Saved to: '{output_filename}'")
        except Exception as e:
            print(f"[-] Spreadsheet Generation Failed:\n{e}")


# =======================================================================================
# Pipeline Orchestration Runner
# =======================================================================================
if __name__ == "__main__":
    pass
    inventory_directory = "./device_vault"
    topology_engine = CablingLayoutGenerator(inventory_directory)
    topology_engine()
    topology_engine.export_to_csv("production_patch_guide.csv")
# =======================================================================================

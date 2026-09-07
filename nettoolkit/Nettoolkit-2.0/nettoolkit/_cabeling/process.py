"""class-based cabling topography layout generator with physical port aggregation """

import os
import csv
import re
import yaml

# ==============================================================================
# 1. OPTICS SPECIFICATION PROPERTY EXTRACTOR CLASS
# ==============================================================================
class CableSpecs:
    """
    Analyzes raw SFP hardware description strings to contextually extract
    and map individual physical media layer properties.
    """
    def __init__(self, sfp_type_str):
        self.sfp = str(sfp_type_str).upper() if sfp_type_str else 'MISSING OPTIC'
        
        # Populate all derived traits immediately using explicit, localized methods
        self.medium = self.derive_medium()
        self.speed = self.derive_speed()
        self.cable_type = self.derive_cable_type()
        self.color = self.derive_color()

    def derive_medium(self):
        """Isolates the core physical cable medium profile layer."""
        if self.sfp in ['MISSING OPTIC', 'MISSING REMOTE FILE']:
            return "Unknown Medium"
        if any(x in self.sfp for x in ['-T', '10G-T', ' COPPER', 'RJ45', '1000BASE-T']):
            return "Copper (Cat6/6A)"
        if any(x in self.sfp for x in ['DAC', 'TWINAX', 'PASSIVE COPPER', '10G-SFPP-CU']):
            return "Direct-Attach Copper (DAC)"
        if any(x in self.sfp for x in ['LR', 'LX', 'LH', 'EX', 'ZX', 'ER', 'ZR', 'SR', 'SX', 'FX', 'FIBER', 'OPTIC', 'QSFP']):
            return "Fiber-Optic"
        return "Unknown Medium"

    def derive_speed(self):
        """Captures the active operational link bandwidth capacity."""
        if self.sfp in ['MISSING OPTIC', 'MISSING REMOTE FILE']:
            return "Unknown Speed"
        if any(x in self.sfp for x in ['10G', 'LR', 'SR', 'ER', 'ZR']):
            return "10Gbps"
        if any(x in self.sfp for x in ['QSFP', '40G']):
            return "40Gbps"
        if '100G' in self.sfp:
            return "100Gbps"
        if any(x in self.sfp for x in ['1G', 'SX', 'LX', 'GIGABIT', '1000BASE']):
            return "1Gbps"
        return "1Gbps (Fallback)"

    def derive_cable_type(self):
        """Maps out the exact physical patch cord connector type."""
        if self.sfp in ['MISSING OPTIC', 'MISSING REMOTE FILE']:
            return "Unknown Cable Type"
        if "COPPER" in self.medium.upper():
            return "RJ45 Copper Patch Cable"
        if "DIRECT-ATTACH" in self.medium.upper():
            return "Direct-Attach Twinax Cable"
        if "QSFP" in self.sfp or "40G" in self.sfp:
            return "MPO to 4xLC Multi-Mode Breakout Fiber"
        if any(x in self.sfp for x in ['LR', 'LX', 'LH', 'EX', 'ZX', 'ER', 'ZR']):
            return "LC to LC Single-Mode Fiber (SMF)"
        if any(x in self.sfp for x in ['SR', 'SX', 'FX']):
            return "LC to SC Multi-Mode Fiber (MMF)" if 'SC' in self.sfp else "LC to LC Multi-Mode Fiber (MMF)"
        return "LC to LC Fiber Patch Cable" if "FIBER" in self.medium.upper() else "Verify Physical Slot Optic"

    def derive_color(self):
        """Assigns the standardized physical cable jacket or latch clip color coding."""
        if self.sfp in ['MISSING OPTIC', 'MISSING REMOTE FILE']:
            return "Unknown Color"
        if "COPPER" in self.medium.upper():
            return "Black"
        if "DIRECT-ATTACH" in self.medium.upper():
            return "Black / Twinax Grey"
        if any(x in self.sfp for x in ['LR', 'LX', 'LH', 'EX', 'ZX', 'ER', 'ZR']):
            return "Yellow"
        if any(x in self.sfp for x in ['SR', 'SX', 'FX', 'QSFP']):
            if any(x in self.sfp for x in ['OM3', '10GBASE-SR', 'QSFP', '40G']):
                return "Sky Blue (Aqua)"
            return "Orange"
        return "Verify Physical Cable Media"


# ==============================================================================
# 2. MASTER TOPOLOGY REPORT COMPILER CLASS
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

    def _strip_logical_unit(self, interface_name):
        """
        FIX: Safely strips logical unit extensions (.10) while preserving
        hardware channelised breakout ports (:1) completely intact.
        """
        if not interface_name:
            return ""
        if "." in str(interface_name):
            return str(interface_name).split(".")[0].strip()
        return str(interface_name).strip()

    def _get_remote_sfp_type(self, remote_host, physical_remote_port):
        """Queries the side-B telemetry file context safely to catch optic specifications."""
        tel_file = os.path.join(self.data_dir, f"{remote_host}_telemetrydata.yaml")
        if not os.path.exists(tel_file):
            tel_file = os.path.join(self.data_dir, f"{remote_host}_telemetrydata.yml")
            
        if not os.path.exists(tel_file):
            return "Missing Remote File"

        try:
            with open(tel_file, 'r') as f:
                remote_tel = yaml.safe_load(f) or {}
            
            interfaces_dict = remote_tel.get('interfaces_telemetry', {})
            
            # Walk through keys to locate the remote transceiver data block matching our physical port
            for r_key, r_metrics in interfaces_dict.items():
                if self._strip_logical_unit(r_key) == physical_remote_port:
                    optics = r_metrics.get('transceiver_optics', r_metrics.get('transceiver', {}))
                    if optics:
                        return optics.get('sfp_type', 'Missing Optic')
        except Exception:
            pass
        return "Missing Optic"

    def compile_matrix(self):
        """Loops through files to compile the physical port cabling records."""
        if not os.path.exists(self.data_dir):
            print(f"[-] Directory Path Error: Folder '{self.data_dir}' does not exist!")
            return []

        all_files = os.listdir(self.data_dir)
        device_baselines = set()
        
        # Isolate clean system hostnames using regex match parameters
        for f in all_files:
            if f.endswith('_devicedata.yaml') or f.endswith('_devicedata.yml'):
                hostname = re.sub(r'_devicedata\.yaml$', '', f, flags=re.IGNORECASE)
                hostname = re.sub(r'_devicedata\.yml$', '', hostname, flags=re.IGNORECASE)
                device_baselines.add(hostname)

        # Temporary storage map to aggregate sub-interfaces onto their base physical ports
        # Key format: (hostname, phys_local_port, remote_device, phys_remote_port) -> sets of units
        staged_links = {}

        for hostname in device_baselines:
            tel_file = os.path.join(self.data_dir, f"{hostname}_telemetrydata.yaml")
            if not os.path.exists(tel_file):
                tel_file = os.path.join(self.data_dir, f"{hostname}_telemetrydata.yml")

            if not os.path.exists(tel_file):
                continue

            try:
                with open(tel_file, 'r') as f:
                    tel_data = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"[!] Error reading file stream for host '{hostname}': {e}")
                continue

            interfaces_tel = tel_data.get('interfaces_telemetry', {})
            for raw_local_port, telemetry_metrics in interfaces_tel.items():
                if not isinstance(telemetry_metrics, dict):
                    continue
                    
                lldp = telemetry_metrics.get('lldp_topology', {})
                if not lldp or 'neighbor' not in lldp:
                    continue

                nbr = lldp['neighbor']
                remote_device = nbr.get('hostname', '').strip()
                raw_remote_port = nbr.get('interface', '').strip()

                if not remote_device or not raw_remote_port:
                    continue

                # --- 1. RESOLVE BASE PHYSICAL HARDWARE INTERFACE STRINGS ---
                # Preserves breakouts (xe-0/0/0:1) while stripping units (.10)
                phys_local_port = self._strip_logical_unit(raw_local_port)
                phys_remote_port = self._strip_logical_unit(raw_remote_port)

                # --- 2. DE-DUPLICATION CHECK AT THE PHYSICAL PORT LAYER ---
                connection_token = frozenset({(hostname, phys_local_port), (remote_device, phys_remote_port)})
                if connection_token in self.processed_connections:
                    continue 
                
                # Extract logical unit IDs to add to our tracking sets
                local_unit = raw_local_port.split(".")[-1] if "." in raw_local_port else "0"
                remote_unit = raw_remote_port.split(".")[-1] if "." in raw_remote_port else "0"

                # Define a unique lookup token for our localized aggregation staging map
                map_key = (hostname, phys_local_port, remote_device, phys_remote_port)
                
                if map_key not in staged_links:
                    staged_links[map_key] = {
                        'local_units': set(),
                        'remote_units': set(),
                        'metrics': telemetry_metrics
                    }
                    
                staged_links[map_key]['local_units'].add(local_unit)
                staged_links[map_key]['remote_units'].add(remote_unit)

        # --- 3. PROPS EXTRACTION AND OBJECT PACKING SWEEPS ---
        for (local_host, p_local, remote_host, p_remote), data in staged_links.items():
            # Add to the global processed connections checklist to eliminate mirror row duplicates
            connection_token = frozenset({(local_host, p_local), (remote_host, p_remote)})
            self.processed_connections.add(connection_token)

            telemetry_metrics = data['metrics']
            local_optics = telemetry_metrics.get('transceiver_optics', telemetry_metrics.get('transceiver', {}))
            local_sfp = local_optics.get('sfp_type', 'Missing Optic') if local_optics else 'Missing Optic'
            
            remote_sfp = self._get_remote_sfp_type(remote_host, p_remote)
            
            # Instantiate our object class to automatically resolve all parameters contextually!
            specs = CableSpecs(local_sfp)
            if specs.medium == "Unknown Medium" and remote_sfp not in ['Missing Optic', 'Missing Remote File']:
                specs = CableSpecs(remote_sfp)

            # Sort and clean logical units into readable string formats
            local_units_str = ",".join(sorted(list(data['local_units'])))
            remote_units_str = ",".join(sorted(list(data['remote_units'])))

            cable_record = {
                'local_device': local_host,
                'local_interface': p_local,
                'local_units': local_units_str,
                'local_sfp_type': local_sfp,
                'remote_device': remote_host,
                'remote_interface': p_remote,
                'remote_units': remote_units_str,
                'remote_sfp_type': remote_sfp,
                'cable_medium_type': specs.medium,
                'link_speed_capacity': specs.speed,
                'physical_cable_type': specs.cable_type,
                'cable_color_code': specs.color
            }
            self.cabling_matrix.append(cable_record)

        return self.cabling_matrix

    def export_to_csv(self, output_filename="cabling_layout_matrix.csv"):
        """Dumps compiled matrix entries out to a presentation-ready spreadsheet document."""
        if not self.cabling_matrix:
            print("[-] Analysis complete: No data collected. Please call compile_matrix() first.")
            return

        headers = [
            'Local Device Name', 'Physical Local Port', 'Local Units Active', 'Local SFP Model',
            'Remote Device Name', 'Physical Remote Port', 'Remote Units Active', 'Remote SFP Model',
            'Cable Medium', 'Link Speed', 'Required Physical Patch Cable Type', 'Required Cable Jacket Color'
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
# Pipeline Orchestration Runner (Standalone Script Execution Example Entry Point)
# =======================================================================================
if __name__ == "__main__":
    # Specify the workspace folder where your split YAML models are saved
    inventory_directory = "./device_vault"
    
    # 1. Instantiate the object-oriented topology layout processing machine
    topology_engine = CablingLayoutGenerator(inventory_directory)
    
    # 2. Run the high-speed file directory compilation sweeps
    topology_engine.compile_matrix()
    
    # 3. Generate the verified datacenter patching layout spreadsheet
    topology_engine.export_to_csv("production_patch_guide.csv")

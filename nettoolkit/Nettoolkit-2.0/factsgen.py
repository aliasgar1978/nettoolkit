


from nettoolkit.factsgen.device_config_parser import *
from nettoolkit.factsgen.device_telemetry_parser import *


from pathlib import Path



inventory_directory = Path("./device_vault")

for capture_file in inventory_directory.iterdir():
    if not capture_file.is_file(): continue
    if capture_file.suffix.lower() not in {".log", ".txt", ".cfg"}: continue
    try:
        extract_device_facts(capture_file)
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"[-] {capture_file.name}: {exc}")



# for capture_file in inventory_directory.iterdir():
#     if not capture_file.is_file(): continue
#     if capture_file.suffix.lower() not in {".log", ".txt", ".cfg"}: continue
#     try:
#         extract_device_telemetry_data(capture_file)
#     except (OSError, ValueError, KeyError, TypeError) as exc:
#         print(f"[-] {capture_file.name}: {exc}")


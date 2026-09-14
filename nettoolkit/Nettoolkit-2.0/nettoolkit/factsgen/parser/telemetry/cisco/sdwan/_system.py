# ------------------------------------------------------------------------------
import re


def parse_sdwan_system_flat(cmd_op):
    """Parses 'show sdwan system status' or 'show sdwan system' output.
    Returns a flat dictionary containing system performance and inventory details.
    """
    system_metrics = {}
    patterns = {
        "vmanage_ip": re.compile(r"^vManage\s+IP\s+([\d.]+)"),
        "system_ip": re.compile(r"^System\s+IP\s+([\d.]+)"),
        "site_id": re.compile(r"^Site\s+ID\s+(\d+)"),
        "domain_id": re.compile(r"^Domain\s+ID\s+(\d+)"),
        "personality": re.compile(r"^Personality\s+(\S+)"),
        "version": re.compile(r"^Version\s+(\S+)"),
        "uptime": re.compile(r"^Uptime\s+(.+)"),
        "cpu_user": re.compile(r"^CPU\s+user\s+(\d+)"),
        "cpu_system": re.compile(r"^CPU\s+system\s+(\d+)"),
        "memory_total": re.compile(r"^Memory\s+total\s+(\d+)"),
        "memory_used": re.compile(r"^Memory\s+used\s+(\d+)"),
    }

    for line in cmd_op:
        line_clean = line.strip()

        for key, pattern in patterns.items():
            if match := pattern.match(line_clean):
                system_metrics[key] = match.group(1).strip()
                break

    return system_metrics

# ----------------------------------------------------------------------

def parse_sdwan_software_by_version(cmd_op):
    """Parses 'show sdwan software' output.
    Returns a clean dictionary keyed directly by the 'version' string.
    """
    version_map = {}
    version_pattern = re.compile(
        r"^(?P<version>\S+)\s+"
        r"(?P<active>true|false)\s+"
        r"(?P<default>true|false)\s+"
        r"(?P<previous>true|false)\s+"
        r"(?P<confirmed>\S+)\s+"
        r"(?P<timestamp>\S+)"
    )

    for line in cmd_op:
        line_clean = line.strip()

        if (
            not line_clean
            or "---" in line_clean
            or "VERSION" in line_clean
            or "ACTIVE" in line_clean
        ):
            continue

        if match_ver := version_pattern.match(line_clean):
            data = match_ver.groupdict()
            version_key = data.pop("version")  # E.g., "17.3.1.0.102822"

            version_map[version_key] = data

    return version_map

import re


def parse_license_summary(cmd_op):
    """Parses 'show license summary' output.
    Returns a clean dictionary with top-level account metadata and a list of
    parsed license dictionaries.
    """
    parsed_data = {
        "smart_account": "none",
        "virtual_account": "none",
        "licenses": [],
    }

    account_pattern = re.compile(r"Smart Account\s*:\s*(.+)", re.IGNORECASE)
    virtual_pattern = re.compile(r"Virtual Account\s*:\s*(.+)", re.IGNORECASE)
    usage_pattern = re.compile(
        r"^(?P<entitlement_tag>.+?)\s{2,}(?P<count>\d+)\s+(?P<status>[A-Z ]+)"
    )

    for line in cmd_op:
        line_clean = line.strip()

        if (
            not line_clean
            or "---" in line_clean
            or "License Usage:" in line_clean
            or "Entitlement tag" in line_clean
        ):
            continue

        if match_acc := account_pattern.match(line_clean):
            account_raw = match_acc.group(1)
            parsed_data["smart_account"] = (
                account_raw.split("As of")[0].strip()
            )
            continue

        if match_virt := virtual_pattern.match(line_clean):
            parsed_data["virtual_account"] = match_virt.group(1).strip()
            continue

        if match_usage := usage_pattern.match(line_clean):
            parsed_data["licenses"].append(match_usage.groupdict())

    return parsed_data


# ------------------------------------------------------------------------------
def get_sdwan_system(cmd_op, *args):
    _dict = parse_sdwan_system_flat(cmd_op)
    _ = {}
    if _dict:
        _ = {'system': _dict}
    return {'op_dict': _ }

def get_sdwan_software(cmd_op, *args):
    _dict = parse_sdwan_software_by_version(cmd_op)
    _ = {}
    if _dict:
        _ = {'system': {'versions': _dict}}
    return {'op_dict': _ }

def get_license_summary(cmd_op, *args):
    _dict = parse_license_summary(cmd_op)
    _ = {}
    if _dict:
        _ = {'system': {'license': _dict}}
    return {'op_dict': _ }

# ------------------------------------------------------------------------------

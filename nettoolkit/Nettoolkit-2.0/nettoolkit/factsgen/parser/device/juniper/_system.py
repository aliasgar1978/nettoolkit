"""juniper system config parser from set config """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.fstr import blank_line
from nettoolkit.cmn.flist import add_to_list_if_missing
from nettoolkit.cmn.networking import get_juniper_pw_string
# ------------------------------------------------------------------------------

def parse_juniper_system_single_pass(cmd_op):
    """
    Parses Juniper system 'set' configurations in a single high-efficiency pass.
    Uses standard dictionaries while maintaining strict execution order.
    """
    raw_lines = cmd_op if isinstance(cmd_op, list) else cmd_op.splitlines()

    # Clean, lightweight standard dictionary blueprint (Insertion order is preserved natively!)
    sys_dict = {
        'identity': {'hostname': None, 'banner': None},
        'routing_metadata': {'bgp_as': None},
        'security': {'management_ip': None},
        'aaa': {'tacacs_servers': [], 'tacacs_key': None, 'tacacs_tcp_port': 49},
        'services': {'dns_servers': [], 'syslog_servers': [], 'ntp_servers': []}
    }
    
    # Context state dictionary to pass mutable flags to our handlers
    state_ctx = {
        'aaa_group_start': False
    }

    for line in raw_lines:
        line = line.strip()
        if not line or line.startswith("#") or line.startswith("!"):
            continue
            
        spl = line.split()
        # Fixed: Evaluates the FIRST element in the list against the 'set' string literal
        if not spl or spl[0] != "set":
            continue

        # Delegate parsing to dedicated sub-handlers
        _parse_identity_metadata(sys_dict, line, spl)
        _parse_network_services(sys_dict, line, spl)
        _parse_management_ip(sys_dict, line, spl)
        _parse_aaa_tacacs(sys_dict, line, spl, state_ctx)

    # Post-parsing cleanup: Remove unpopulated tracking nodes
    return _cleanup_juniper_placeholders(sys_dict)


# ==============================================================================
# Helper Sub-Handlers for Clean, Precise Code Separation
# ==============================================================================

def _parse_identity_metadata(sys_dict, line, spl):
    """Extracts hostnames, login announcements, and autonomous system metrics."""
    if line.startswith("set system host-name"):
        sys_dict['identity']['hostname'] = spl[-1]
    elif line.startswith("set system login announcement"):
        sys_dict['identity']['banner'] = " ".join(spl[4:]).strip('"')
    elif line.startswith("set routing-options autonomous-system"):
        try:
            sys_dict['routing_metadata']['bgp_as'] = int(spl[3])
        except (ValueError, IndexError):
            pass


def _parse_network_services(sys_dict, line, spl):
    """Extracts operational infrastructure elements like DNS, NTP, and Syslog lists."""
    if line.startswith("set system name-server"):
        add_to_list_if_missing(sys_dict['services']['dns_servers'], spl[-1])
    elif line.startswith("set system ntp server"):
        add_to_list_if_missing(sys_dict['services']['ntp_servers'], spl[-1])
    elif line.startswith("set system syslog host"):
        if len(spl) >= 5:
            add_to_list_if_missing(sys_dict['services']['syslog_servers'], spl[4])


def _parse_management_ip(sys_dict, line, spl):
    """Extracts system-wide management loopback or binding source addresses."""
    if line.startswith("set system ") and "source-address" in spl:
        sys_dict['security']['management_ip'] = spl[-1]


def _parse_aaa_tacacs(sys_dict, line, spl, state_ctx):
    """Extracts global TACACS settings and embedded server parameters."""
    if line.startswith("set system tacplus-server"):
        ip = spl[3]
        add_to_list_if_missing(sys_dict['aaa']['tacacs_servers'], ip)
        
        if 'port' in spl:
            try:
                sys_dict['aaa']['tacacs_tcp_port'] = int(spl[spl.index('port') + 1])
            except (ValueError, IndexError):
                pass
        if 'secret' in spl:
            try:
                sys_dict['aaa']['tacacs_key'] = get_juniper_pw_string(spl, spl.index('secret') + 1)
            except (ValueError, IndexError):
                pass


def _cleanup_juniper_placeholders(d):
    """Trims unpopulated tracking lists out to guarantee clean block-style YAML formatting."""
    if not d['identity']['hostname']: del d['identity']['hostname']
    if not d['identity']['banner']: del d['identity']['banner']
    if not d['identity']: del d['identity']
    
    if not d['routing_metadata']['bgp_as']: del d['routing_metadata']
    if not d['security']['management_ip']: del d['security']
    
    if not d['aaa']['tacacs_servers']: del d['aaa']
    else:
        if not d['aaa']['tacacs_key']: del d['aaa']['tacacs_key']
        if not d['aaa']['tacacs_tcp_port']: del d['aaa']['tacacs_tcp_port']
        
    if not d['services']['dns_servers']: del d['services']['dns_servers']
    if not d['services']['syslog_servers']: del d['services']['syslog_servers']
    if not d['services']['ntp_servers']: del d['services']['ntp_servers']
    if not d['services']: del d['services']
    
    return d


# ==============================================================================
# Pipeline Entry Point Hook
# ==============================================================================
def get_juniper_system_running(cmd_op, *args):
    return {'op_dict': parse_juniper_system_single_pass(cmd_op)}

def get_system(cmd_op, *args):
    return {'op_dict': parse_juniper_system_single_pass(cmd_op)}
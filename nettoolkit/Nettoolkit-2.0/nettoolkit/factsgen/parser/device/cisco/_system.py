"""cisco show running-config parser for system outputs """

# ------------------------------------------------------------------------------
from nettoolkit.cmn.flist import add_to_list_if_missing
from nettoolkit.addressing import addressing
from nettoolkit.crypt.cpw import type7_dec
# ------------------------------------------------------------------------------

def parse_system_single_pass(cmd_op):
    """
    Parses global system configurations in a single pass.
    Delegates parsing tasks to concise, dedicated sub-handlers.
    """
    # Initialize our structured schema blueprint
    sys_dict = {
        'identity': {'hostname': None, 'banner': None},
        'routing_metadata': {'bgp_as': None},
        'security': {'ca_certificate': None},
        'aaa': {'tacacs_servers': [], 'tacacs_key': None, 'tacacs_tcp_port': None},
        'services': {'dns_servers': [], 'syslog_servers': [], 'ntp_servers': []}
    }
    
    # State tracking variables passed via a mutable dictionary context
    state_ctx = {
        'ca_start': False,
        'cert_buffer': [],
        'aaa_group_start': False
    }

    for line in cmd_op:
        raw_line = line
        line = line.strip()
        if not line or line == "!":
            if state_ctx['aaa_group_start'] and line == "!":
                state_ctx['aaa_group_start'] = False  # Close group block safely
            continue

        spl = line.split()
        if not spl:
            continue

        # Delegate parsing to dedicated sub-handlers
        _parse_identity_metadata(sys_dict, line)
        _parse_ca_certificates(sys_dict, line, raw_line, state_ctx)
        _parse_network_services(sys_dict, line, spl)
        _parse_aaa_tacacs(sys_dict, line, spl, state_ctx)

    # Post-parsing cleanup: Remove unpopulated tracking nodes
    return _cleanup_system_placeholders(sys_dict)


# ==============================================================================
# Helper Sub-Handlers for Clean, Precise Code Separation
# ==============================================================================

def _parse_identity_metadata(sys_dict, line):
    """Extracts top-level identity attributes and BGP global routing process metadata."""
    if line.startswith("hostname "):
        sys_dict['identity']['hostname'] = line.split(" ", 1)[-1].strip()
    elif line.startswith("banner exec "):
        sys_dict['identity']['banner'] = line
    elif line.startswith("router bgp "):
        sys_dict['routing_metadata']['bgp_as'] = int(line.split()[-1])


def _parse_ca_certificates(sys_dict, line, raw_line, state_ctx):
    """Safely extracts cryptographic CA certificates spanning multiple text lines."""
    if line.startswith("certificate ca 01"):
        state_ctx['ca_start'] = True
        return

    if state_ctx['ca_start']:
        if line.startswith("quit"):
            state_ctx['ca_start'] = False
            sys_dict['security']['ca_certificate'] = "\n".join(state_ctx['cert_buffer'])
        else:
            state_ctx['cert_buffer'].append(raw_line.rstrip())


def _parse_network_services(sys_dict, line, spl):
    """Extracts network operational services like DNS, NTP, and Syslog."""
    if line.startswith("ip name-server "):
        for ip in spl[2:]:
            add_to_list_if_missing(sys_dict['services']['dns_servers'], ip)
            
    elif line.startswith("ntp server "):
        for ip in spl[2:]:
            add_to_list_if_missing(sys_dict['services']['ntp_servers'], ip)
            
    elif line.startswith("logging "):
        for token in spl[1:]:
            try:
                addressing(token)  # Validates if token matches a real IP address format
                add_to_list_if_missing(sys_dict['services']['syslog_servers'], token)
            except Exception:
                continue


def _parse_aaa_tacacs(sys_dict, line, spl, state_ctx):
    """Extracts standard global TACACS settings and embedded server-private structures."""
    # Global legacy configurations
    if line.startswith("tacacs-server host "):
        add_to_list_if_missing(sys_dict['aaa']['tacacs_servers'], spl[2])
        
    elif line.startswith("tacacs-server ") and "key" in line:
        key_idx = spl.index("key") + 1
        if key_idx < len(spl):
            if spl[key_idx] == "7" and key_idx + 1 < len(spl):
                sys_dict['aaa']['tacacs_key'] = type7_dec(spl[key_idx + 1])
            else:
                sys_dict['aaa']['tacacs_key'] = spl[key_idx]
                
    elif line.startswith("tacacs-server ") and "port" in line:
        sys_dict['aaa']['tacacs_tcp_port'] = int(spl[spl.index("port") + 1])

    # Embedded AAA server group configurations
    elif line.startswith("aaa group server tacacs"):
        state_ctx['aaa_group_start'] = True
        return

    if state_ctx['aaa_group_start']:
        if spl[0] == 'server-private':
            add_to_list_if_missing(sys_dict['aaa']['tacacs_servers'], spl[1])
        if 'key' in spl:
            k_idx = spl.index('key') + 1
            if k_idx < len(spl):
                if spl[k_idx] == '7' and k_idx + 1 < len(spl):
                    sys_dict['aaa']['tacacs_key'] = type7_dec(spl[k_idx + 1])
                else:
                    sys_dict['aaa']['tacacs_key'] = spl[k_idx]
        if 'port' in spl:
            sys_dict['aaa']['tacacs_tcp_port'] = int(spl[spl.index('port') + 1])


def _cleanup_system_placeholders(d):
    """Trims empty initialization fields out to guarantee tight YAML formatting."""
    if not d['identity']['hostname']: del d['identity']['hostname']
    if not d['identity']['banner']: del d['identity']['banner']
    if not d['identity']: del d['identity']
    
    if not d['routing_metadata']['bgp_as']: del d['routing_metadata']
    if not d['security']['ca_certificate']: del d['security']
    
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
def get_system(cmd_op, *args):
    return {'op_dict': parse_system_single_pass(cmd_op)}
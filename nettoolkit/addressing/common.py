import os, csv

# ----------------------------------------------------------------------


def load_active_ips(file_path):
    """
    Streams a single CSV file and extracts all successfully pinging IPs.
    Returns an empty set if the file does not exist.
    """
    active_ips = set()
    
    if not os.path.exists(file_path):
        return active_ips

    with open(file_path, mode='r', newline='', encoding='utf-8') as f:
        # DictReader allows us to access columns by their name directly
        reader = csv.DictReader(f)
        
        for row in reader:
            ip = row.get('ip', '').strip()
            status = row.get('ping_results', '').strip().lower()
            
            # Add to set if IP exists and status is explicitly true
            if ip and status in ('true', '1'):
                active_ips.add(ip)
                
    return active_ips


def compare_two_ping_files(pre_file, post_file):
    """
    Compares a pre-change and post-change CSV file.
    Calculates differences instantly using native set arithmetic.
    """
    # 1. Parse both files into memory-efficient sets
    pre_active = load_active_ips(pre_file)
    post_active = load_active_ips(post_file)
    
    # 2. Compute differences using high-speed native set operations
    dropped_ips = pre_active.difference(post_active)
    new_ips = post_active.difference(pre_active)
    
    # 3. Print a clean, well-formatted terminal report
    border = "=" * 60
    filename_display = os.path.basename(pre_file)
    
    print(f"\n📊 COMPARISON REPORT FOR: {filename_display}")
    print(border)
    
    if not dropped_ips and not new_ips:
        print("[+] Perfect Match: No changes detected.")
        print(border)
        return

    if dropped_ips:
        print("🔴 DROPPED (Pinging BEFORE, but NOT responding AFTER):")
        # Sorting the set ensures the IP addresses are printed in logical order
        print(", ".join(sorted(dropped_ips)))
        print(border)
        
    if new_ips:
        print("🟢 NEW (NOT responding BEFORE, but started responding AFTER):")
        print(", ".join(sorted(new_ips)))
        print(border)


# ====================================================================================
# Replacement of below
# def sort_dataframe_on_subnet(df, col, ascending=True):
# ====================================================================================
def sort_subnet_list(prefixes, ascending=True):
    """Sorts a list of subnet strings in place.

    Args:
        prefixes (list): List of subnet strings (e.g., ['10.0.0.0/24', '192.168.1.0/24'])
        ascending (bool, optional): Sort order. Defaults to True.

    Returns:
        list: The sorted list of subnets.
    """
    def get_sort_key(subnet_str):
        try:
            # 1. Split IP from prefix (e.g., '192.168.1.0/24' -> '192.168.1.0', '24')
            if '/' in subnet_str:
                ip_str, prefix_str = subnet_str.split('/', 1)
                prefix = int(prefix_str)
            else:
                ip_str, prefix = subnet_str, 32

            # 2. Convert IP octets to a tuple of integers (e.g., (192, 168, 1, 0))
            octets = tuple(int(x) for x in ip_str.split('.'))

            # 3. Return a combined sorting key: (octets, prefix)
            return octets + (prefix,)
        except (ValueError, AttributeError):
            # Handle empty or malformed strings gracefully by forcing them to the end
            return (256, 256, 256, 256, 32)

    # Sort the list using the custom integer-tuple key
    return sorted(prefixes, key=get_sort_key, reverse=not ascending)
# ====================================================================================

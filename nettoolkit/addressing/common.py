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

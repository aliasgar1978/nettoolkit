# pip install pandas openpyxl pyyaml

import re
import pandas as pd
import yaml

def clean_key(val):
    """Converts Excel headers into clean, lower_snake_case YAML keys."""
    return str(val).strip().lower().replace(" ", "_")

def parse_multiline_value(val):
    """Handles multiline strings or list items from the Excel var tab."""
    if pd.isna(val):
        return ""
    
    val_str = str(val).strip()
    
    # Check if it's a multiline value or a common comma-separated list
    if '\n' in val_str:
        return [line.strip() for line in val_str.split('\n') if line.strip()]
    elif ',' in val_str and not re.match(r'^\d[\d,.]*$', val_str): 
        return [item.strip() for item in val_str.split(',') if item.strip()]
        
    return val

def migrate_and_purge_sequence(excel_path, yaml_output_path):
    excel_file = pd.ExcelFile(excel_path)
    
    master_structure = {
        "system_var": {},
        "devices": {}
    }
    
    # 1. PARSE THE 'VAR' TAB INTO system_var
    if 'var' in excel_file.sheet_names:
        print("[*] Migrating 'var' tab...")
        var_df = pd.read_excel(excel_path, sheet_name='var')
        var_df.columns = [clean_key(col) for col in var_df.columns]
        
        if 'variable' in var_df.columns and 'value' in var_df.columns:
            for _, row in var_df.iterrows():
                var_name = str(row['variable']).strip()
                if pd.isna(row['variable']) or not var_name:
                    continue
                master_structure["system_var"][var_name] = parse_multiline_value(row['value'])

    # 2. PARSE CONFIGURATION TABS (SORT & STRIP INT_NUMBER)
    for sheet_name in excel_file.sheet_names:
        if sheet_name == 'var':
            continue
            
        feature_name = clean_key(sheet_name)
        print(f"[*] Processing and sorting tab: {sheet_name}")
        
        df = pd.read_excel(excel_path, sheet_name=sheet_name)
        df.columns = [clean_key(col) for col in df.columns]
        
        # Sort by int_number first while it is still a dataframe
        if 'int_number' in df.columns:
            # Coerce to numeric so sorting acts as numbers (1, 2, 10) instead of strings
            df['int_number'] = pd.to_numeric(df['int_number'], errors='coerce')
            df = df.sort_values(by='int_number', ascending=True)
        
        # Drop completely empty columns and drop the old structural 'filter' column
        cleaned_df = df.dropna(axis=1, how='all')
        if 'filter' in cleaned_df.columns:
            cleaned_df = cleaned_df.drop(columns=['filter'])
            
        # Convert to a dictionary list structure
        records = cleaned_df.to_dict(orient='records')
        
        # Clean up records and STRIP the 'int_number' key entirely
        cleaned_records = []
        for rec in records:
            cleaned_rec = {}
            for k, v in rec.items():
                if k == 'int_number': 
                    continue # Skip and delete the int_number key
                cleaned_rec[k] = v if not pd.isna(v) else ""
            cleaned_records.append(cleaned_rec)
        
        # Store directly under devices in its pre-sorted state
        master_structure["devices"][feature_name] = cleaned_records

    # 3. WRITE TO COMBINED YAML FILE
    with open(yaml_output_path, 'w') as f:
        # sort_keys=False ensures YAML keeps the exact list order we built
        yaml.dump(master_structure, f, default_flow_style=False, sort_keys=False)
        
    print(f"\n[+] Success! Pre-sorted configuration saved without sequence numbers to: {yaml_output_path}")

# ==========================================
# RUN THE MIGRATION
# ==========================================
EXCEL_INPUT = "network_data.xlsx"
COMBINED_YAML = "network_data.yaml"

migrate_and_purge_sequence(EXCEL_INPUT, COMBINED_YAML)



# ### Reading script #####
# import yaml

# with open('network_data.yaml', 'r') as file:
#     config = yaml.safe_load(file)

# # The data arrives exactly in the sequence it was sorted during migration
# for interface in config['devices']['interfaces']:
#     # Pure configuration parameters, no sequence or database artifacts
#     print(f"Configuring {interface['name']} - Description: {interface['description']}")



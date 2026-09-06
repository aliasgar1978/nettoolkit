"""jinja2 template structural syntax validation scanner with whitespace control support """

# ---------------------------------------------------------------------------------------
import re

from nettoolkit.cmn.fstr import find_multi
from nettoolkit.cmn.fio import file_to_list
# ---------------------------------------------------------------------------------------

def get_conditions(jinja_file):
    """get all conditional statements from jinja file

    Args:
        jinja_file (str): jinja template file

    Returns:
        dict: dictionary with list of jinja variables, conditions, and loops.
    """	
    d = {'conditions': set(), 'loops': set(), 'variables': set()}
    lns = file_to_list(jinja_file)
        
    for ln in lns:
        l_strip = ln.strip()
        
        # Regex checks look for optional spaces \s* and optional dashes -? after the open brace
        if re.search(r'^{%\s*-?\s*for\b', l_strip):
            d['loops'].add(ln)
        elif re.search(r'^{%\s*-?\s*(if|elif|else)\b', l_strip):
            d['conditions'].add(ln)
        elif re.search(r'^{%\s*-?\s*set\b', l_strip):
            d['variables'].add(ln)
            
    return d


def get_variables(jinja_file):
    """get all jinja variables defined in jinja file

    Args:
        jinja_file (str): jinja template file

    Returns:
        set: set of jinja variables
    """	
    conds = set()
    lns = file_to_list(jinja_file)
        
    for ln in lns:
        starts, ends = [], []
        current_start_pointer = 0
        current_end_pointer = 0
        
        for i in range(20):
            start = find_multi(ln, '{{', start=current_start_pointer, count=None, index=True, beginwith=False)
            end   = find_multi(ln, '}}', start=current_end_pointer, count=None, index=True, beginwith=False)
            
            if start == -1: 
                break
                
            starts.append(start)
            ends.append(end)
            
            current_start_pointer = start + 2
            current_end_pointer = end + 2

        if not starts: 
            continue
            
        for s, e in zip(starts, ends):
            cond = ln[s:e+2]
            conds.add(cond)
            
    return conds


# ==============================================================================
# SANITY CHECK: CORE SYNTAX BLOCK BALANCE VERIFIER (WITH WHITESPACE CONTROL)
# ==============================================================================
def verify_jinja_syntax_sanity(jinja_file):
    """
    Scans the Jinja2 file and cross-references block open tags against closures.
    Supports whitespace control modifiers (`-`) and varying space definitions.
    """
    lns = file_to_list(jinja_file)

    report = {'errors': [], 'is_valid': True}
    
    # Balance stacks record tuples of (line_number, line_content)
    if_stack = []
    for_stack = []
    macro_stack = []  

    for line_num, ln in enumerate(lns, 1):
        l_strip = ln.strip()
        
        # 1. --- Match Open/Close Conditional Blocks ---
        if re.search(r'^{%\s*-?\s*if\b', l_strip):
            if_stack.append((line_num, l_strip))
            
        elif re.search(r'^{%\s*-?\s*endif\s*-?%}', l_strip):
            if if_stack:
                if_stack.pop()
            else:
                report['errors'].append(f"Line {line_num}: Orphaned closure '{l_strip}' found with no matching open 'if' block.")

        # 2. --- Match Open/Close Iteration Loops ---
        elif re.search(r'^{%\s*-?\s*for\b', l_strip):
            for_stack.append((line_num, l_strip))
            
        elif re.search(r'^{%\s*-?\s*endfor\s*-?%}', l_strip):
            if for_stack:
                for_stack.pop()
            else:
                report['errors'].append(f"Line {line_num}: Orphaned closure '{l_strip}' found with no matching open 'for' loop.")

        # 3. --- Track Open/Close Macro Statements ---
        if re.search(r'^{%\s*-?\s*macro\b', l_strip):
            macro_stack.append((line_num, l_strip))
            
        elif re.search(r'^{%\s*-?\s*endmacro\s*-?%}', l_strip):
            if macro_stack:
                macro_stack.pop()
            else:
                report['errors'].append(f"Line {line_num}: Orphaned closure '{l_strip}' found with no matching open 'macro' block.")

    # Evaluate leftovers remaining inside our tracking stacks
    while if_stack:
        err_line, err_content = if_stack.pop()
        report['errors'].append(f"Line {err_line}: Unclosed conditional statement block! Missing 'endif' for statement: '{err_content}'")
        
    while for_stack:
        err_line, err_content = for_stack.pop()
        report['errors'].append(f"Line {err_line}: Unclosed iteration loop block! Missing 'endfor' for statement: '{err_content}'")

    while macro_stack:
        err_line, err_content = macro_stack.pop()
        report['errors'].append(f"Line {err_line}: Unclosed template macro block! Missing 'endmacro' for statement: '{err_content}'")

    if report['errors']:
        report['is_valid'] = False
        
    return report

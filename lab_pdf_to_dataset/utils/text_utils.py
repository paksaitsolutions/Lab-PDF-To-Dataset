import re

def extract_value_from_line(line, min_val, max_val):
    """
    Extracts a numeric value from a line that likely falls within min_val and max_val.
    Avoids ranges (e.g. 10-20, 10 - 20) and ignores numbers outside logical bounds.
    Returns the valid number found right-most in the line (heuristic).
    """
    # Find all numbers (integers or floats)
    # We use a pattern that allows for surrounding whitespace or non-digit chars
    # but captures the number itself.
    numbers_iter = re.finditer(r'(\d+(\.\d+)?)', line)
    
    candidates = []
    
    for match in numbers_iter:
        num_str = match.group(1)
        start, end = match.span()
        
        # Context checks to detect if this number is part of a reference range
        # Look behind (pre_context) and ahead (post_context)
        
        # 1. Check if it's part of a range like "10-20" or "10 - 20"
        # Check char immediately before (ignoring spaces)
        pre_slice = line[:start].rstrip()
        post_slice = line[end:].lstrip()
        
        is_range_part = False
        
        # Check for preceding dash/hyphen
        if pre_slice and pre_slice[-1] in ['-', '–', '~']:
             is_range_part = True
             
        # Check for succeeding dash/hyphen
        if post_slice and post_slice[0] in ['-', '–', '~']:
             is_range_part = True
             
        if pre_slice.lower().endswith(" to"):
            is_range_part = True
        if post_slice.lower().startswith("to "):
            is_range_part = True

        # Check if number is immediately preceded by a letter (e.g. mm3, T3, CD4)
        # This prevents extracting parts of units or test names as values.
        # But allow if there is a space (e.g. 'Hemoglobin 14.5')
        if start > 0 and line[start-1].isalpha():
            continue

        if is_range_part:
            continue
            
        try:
            val = float(num_str)
            # Check if value is within logical bounds for this test
            if min_val <= val <= max_val:
                candidates.append(num_str)
        except:
            continue
            
    if candidates:
        # Return the last valid candidate (heuristic: result is usually column on the right)
        return candidates[-1]
        
    return None

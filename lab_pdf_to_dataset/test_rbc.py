import re

text = """Total RBC                4 - 6              x10^12/l      3.2"""

pattern = r'(?:Total\s+)?(?:Red Blood Cell|RBC).*?\*10[^\n]*?([0-9]+\.?[0-9]*)'
match = re.search(pattern, text, re.IGNORECASE)
print(f"Pattern 1 match: {match}")

pattern2 = r'(?:Total\s+)?(?:Red Blood Cell|RBC).*?x10[^\n]*?([0-9]+\.?[0-9]*)'
match2 = re.search(pattern2, text, re.IGNORECASE)
print(f"Pattern 2 match: {match2}")
if match2:
    print(f"Extracted value: {match2.group(1)}")

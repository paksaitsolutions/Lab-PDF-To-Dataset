import re

sample2 = """
Bilirubin Total         0.20 - 1.00     mg/dl           0.9
"""

# Test pattern
pattern = r'(?:Bilirubin\s+Total|Total\s+Bilirubin)[^\n]{0,300}?([0-9]+\.?[0-9]+)\s*(?:mg/d[Ll]|U/L|g/d[Ll]|%)'
matches = list(re.finditer(pattern, sample2, re.IGNORECASE | re.DOTALL))

print(f"Found {len(matches)} matches:")
for i, match in enumerate(matches):
    print(f"Match {i+1}: '{match.group(1)}' at position {match.start()}-{match.end()}")
    print(f"Full match: '{match.group(0)}'")

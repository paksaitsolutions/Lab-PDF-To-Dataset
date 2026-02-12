# TFT Extractor
import re
from extractors.cbc_extractor import extract_basic_info
from utils.text_utils import extract_value_from_line


def extract_tft(text):
    data = extract_basic_info(text)

    for test in ["T3", "T4", "TSH", "Free T3", "Free T4"]:
        data[test] = ""

    lines = text.split('\n')

    test_defs = [
        (r'\btotal\s*t3\b|\bt3\b|triiodothyronine', 'T3', 0.1, 10.0, ['free']),
        (r'\btotal\s*t4\b|\bt4\b|thyroxine', 'T4', 0.5, 30.0, ['free']),
        (r'\btsh\b|thyroid\s*stimulating\s*hormone|t\s*s\s*h', 'TSH', 0.01, 200.0, []),
        (r'\bfree\s*t3\b|\bft3\b', 'Free T3', 0.5, 30.0, []),
        (r'\bfree\s*t4\b|\bft4\b', 'Free T4', 0.1, 30.0, []),
    ]

    tests_found = []
    for i, line in enumerate(lines):
        line_lower = line.lower()
        for pattern, test_name, min_val, max_val, exclusions in test_defs:
            if re.search(pattern, line_lower):
                if any(excl in line_lower for excl in exclusions):
                    continue
                if not any(t[0] == test_name for t in tests_found):
                    tests_found.append((test_name, min_val, max_val, i, line))
                break

    if not tests_found:
        return data

    for test_name, min_val, max_val, _, line in tests_found:
        val = extract_value_from_line(line, min_val, max_val)
        if val:
            data[test_name] = val

    missing_tests = [(t, mn, mx, ln) for t, mn, mx, ln, _ in tests_found if not data[t]]

    if missing_tests:
        test_line_nums = {t[3] for t in tests_found}
        start_line = tests_found[0][3]
        end_line = tests_found[-1][3] + 3

        next_line_values = []
        for i in range(start_line, min(end_line, len(lines))):
            if i in test_line_nums:
                continue

            line = lines[i]
            if len(line) < 20:
                continue

            right_part = line[-40:]
            numbers = re.findall(r'\b(\d+\.?\d*)\b', right_part)
            if numbers:
                num = numbers[-1]
                if not re.search(r'\d+\.?\d*\s*[-–]\s*' + re.escape(num) + r'(?!\d)', right_part) and \
                   not re.search(r'(?<!\d)' + re.escape(num) + r'\s*[-–]\s*\d+\.?\d*', right_part):
                    next_line_values.append(num)

        for idx, (test_name, min_val, max_val, _) in enumerate(missing_tests):
            if idx < len(next_line_values):
                try:
                    val = float(next_line_values[idx])
                    if min_val <= val <= max_val:
                        data[test_name] = next_line_values[idx]
                except Exception:
                    pass

    return data

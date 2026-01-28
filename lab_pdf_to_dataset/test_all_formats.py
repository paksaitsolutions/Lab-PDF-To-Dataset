import sys
sys.path.insert(0, '.')

from extractors.lft_extractor import extract_lft
from extractors.rft_extractor import extract_rft

# Sample 1: Format with RESULT column and date
sample1 = """
LIVER FUNCTION TESTS                                    Specimen: Serum
TEST                    REFERENCE RANGE UNIT            RESULT
                                                        1225-7/01-Dec-2025
SGPT (ALT)              5 - 41          U/L             34

RENAL FUNCTION TESTS                                    Specimen: Serum
TEST                    REFERENCE RANGE UNIT            RESULT
                                                        1225-7/01-Dec-2025
Creatinine              0.60 - 1.30     mg/dL           1.3
"""

# Sample 2: Format with RESULT header and date
sample2 = """
LIVER FUNCTION TESTS                                    RESULT
TEST                    NORMAL RANGE    UNIT            4631
                                                        29-Jan-2025 8:53 am
Bilirubin Total         0.20 - 1.00     mg/dl           0.9
SGPT (ALT)              See Below*      U/L             28
                        * M = 0 - 40
                        F = 0 - 31
SGOT (AST)              Upto - 40       U/L             36
Alkaline Phosphatase    See Below*      U/L             268
                        * Adults: Less than 258
Total Protein           6.40 - 8.30     g/dl            7.6
Albumin                 3.40 - 4.80     %               4.0
"""

# Sample 3: Format with date column header
sample3 = """
Liver Function Test
Tests                   Reference Value Unit            1015-29-04
                                                        29-Apr-2024
Bilirubin Total         0.1 - 1.0       mg/dl           0.7
Bilirubin Conjugated    Less Than 0.5   mg/dl           0.3
Bilirubin Unconjugated  0.1 - 1.0       mg/dl           0.4
S.G.P.T (A.L.T)         Less Than 40    U/L             37
S.G.O.T (A.S.T)         Less Than 40    U/L             46
Alkaline Phosphatase    46 - 302        U/L             210
Total Protein           6.0 - 8.5       g/dl            7.4
Albumin                 3.5 - 5.2       g/dl            4.2
"""

# Sample 4: Format with large result values on right
sample4 = """
Patient Name: HAFIZ MUBASHAR
Age / Sex: 20 Years / Male

LIVER FUNCTION TESTS (LFT)

Total Bilirubin         Adults: 0.1 - 1.2               0.9 mg/dL
S.G.P.T. (ALT)          Male: <45                       47 U/L
                        Female: <34
S.G.O.T (AST)           Male: <35                       41 U/L
                        Female: <31
Alkaline Phosphatase    Female: 64 - 306                210 U/L
                        Male: 80 - 306
"""

print("="*70)
print("Testing Sample 1 (RESULT column with date)")
print("="*70)
result1_lft = extract_lft(sample1)
result1_rft = extract_rft(sample1)
print(f"LFT - ALT: {result1_lft['ALT']} (expected: 34)")
print(f"RFT - Creatinine: {result1_rft['Creatinine']} (expected: 1.3)")

print("\n" + "="*70)
print("Testing Sample 2 (RESULT header with date)")
print("="*70)
result2 = extract_lft(sample2)
print(f"Total Bilirubin: {result2['Total Bilirubin']} (expected: 0.9)")
print(f"ALT: {result2['ALT']} (expected: 28)")
print(f"AST: {result2['AST']} (expected: 36)")
print(f"ALP: {result2['ALP']} (expected: 268)")
print(f"Total Protein: {result2['Total Protein']} (expected: 7.6)")
print(f"Albumin: {result2['Albumin']} (expected: 4.0)")

print("\n" + "="*70)
print("Testing Sample 3 (Date column header)")
print("="*70)
result3 = extract_lft(sample3)
print(f"Total Bilirubin: {result3['Total Bilirubin']} (expected: 0.7)")
print(f"Direct Bilirubin: {result3['Direct Bilirubin']} (expected: 0.3)")
print(f"Indirect Bilirubin: {result3['Indirect Bilirubin']} (expected: 0.4)")
print(f"ALT: {result3['ALT']} (expected: 37)")
print(f"AST: {result3['AST']} (expected: 46)")
print(f"ALP: {result3['ALP']} (expected: 210)")
print(f"Total Protein: {result3['Total Protein']} (expected: 7.4)")
print(f"Albumin: {result3['Albumin']} (expected: 4.2)")

print("\n" + "="*70)
print("Testing Sample 4 (Large values on right)")
print("="*70)
result4 = extract_lft(sample4)
print(f"Total Bilirubin: {result4['Total Bilirubin']} (expected: 0.9)")
print(f"ALT: {result4['ALT']} (expected: 47)")
print(f"AST: {result4['AST']} (expected: 41)")
print(f"ALP: {result4['ALP']} (expected: 210)")

print("\n" + "="*70)
print("Test Complete")
print("="*70)

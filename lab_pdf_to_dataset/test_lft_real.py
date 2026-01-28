import sys
sys.path.insert(0, '.')

from extractors.lft_extractor import extract_lft

sample_lft = """
Booking (Ref) #: 10488
Patient Name: HAFIZ MUBASHAR
Age / Sex: 20 Years / Male
Mobile: 00000000000
Consultant: Self

LIVER FUNCTION TESTS (LFT)

Total Bilirubin          Adults: 0.1 - 1.2         0.9 mg/dL
                         Newborn: <10

S.G.P.T. (ALT)          Male: <45                  47 U/L
                        Female: <34

S.G.O.T (AST)           Male: <35                  41 U/L
                        Female: <31

Alkaline Phosphatase    Female: 64 - 306           210 U/L
                        Male: 80 - 306
"""

result = extract_lft(sample_lft)
print("LFT Extraction Test:")
print(f"Name: {result['Name']}")
print(f"Age: {result['Age']}")
print(f"Gender: {result['Gender']}")
print(f"Total Bilirubin: {result['Total Bilirubin']}")
print(f"ALT: {result['ALT']}")
print(f"AST: {result['AST']}")
print(f"ALP: {result['ALP']}")
print(f"Albumin: {result['Albumin']}")
print(f"Total Protein: {result['Total Protein']}")

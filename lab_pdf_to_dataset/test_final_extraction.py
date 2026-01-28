"""
Test the updated extractors with sample lab report text
"""
import sys
sys.path.insert(0, '.')

from extractors.cbc_extractor import extract_cbc
from extractors.rft_extractor import extract_rft

# Sample text from the actual PDF
sample_cbc_text = """
CHUGHTAI's Plus
LAHORE LAB

Patient Name:                                Registration Location:
Safia Bibi .                                 CC JINNAH HOSPITAL LHR

Age/Sex:                                     Registration Date:
73 Yr(s) / Female                            23-Feb-2024 12:42 pm

Contact No: 03057145066

Blood C/E (Complete, CBC)

Tests                    Reference Value    Unit           1001-23-02
                                                          23-Feb-2024

Hb                       11.5 - 16          g/dl          9.5
Total RBC                4 - 6              x10^12/l      3.2
HCT                      36 - 46            %             29
MCV                      75 - 95            fl            92
MCH                      26 - 32            pg            29
MCHC                     30 - 35            g/dl          31
Platelet Count           150 - 400          x10^9/l       357
WBC Count (TLC)          4 - 11             x10^9/l       6.0
Neutrophils              40 - 75            %             80
Lymphocytes              20 - 50            %             15
Monocytes                02 - 10            %             04
Eosinophils              01 - 06            %             01
"""

sample_rft_text = """
CHUGHTAI's Plus
LAHORE LAB

Patient Name:                                Registration Location:
Ahmed Khan .                                 CC JINNAH HOSPITAL LHR

Age/Sex:                                     Registration Date:
45 Yr(s) / Male                              23-Feb-2024 14:30 pm

Renal Function Test (RFT)

Tests                    Reference Value    Unit           Result

Urea                     15 - 45            mg/dL         35.5
BUN                      7 - 20             mg/dL         16.5
Creatinine               0.6 - 1.2          mg/dL         1.1
GFR                      >60                mL/min        85.0
Uric Acid                3.5 - 7.2          mg/dL         5.8
"""

print("=" * 60)
print("Testing CBC Extraction")
print("=" * 60)
cbc_result = extract_cbc(sample_cbc_text)
print(f"Name: {cbc_result['Name']}")
print(f"Age: {cbc_result['Age']}")
print(f"Gender: {cbc_result['Gender']}")
print(f"HB: {cbc_result['HB']}")
print(f"RBC: {cbc_result['RBC']}")
print(f"HCT: {cbc_result['HCT']}")
print(f"Neutrophils: {cbc_result['Neutrophils']}")
print(f"Lymphocytes: {cbc_result['Lymphocytes']}")

print("\n" + "=" * 60)
print("Testing RFT Extraction")
print("=" * 60)
rft_result = extract_rft(sample_rft_text)
print(f"Name: {rft_result['Name']}")
print(f"Age: {rft_result['Age']}")
print(f"Gender: {rft_result['Gender']}")
print(f"Urea: {rft_result['Urea']}")
print(f"BUN: {rft_result['BUN']}")
print(f"Creatinine: {rft_result['Creatinine']}")
print(f"GFR: {rft_result['GFR']}")
print(f"Uric Acid: {rft_result['Uric Acid']}")

print("\n" + "=" * 60)
print("✅ All tests completed!")
print("=" * 60)

import sys
sys.path.insert(0, '.')

from extractors.rft_extractor import extract_rft

# Format 1: RESULT column with date
format1 = """
RENAL FUNCTION TESTS                                    Specimen: Serum
TEST                    REFERENCE RANGE UNIT            RESULT
                                                        1225-7/01-Dec-2025
Creatinine              0.60 - 1.30     mg/dL           1.3
Urea                    15 - 50         mg/dL           35
BUN                     7 - 23          mg/dL           16.3
"""

# Format 2: Detailed format with descriptions
format2 = """
Booking (Ref) #: 10553
Patient Name: RABIA
Age / Sex: 27 Years / Female
Mobile: 00000000000
Consultant: Dr Ali Qasim

RENAL FUNCTION TEST (RFT)

Urea (Serum)                                    24 mg/dl
Serum/plasma urea concentration reflects the balance between
urea production in the liver and urea elimination by the kidneys,
in urine.
                                                Adults <65Y: 15 - 50 mg/dl
                                                Adults >65Y: <60 mg/dl

BUN (Blood Urea Nitrogen)                       11.21 mg/dl
BUN reflects only the nitrogen content of urea.
                                                Adults <65Y: 7 - 23.3 mg/dl
                                                Adults >65Y: <28 mg/dl

Creatinine (Serum)                              0.59 mg/dl
The creatinine blood test measures the level of creatinine in the
blood. This test is done to see how well your kidneys are
working.
                                                Female: 0.55 to 1.02 mg/dL

Glomerular Filtration Rate (GFR)                127 mL/Min/1.73m^2
It is a measure of how well your kidneys filter blood, essentially
indicating how efficiently they remove waste and excess fluid
from your body.
                                                Normal: >=90
                                                Mild decrease: 60 - 89
                                                Moderate decrease: 45 - 30
                                                Severe decrease: 15 - 29
"""

# Format 3: Date column format
format3 = """
Patient Name: AHMED KHAN
Age / Sex: 45 Years / Male

Renal Function Test
Tests                   Reference Value Unit            1015-29-04
                                                        29-Apr-2024
Urea                    15 - 50         mg/dl           42
BUN                     7 - 23          mg/dl           19.6
Creatinine              0.7 - 1.3       mg/dl           1.1
GFR                     >=90            mL/min          95
Uric Acid               3.5 - 7.2       mg/dl           5.8
"""

# Format 4: Simple table format
format4 = """
Patient Name: SARA AHMED
Age / Sex: 32 Years / Female

RENAL FUNCTION TEST

Test                            Normal Range        Unit            Result

Urea                            15 - 50             mg/dl           28
BUN (Blood Urea Nitrogen)       7 - 23              mg/dl           13.1
Creatinine                      0.6 - 1.2           mg/dl           0.8
GFR                             >=90                mL/min          105
Uric Acid                       2.5 - 6.0           mg/dl           4.2
"""

print("="*80)
print("Format 1: RESULT column with date")
print("="*80)
r1 = extract_rft(format1)
print(f"Creatinine: {r1['Creatinine']} (expected: 1.3)")
print(f"Urea: {r1['Urea']} (expected: 35)")
print(f"BUN: {r1['BUN']} (expected: 16.3)")

print("\n" + "="*80)
print("Format 2: Detailed with descriptions")
print("="*80)
r2 = extract_rft(format2)
print(f"Name: {r2['Name']} (expected: RABIA)")
print(f"Age: {r2['Age']} (expected: 27)")
print(f"Gender: {r2['Gender']} (expected: Female)")
print(f"Urea: {r2['Urea']} (expected: 24)")
print(f"BUN: {r2['BUN']} (expected: 11.21)")
print(f"Creatinine: {r2['Creatinine']} (expected: 0.59)")
print(f"GFR: {r2['GFR']} (expected: 127)")

print("\n" + "="*80)
print("Format 3: Date column format")
print("="*80)
r3 = extract_rft(format3)
print(f"Name: {r3['Name']} (expected: AHMED KHAN)")
print(f"Age: {r3['Age']} (expected: 45)")
print(f"Gender: {r3['Gender']} (expected: Male)")
print(f"Urea: {r3['Urea']} (expected: 42)")
print(f"BUN: {r3['BUN']} (expected: 19.6)")
print(f"Creatinine: {r3['Creatinine']} (expected: 1.1)")
print(f"GFR: {r3['GFR']} (expected: 95)")
print(f"Uric Acid: {r3['Uric Acid']} (expected: 5.8)")

print("\n" + "="*80)
print("Format 4: Simple table format")
print("="*80)
r4 = extract_rft(format4)
print(f"Name: {r4['Name']} (expected: SARA AHMED)")
print(f"Age: {r4['Age']} (expected: 32)")
print(f"Gender: {r4['Gender']} (expected: Female)")
print(f"Urea: {r4['Urea']} (expected: 28)")
print(f"BUN: {r4['BUN']} (expected: 13.1)")
print(f"Creatinine: {r4['Creatinine']} (expected: 0.8)")
print(f"GFR: {r4['GFR']} (expected: 105)")
print(f"Uric Acid: {r4['Uric Acid']} (expected: 4.2)")

print("\n" + "="*80)
print("RFT Test Complete - All 4 Formats Tested")
print("="*80)

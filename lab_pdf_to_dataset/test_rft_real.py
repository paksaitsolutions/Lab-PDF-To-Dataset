import sys
sys.path.insert(0, '.')

from extractors.rft_extractor import extract_rft

sample_rft = """
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

result = extract_rft(sample_rft)
print("RFT Extraction Test:")
print(f"Name: {result['Name']}")
print(f"Age: {result['Age']}")
print(f"Gender: {result['Gender']}")
print(f"Urea: {result['Urea']}")
print(f"BUN: {result['BUN']}")
print(f"Creatinine: {result['Creatinine']}")
print(f"GFR: {result['GFR']}")
print(f"Uric Acid: {result['Uric Acid']}")

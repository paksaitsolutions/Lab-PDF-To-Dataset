from extractors.cbc_extractor import extract_cbc

# Simulated text from the PDF image you provided
sample_text = """
Lab Number                : 0730
Patient's Name            : Sugra Bibi
Age/Sex                   : 40 Year(s) Female
Contact Number            :
Address                   :

HEMATOLOGY REPORT

COMPLETE BLOOD COUNT (CBC)

TEST(s)                RESULT(s)        UNIT(s)              NORMAL RANGE

HGB                    13.9             g/dl                 Male: 13 - 18
                                                             Female: 12 - 16

WBC Count              9.8              x10.e 3/µl           4 - 11
RBC Count              5.2              x10.e 6/µl           4 - 6
PLATELET COUNT         200              x10.e 3/µl           150 - 400

Red cell indices

HCT                    45.9             %                    36-54
MCV                    88.7             fL                   76-96
MCH                    32.4             pg                   27-33
MCHC                   34.6             g/dL                 33-35

Differentials %

Neutrophils            43               %                    40 - 75
Lymphocytes            44               %                    20 - 45
Monocytes              09               %                    2 - 10
Eosinophils            04               %                    0 - 6
Reticulocyte Count     1.0              %                    0.5 - 2.4

RBCs Morphology:
Normocytic  Normochromic
"""

print("Testing CBC extraction...")
result = extract_cbc(sample_text)
print("\nExtracted data:")
for key, value in result.items():
    print(f"{key}: {value}")

# Check what's missing
missing = [k for k, v in result.items() if not v]
if missing:
    print(f"\nMissing fields: {missing}")
else:
    print("\n✅ All fields extracted successfully!")

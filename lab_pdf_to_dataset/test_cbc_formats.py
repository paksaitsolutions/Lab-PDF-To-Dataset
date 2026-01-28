import sys
sys.path.insert(0, '.')

from extractors.cbc_extractor import extract_cbc

# Format 1: Ramin Malooq - Date column format
format1 = """
Patient Name: Ramin Malooq
Age/Sex: 18 Yr(s) / Male

Blood C/E (Complete, CBC)

Tests                    Reference Value    Unit           1005-13-06
                                                          13-Jun-2024
Hb                       13 - 18            g/dl          13.4
Total RBC                4.5 - 6.5          x10^12/l      5.2
HCT                      38 - 52            %             45
MCV                      75 - 95            fl            87
MCH                      26 - 32            pg            25
MCHC                     30 - 35            g/dl          29
Platelet Count           150 - 400          x10^9/l       174
WBC Count (TLC)          4 - 11             x10^9/l       7.5
Neutrophils              40 - 75            %             65
Lymphocytes              20 - 50            %             30
Monocytes                02 - 10            %             02
Eosinophils              01 - 06            %             03
"""

# Format 2: HAJI MOHAMMAD ARSHAD - RESULT column with date
format2 = """
Patient Name: HAJI MOHAMMAD ARSHAD
Age / Sex: 55 Year(s)/Male

Blood Complete Examination                                RESULT
TEST                    NORMAL RANGE    UNIT              3945
                                                          11-Feb-2025 9:12 am
Hb (Hemoglobin)         14.00 - 18.00   g/dl              12.5
TLC                     4.00 - 11.00    x10^9/l           4.1
ESR                     0.00 - 10.00    mm/1st hr         38
RBC                     4.60 - 6.00     x10^12/l          3.93
HCT                     40.00 - 54.00   %                 33.2
MCV                     80.00 - 94.00   fl                84.5
MCH                     26.00 - 32.00   pg                31.8
MCHC                    32.00 - 36.00   %                 37.7
Platelet Count          150.00 - 450.00 x10^9/l           72
Neutrophils             See Below*      %                 56
Lymphocytes             See Below*      %                 35
Monocytes               2.00 - 11.00    %                 06
Eosinophils             See Below*      %                 03
"""

# Format 3: HEMATOLOGY REPORT - RESULT with date
format3 = """
HEMATOLOGY REPORT.                                        Specimen: EDTA-Whole Blood

TEST                    REFERENCE RANGE UNIT              RESULT
                                                          1225-7/01-Dec-2025
Hemoglobin (HB)         13.0 - 17.0     g/dl              13.9
Total RBCs              4.50 - 5.50     10^6luL           3.90
HCT (Hematocrit)        40.0 - 50.0     %                 37.7
MCV                     80.0 - 100.0    fl                96.5
MCH                     27.0 - 32.0     pg                35.5
MCHC                    31.5 - 34.5     g/dl              36.8
Platelet Count          150.0 - 450.0   10^9/L            337
WBC Count (TLC)         4.0 - 11.0      x10^9/l           4.45
Neutrophils             40.0 - 80.0     %                 60
Lymphocytes             20.0 - 40.0     %                 30
Monocytes               2.0 - 10.0      %                 06
Eosinophils             1.0 - 6.0       %                 04
"""

# Format 4: ZAHID - Result column on right
format4 = """
Patient Name: ZAHID
Age / Sex: 36 Years / Male

HAEMATOLOGY

Test                            Normal Range        Unit            Result

CBC for Male

Hemoglobin (HB)                 13 - 18             g/dl            15.1
Red Blood Cell (RBC)            4.5 - 6.5           *10^12/l        5.6
Hematocrit (HCT)                38 - 52             %               49.2
Mean Cell Volume (MCV)          75 - 95             fl              87.1
Mean Cell Hemoglobin (MCH)      26 - 32             pg              26.8
Mean Cell Hb Conc (MCHC)        30 - 35             g/dl            30.8
Platelets Count                 150 - 400           *10^9/l         351
White Blood Cell (WBC/TLC)      4 - 11              *10^9/l         9.0
Neutrophils                     40 - 75             %               57.1
Lymphocytes                     20 - 50             %               37.3
Monocytes                       2 - 10              %               4.0
Eosinophil                      1 - 6               %               1.6
"""

# Format 5: HAYAT - Table format with arrows
format5 = """
Booking (Ref) #:    572                                 Patient (MR) #:     591
Patient Name:       HAYAT                               Sample Collected:   Outside Lab
Age / Sex:          74 Years / Male                     Test Booked:        20/07/2023 08:51 PM
Mobile:             00000000000                         Results Saved:      21/07/2023 01:29 PM
Consultant:         DR YOUNAS KHAN                      Collection Point:   Main

                                    HAEMATOLOGY

Test                            Normal Range        Unit            Result

CBC for Male

Hemoglobin (HB)                 13 - 18             g/dl            ↓ 12.1
Red Blood Cell (RBC)            4.5 - 6.5           *10*12/l        4.5
Hematocrit (HCT)                38 - 52             %               ↓ 37.3
Mean Cell Volume (MCV)          75 - 95             fl              84.0
Mean Cell Hemoglobin (MCH)      26 - 32             pg              27.1
Mean Cell Hb Conc (MCHC)        30 - 35             g/dl            32.4
Platelets Count                 150 - 400           *10^9/l         201
White Blood Cell (WBC/TLC)      4 - 11              *10^9/l         5.5
Neutrophils                     40 - 75             %               50.1
Lymphocytes                     20 - 50             %               36.4
Monocytes                       2 - 10              %               10.0
Eosinophil                      1 - 6               %               3.5
"""

print("="*80)
print("Format 1: Ramin Malooq (Date column)")
print("="*80)
r1 = extract_cbc(format1)
print(f"Name: {r1['Name']} (expected: Ramin Malooq)")
print(f"Age: {r1['Age']} (expected: 18)")
print(f"Gender: {r1['Gender']} (expected: Male)")
print(f"HB: {r1['HB']} (expected: 13.4)")
print(f"RBC: {r1['RBC']} (expected: 5.2)")
print(f"HCT: {r1['HCT']} (expected: 45)")
print(f"MCV: {r1['MCV']} (expected: 87)")
print(f"MCH: {r1['MCH']} (expected: 25)")
print(f"MCHC: {r1['MCHC']} (expected: 29)")
print(f"Platelets: {r1['Platelets']} (expected: 174)")
print(f"WBC: {r1['WBC']} (expected: 7.5)")
print(f"Neutrophils: {r1['Neutrophils']} (expected: 65)")
print(f"Lymphocytes: {r1['Lymphocytes']} (expected: 30)")
print(f"Monocytes: {r1['Monocytes']} (expected: 02)")
print(f"Eosinophils: {r1['Eosinophils']} (expected: 03)")

print("\n" + "="*80)
print("Format 2: HAJI MOHAMMAD ARSHAD (RESULT column)")
print("="*80)
r2 = extract_cbc(format2)
print(f"Name: {r2['Name']} (expected: HAJI MOHAMMAD ARSHAD)")
print(f"Age: {r2['Age']} (expected: 55)")
print(f"Gender: {r2['Gender']} (expected: Male)")
print(f"HB: {r2['HB']} (expected: 12.5)")
print(f"RBC: {r2['RBC']} (expected: 3.93)")
print(f"HCT: {r2['HCT']} (expected: 33.2)")
print(f"WBC: {r2['WBC']} (expected: 4.1)")
print(f"Neutrophils: {r2['Neutrophils']} (expected: 56)")

print("\n" + "="*80)
print("Format 3: HEMATOLOGY REPORT")
print("="*80)
r3 = extract_cbc(format3)
print(f"HB: {r3['HB']} (expected: 13.9)")
print(f"RBC: {r3['RBC']} (expected: 3.90)")
print(f"HCT: {r3['HCT']} (expected: 37.7)")
print(f"MCV: {r3['MCV']} (expected: 96.5)")
print(f"MCH: {r3['MCH']} (expected: 35.5)")
print(f"MCHC: {r3['MCHC']} (expected: 36.8)")
print(f"Platelets: {r3['Platelets']} (expected: 337)")
print(f"WBC: {r3['WBC']} (expected: 4.45)")

print("\n" + "="*80)
print("Format 4: ZAHID (Result on right)")
print("="*80)
r4 = extract_cbc(format4)
print(f"Name: {r4['Name']} (expected: ZAHID)")
print(f"Age: {r4['Age']} (expected: 36)")
print(f"Gender: {r4['Gender']} (expected: Male)")
print(f"HB: {r4['HB']} (expected: 15.1)")
print(f"RBC: {r4['RBC']} (expected: 5.6)")
print(f"HCT: {r4['HCT']} (expected: 49.2)")
print(f"MCV: {r4['MCV']} (expected: 87.1)")
print(f"MCH: {r4['MCH']} (expected: 26.8)")
print(f"MCHC: {r4['MCHC']} (expected: 30.8)")
print(f"Platelets: {r4['Platelets']} (expected: 351)")
print(f"WBC: {r4['WBC']} (expected: 9.0)")
print(f"Neutrophils: {r4['Neutrophils']} (expected: 57.1)")
print(f"Lymphocytes: {r4['Lymphocytes']} (expected: 37.3)")
print(f"Monocytes: {r4['Monocytes']} (expected: 4.0)")
print(f"Eosinophils: {r4['Eosinophils']} (expected: 1.6)")

print("\n" + "="*80)
print("Format 5: HAYAT (Table with arrows)")
print("="*80)
r5 = extract_cbc(format5)
print(f"Name: {r5['Name']} (expected: HAYAT)")
print(f"Age: {r5['Age']} (expected: 74)")
print(f"Gender: {r5['Gender']} (expected: Male)")
print(f"HB: {r5['HB']} (expected: 12.1)")
print(f"RBC: {r5['RBC']} (expected: 4.5)")
print(f"HCT: {r5['HCT']} (expected: 37.3)")
print(f"MCV: {r5['MCV']} (expected: 84.0)")
print(f"MCH: {r5['MCH']} (expected: 27.1)")
print(f"MCHC: {r5['MCHC']} (expected: 32.4)")
print(f"Platelets: {r5['Platelets']} (expected: 201)")
print(f"WBC: {r5['WBC']} (expected: 5.5)")
print(f"Neutrophils: {r5['Neutrophils']} (expected: 50.1)")
print(f"Lymphocytes: {r5['Lymphocytes']} (expected: 36.4)")
print(f"Monocytes: {r5['Monocytes']} (expected: 10.0)")
print(f"Eosinophils: {r5['Eosinophils']} (expected: 3.5)")

print("\n" + "="*80)
print("CBC Test Complete - All 5 Formats Tested")
print("="*80)

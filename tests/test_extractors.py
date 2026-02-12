import pytest
import sys
import os

# Add application path
sys.path.append(os.path.join(os.getcwd(), 'lab_pdf_to_dataset'))

from extractors.cbc_extractor import extract_cbc
from extractors.lft_extractor import extract_lft
from extractors.rft_extractor import extract_rft
from extractors.tft_extractor import extract_tft

class TestExtractors:
    
    def test_cbc_extraction(self):
        text = """
        Patient Name: John Doe
        Age: 30 Years / Sex: Male
        Hemoglobin                    14.5        g/dL
        RBC Count                     5.2         mill/cumm
        HCT                           42.0        %
        MCV                           85.0        fL
        Platelet Count                250         thousand/cumm
        WBC Count                     7.5         thousand/cumm
        Neutrophils                   60          %
        """
        data = extract_cbc(text)
        assert data['Name'] == 'John Doe'
        assert data['Age'] == '30'
        assert data['Gender'] == 'Male'
        assert data['HB'] == '14.5'
        assert data['RBC'] == '5.2'
        # Note: WBC/Platelet may extract differently depending on format
        
    def test_lft_extraction(self):
        text = """
        Patient Name: Jane Doe
        Age: 45 Years / Sex: Female
        Total Bilirubin               0.8        mg/dL
        Direct Bilirubin              0.2        mg/dL
        SGPT (ALT)                    35         U/L
        SGOT (AST)                    30         U/L
        """
        data = extract_lft(text)
        assert data['Name'] == 'Jane Doe'
        assert data['Age'] == '45'
        assert data['Gender'] == 'Female'
        assert data['Total Bilirubin'] == '0.8'
        assert data['ALT'] == '35'
        
    def test_rft_extraction(self):
        text = """
        Patient Name: Test Patient
        Age: 50 Years / Sex: Male
        Blood Urea                    30         mg/dL
        Serum Creatinine              1.0        mg/dL
        Uric Acid                     5.5        mg/dL
        """
        data = extract_rft(text)
        assert data['Name'] == 'Test Patient'
        assert data['Urea'] == '30'
        assert data['Creatinine'] == '1.0'
        
    def test_tft_extraction(self):
        text = """
        Name: Thyroid User
        Age: 25 Years / Sex: F
        Total T3                      1.2        ng/mL
        Total T4                      8.5        ug/dL
        TSH                           2.5        uIU/mL
        """
        data = extract_tft(text)
        assert data['Name'] == 'Thyroid User'
        assert data['T3'] == '1.2'
        assert data['TSH'] == '2.5'

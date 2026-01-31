import pytest
import os
import sys
import tempfile

# Add the parent directory to the path for all tests
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

@pytest.fixture(scope="session")
def test_data_dir():
    """Create a temporary directory for test data"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir

@pytest.fixture(scope="session")
def sample_lab_text():
    """Sample lab report text for testing"""
    return """
    Patient Name: John Doe
    Age/Sex: 35 years/Male
    Registration: REG12345
    Sample: Blood
    
    Complete Blood Count (CBC):
    HB: 14.5 g/dL
    RBC: 4.8 million/cu.mm
    HCT: 45%
    MCV: 90 fL
    MCH: 30 pg
    MCHC: 32 g/dL
    Platelets: 280,000/cu.mm
    WBC: 7500 cells/cu.mm
    Neutrophils: 55%
    Lymphocytes: 30%
    Monocytes: 8%
    Eosinophils: 5%
    ESR: 10 mm/hr
    
    Liver Function Test (LFT):
    Total Bilirubin: 1.0 mg/dL
    Direct Bilirubin: 0.3 mg/dL
    Indirect Bilirubin: 0.7 mg/dL
    ALT: 25 U/L
    AST: 22 U/L
    ALP: 65 U/L
    Albumin: 4.2 g/dL
    Total Protein: 7.0 g/dL
    
    Renal Function Test (RFT):
    Urea: 25 mg/dL
    BUN: 12 mg/dL
    Creatinine: 0.9 mg/dL
    GFR: 95 mL/min/1.73m²
    Uric Acid: 5.0 mg/dL
    """

@pytest.fixture
def mock_pdf_file(test_data_dir):
    """Create a mock PDF file for testing"""
    pdf_path = os.path.join(test_data_dir, "test_report.pdf")
    with open(pdf_path, 'wb') as f:
        f.write(b"Mock PDF content for testing")
    return pdf_path

@pytest.fixture
def mock_docx_file(test_data_dir):
    """Create a mock DOCX file for testing"""
    docx_path = os.path.join(test_data_dir, "test_report.docx")
    with open(docx_path, 'wb') as f:
        f.write(b"Mock DOCX content for testing")
    return docx_path

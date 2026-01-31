import pytest
import sys
import os

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extractors.cbc_extractor import extract_cbc, extract_basic_info
from extractors.lft_extractor import extract_lft
from extractors.rft_extractor import extract_rft


class TestCBCExtractor:
    """Test cases for CBC data extraction"""
    
    def test_extract_basic_info_success(self):
        """Test successful extraction of basic patient information"""
        sample_text = """
        Patient Name: John Doe
        Age/Sex: 25 years/Male
        Registration: REG123
        """
        
        result = extract_basic_info(sample_text)
        
        assert result["Name"] == "John Doe"
        assert result["Age"] == "25"
        assert result["Gender"] == "Male"
    
    def test_extract_basic_info_missing_data(self):
        """Test extraction with missing patient information"""
        sample_text = "Some random text without patient details"
        
        result = extract_basic_info(sample_text)
        
        assert result["Name"] == ""
        assert result["Age"] == ""
        assert result["Gender"] == ""
    
    def test_extract_cbc_with_sample_data(self):
        """Test CBC extraction with sample lab report data"""
        sample_text = """
        Patient Name: Jane Smith
        Age/Sex: 30 years/Female
        
        Complete Blood Count:
        HB: 12.5 g/dL
        RBC: 4.5 million/cu.mm
        WBC: 7500 cells/cu.mm
        Platelets: 250,000
        """
        
        result = extract_cbc(sample_text)
        
        assert result["Name"] == "Jane Smith"
        assert result["Age"] == "30"
        assert result["Gender"] == "Female"
        assert "HB" in result
        assert "RBC" in result
        assert "WBC" in result
        assert "Platelets" in result


class TestLFTExtractor:
    """Test cases for LFT data extraction"""
    
    def test_extract_lft_with_sample_data(self):
        """Test LFT extraction with sample lab report data"""
        sample_text = """
        Patient Name: Bob Johnson
        Age/Sex: 45 years/Male
        
        Liver Function Test:
        Total Bilirubin: 1.2 mg/dL
        Direct Bilirubin: 0.3 mg/dL
        ALT: 35 U/L
        AST: 28 U/L
        """
        
        result = extract_lft(sample_text)
        
        assert result["Name"] == "Bob Johnson"
        assert result["Age"] == "45"
        assert result["Gender"] == "Male"
        assert "Total Bilirubin" in result
        assert "Direct Bilirubin" in result
        assert "ALT" in result
        assert "AST" in result


class TestRFTExtractor:
    """Test cases for RFT data extraction"""
    
    def test_extract_rft_with_sample_data(self):
        """Test RFT extraction with sample lab report data"""
        sample_text = """
        Patient Name: Alice Brown
        Age/Sex: 35 years/Female
        
        Renal Function Test:
        Urea: 25 mg/dL
        Creatinine: 0.8 mg/dL
        GFR: 90 mL/min/1.73m²
        """
        
        result = extract_rft(sample_text)
        
        assert result["Name"] == "Alice Brown"
        assert result["Age"] == "35"
        assert result["Gender"] == "Female"
        assert "Urea" in result
        assert "Creatinine" in result
        assert "GFR" in result


class TestIntegration:
    """Integration tests for the entire extraction system"""
    
    def test_all_extractors_return_dict(self):
        """Test that all extractors return dictionary with required keys"""
        sample_text = "Patient Name: Test User\nAge/Sex: 25 years/Male"
        
        cbc_result = extract_cbc(sample_text)
        lft_result = extract_lft(sample_text)
        rft_result = extract_rft(sample_text)
        
        # All should return dictionaries
        assert isinstance(cbc_result, dict)
        assert isinstance(lft_result, dict)
        assert isinstance(rft_result, dict)
        
        # All should have basic info keys
        for result in [cbc_result, lft_result, rft_result]:
            assert "Name" in result
            assert "Age" in result
            assert "Gender" in result

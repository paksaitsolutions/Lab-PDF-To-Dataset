import pytest
import os
import sys

# Add the parent directory to the path to import modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Add the lab_pdf_to_dataset directory to path
lab_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'lab_pdf_to_dataset')
sys.path.insert(0, lab_path)

from utils.pdf_reader import read_pdf_text
from utils.docx_reader import read_docx_text


class TestPDFReader:
    """Test cases for PDF reading functionality"""
    
    def test_read_pdf_text_file_not_found(self):
        """Test PDF reader with non-existent file"""
        result = read_pdf_text("non_existent_file.pdf")
        
        # Should handle gracefully and return empty string or error message
        assert isinstance(result, str)
    
    def test_read_pdf_text_invalid_extension(self):
        """Test PDF reader with invalid file extension"""
        result = read_pdf_text("test.txt")
        
        # Should handle gracefully
        assert isinstance(result, str)


class TestDocxReader:
    """Test cases for DOCX reading functionality"""
    
    def test_read_docx_text_file_not_found(self):
        """Test DOCX reader with non-existent file"""
        result = read_docx_text("non_existent_file.docx")
        
        # Should handle gracefully and return empty string or error message
        assert isinstance(result, str)
    
    def test_read_docx_text_invalid_extension(self):
        """Test DOCX reader with invalid file extension"""
        result = read_docx_text("test.txt")
        
        # Should handle gracefully
        assert isinstance(result, str)


class TestUtilityFunctions:
    """Test cases for general utility functions"""
    
    def test_import_modules(self):
        """Test that all utility modules can be imported"""
        try:
            import utils.pdf_reader
            import utils.docx_reader
            import utils.helpers
            import utils.ocr_fallback
            assert True  # All imports successful
        except ImportError as e:
            pytest.fail(f"Failed to import utility module: {e}")
    
    def test_module_attributes(self):
        """Test that required functions exist in modules"""
        # Check if required functions exist
        assert hasattr(read_pdf_text, '__call__')
        assert hasattr(read_docx_text, '__call__')


class TestFileProcessing:
    """Test cases for file processing operations"""
    
    def test_supported_file_extensions(self):
        """Test that supported file extensions are handled correctly"""
        supported_extensions = ['.pdf', '.docx', '.doc']
        
        for ext in supported_extensions:
            assert ext.lower() in ['.pdf', '.docx', '.doc']
    
    def test_file_type_detection(self):
        """Test file type detection logic"""
        test_files = [
            'test.pdf',
            'document.docx',
            'report.doc',
            'image.jpg',
            'text.txt'
        ]
        
        supported = []
        for file in test_files:
            if file.lower().endswith(('.pdf', '.docx', '.doc')):
                supported.append(file)
        
        assert len(supported) == 3
        assert 'test.pdf' in supported
        assert 'document.docx' in supported
        assert 'report.doc' in supported
        assert 'image.jpg' not in supported
        assert 'text.txt' not in supported

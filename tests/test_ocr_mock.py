import pytest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the lab_pdf_to_dataset directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lab_pdf_to_dataset.utils import pdf_reader

class TestOCRFallback:
    def setup_method(self, method):
        """Setup mocks for optional dependencies if they are missing"""
        self.orig_convert = getattr(pdf_reader, 'convert_from_path', None)
        self.orig_pytesseract = getattr(pdf_reader, 'pytesseract', None)
        
        if not hasattr(pdf_reader, 'convert_from_path'):
            pdf_reader.convert_from_path = MagicMock()
        if not hasattr(pdf_reader, 'pytesseract'):
            pdf_reader.pytesseract = MagicMock()

    def teardown_method(self, method):
        """Clean up injected mocks"""
        if self.orig_convert is None:
            delattr(pdf_reader, 'convert_from_path')
        else:
            pdf_reader.convert_from_path = self.orig_convert
            
        if self.orig_pytesseract is None:
            delattr(pdf_reader, 'pytesseract')
        else:
            pdf_reader.pytesseract = self.orig_pytesseract

    def test_ocr_fallback(self):
        """Test that OCR is triggered when standard extraction yields little text"""
        
        with patch('lab_pdf_to_dataset.utils.pdf_reader.pdfplumber') as mock_pdfplumber:
            # Mock standard extraction to return empty text
            mock_pdf = MagicMock()
            mock_page = MagicMock()
            mock_page.extract_text.return_value = "" # No text
            mock_pdf.pages = [mock_page]
            mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf
            
            # Setup OCR mocks
            mock_convert = pdf_reader.convert_from_path
            mock_pytesseract = pdf_reader.pytesseract
            
            mock_convert.return_value = ["mock_image"]
            mock_pytesseract.image_to_string.return_value = "OCR Extracted Text"
            
            # Force OCR_AVAILABLE to be True for this test
            with patch.object(pdf_reader, 'OCR_AVAILABLE', True):
                text = pdf_reader.read_pdf_text("dummy.pdf")
                
                # Assertions
                mock_convert.assert_called()
                mock_pytesseract.image_to_string.assert_called()
                assert "OCR Extracted Text" in text

    def test_standard_extraction_sufficient(self):
        """Test that OCR is NOT triggered when standard extraction is sufficient"""
        
        with patch('lab_pdf_to_dataset.utils.pdf_reader.pdfplumber') as mock_pdfplumber:
            # Mock standard extraction to return sufficient text (>50 chars)
            mock_pdf = MagicMock()
            mock_page = MagicMock()
            mock_page.extract_text.return_value = "A" * 60 # 60 chars
            mock_pdf.pages = [mock_page]
            mock_pdfplumber.open.return_value.__enter__.return_value = mock_pdf
            
            # Setup OCR mocks
            mock_convert = pdf_reader.convert_from_path
            
            # Force OCR_AVAILABLE to be True
            with patch.object(pdf_reader, 'OCR_AVAILABLE', True):
                text = pdf_reader.read_pdf_text("dummy.pdf")
                
                # Assertions
                # convert_from_path should NOT be called
                # We can't use assert_not_called() easily if it wasn't a mock from start, 
                # but we injected a MagicMock in setup_method, so we can.
                mock_convert.assert_not_called()
                assert len(text.strip()) >= 50

import pytest
import pandas as pd
import sys
import os
import shutil

# Add the application directory to sys.path to allow imports from app.py to work correctly
sys.path.append(os.path.join(os.getcwd(), 'lab_pdf_to_dataset'))

from lab_pdf_to_dataset.app import app, OUTPUT_DIR, UPLOAD_DIR


class TestExcelExport:
    def setup_method(self):
        # Create dummy upload and output directories
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        self.client = app.test_client()

    def teardown_method(self):
        # Cleanup
        if os.path.exists(UPLOAD_DIR):
            shutil.rmtree(UPLOAD_DIR)
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

    def test_excel_file_creation(self):
        # Simulate data processing by manually creating a DataFrame and saving it as Excel to OUTPUT_DIR
        # This tests if the environment supports openpyxl and file writing
        
        data = {
            "Name": ["Test User"],
            "Age": [30],
            "Gender": ["Male"],
            "HB": [14.5]
        }
        df = pd.DataFrame(data)
        excel_path = os.path.join(OUTPUT_DIR, "Test_Dataset.xlsx")
        
        try:
            df.to_excel(excel_path, index=False)
        except Exception as e:
            pytest.fail(f"Excel export failed: {e}")
            
        assert os.path.exists(excel_path)
        
        # Verify content
        read_df = pd.read_excel(excel_path)
        assert read_df.iloc[0]["Name"] == "Test User"
        assert read_df.iloc[0]["HB"] == 14.5

    def test_app_config_excel(self):
        # Verify app config has excel output keys
        from lab_pdf_to_dataset.app import TEST_CONFIG
        assert "cbc" in TEST_CONFIG
        assert "excel_output_file" in TEST_CONFIG["cbc"]
        assert TEST_CONFIG["cbc"]["excel_output_file"].endswith(".xlsx")

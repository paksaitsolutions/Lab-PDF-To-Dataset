"""
Debug script to see the actual text extracted from RFT/LFT PDFs
Place your RFT or LFT PDF in the same directory and update the filename below
"""
import sys
sys.path.insert(0, '.')

from utils.pdf_reader import read_pdf_text
from extractors.rft_extractor import extract_rft
from extractors.lft_extractor import extract_lft
import os

# Look for any PDF in current directory
pdf_files = [f for f in os.listdir('.') if f.lower().endswith('.pdf')]

if not pdf_files:
    print("No PDF files found in current directory")
    print("Please place an RFT or LFT PDF file here and run again")
else:
    for pdf_file in pdf_files[:3]:  # Check first 3 PDFs
        print(f"\n{'='*70}")
        print(f"Analyzing: {pdf_file}")
        print('='*70)
        
        text = read_pdf_text(pdf_file)
        print("\n--- EXTRACTED TEXT (first 1500 chars) ---")
        print(text[:1500])
        print("\n--- END OF TEXT SAMPLE ---\n")
        
        # Try to detect test type
        text_lower = text.lower()
        if 'renal' in text_lower or 'kidney' in text_lower or 'creatinine' in text_lower:
            print("Detected as RFT")
            result = extract_rft(text)
            print(f"\nExtracted RFT data:")
            for key, value in result.items():
                print(f"  {key}: {value}")
        elif 'liver' in text_lower or 'bilirubin' in text_lower:
            print("Detected as LFT")
            result = extract_lft(text)
            print(f"\nExtracted LFT data:")
            for key, value in result.items():
                print(f"  {key}: {value}")
        else:
            print("Could not detect test type")

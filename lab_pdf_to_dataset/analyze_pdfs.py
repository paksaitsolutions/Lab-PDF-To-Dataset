"""
Analyze RFT and LFT PDFs to see their actual format
"""
import os
import sys
sys.path.insert(0, '.')

from utils.pdf_reader import read_pdf_text
from extractors.rft_extractor import extract_rft
from extractors.lft_extractor import extract_lft

# Find sample RFT/LFT PDFs from your earlier upload
# Check common locations
search_paths = [
    'uploads',
    'input',
    'input/extracted',
    '.'
]

rft_pdfs = []
lft_pdfs = []

for search_path in search_paths:
    if not os.path.exists(search_path):
        continue
    
    for root, dirs, files in os.walk(search_path):
        for f in files:
            if not f.lower().endswith('.pdf'):
                continue
            
            file_path = os.path.join(root, f)
            text = read_pdf_text(file_path)
            text_lower = text.lower()
            
            if 'renal' in text_lower or 'kidney' in text_lower or 'creatinine' in text_lower:
                rft_pdfs.append((f, file_path, text))
            elif 'liver' in text_lower or 'bilirubin' in text_lower:
                lft_pdfs.append((f, file_path, text))

# Analyze first RFT PDF
if rft_pdfs:
    print("="*70)
    print("RFT PDF ANALYSIS")
    print("="*70)
    filename, filepath, text = rft_pdfs[0]
    print(f"\nFile: {filename}")
    print(f"\n--- EXTRACTED TEXT (first 2000 chars) ---")
    print(text[:2000])
    print("\n--- EXTRACTION ATTEMPT ---")
    result = extract_rft(text)
    print(f"Name: {result['Name']}")
    print(f"Age: {result['Age']}")
    print(f"Gender: {result['Gender']}")
    print(f"Urea: {result['Urea']}")
    print(f"BUN: {result['BUN']}")
    print(f"Creatinine: {result['Creatinine']}")
    print(f"GFR: {result['GFR']}")
    print(f"Uric Acid: {result['Uric Acid']}")
else:
    print("No RFT PDFs found")

# Analyze first LFT PDF
if lft_pdfs:
    print("\n" + "="*70)
    print("LFT PDF ANALYSIS")
    print("="*70)
    filename, filepath, text = lft_pdfs[0]
    print(f"\nFile: {filename}")
    print(f"\n--- EXTRACTED TEXT (first 2000 chars) ---")
    print(text[:2000])
    print("\n--- EXTRACTION ATTEMPT ---")
    result = extract_lft(text)
    print(f"Name: {result['Name']}")
    print(f"Age: {result['Age']}")
    print(f"Gender: {result['Gender']}")
    for key in ['Total Bilirubin', 'Direct Bilirubin', 'Indirect Bilirubin', 'ALT', 'AST', 'ALP', 'Albumin', 'Total Protein']:
        print(f"{key}: {result[key]}")
else:
    print("\nNo LFT PDFs found")

if not rft_pdfs and not lft_pdfs:
    print("\nNo RFT or LFT PDFs found in any location.")
    print("Please upload your files again or place them in the 'uploads' folder.")

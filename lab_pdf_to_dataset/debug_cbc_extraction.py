"""
Debug script to test CBC extraction with actual PDF files
Usage: python debug_cbc_extraction.py <path_to_pdf_file>
"""
import sys
import os
from utils.pdf_reader import read_pdf_text
from extractors.cbc_extractor import extract_cbc
import re

def debug_cbc_extraction(pdf_path):
    print(f"\n{'='*80}")
    print(f"Analyzing: {os.path.basename(pdf_path)}")
    print(f"{'='*80}\n")
    
    # Extract text
    text = read_pdf_text(pdf_path)
    
    # Show first 2000 characters of extracted text
    print("EXTRACTED TEXT (first 2000 chars):")
    print("-" * 80)
    print(text[:2000])
    print("-" * 80)
    
    # Test each pattern individually
    patterns = {
        'HB': r'(?:HGB|Hemoglobin|HB).*?g/dl[\s\n]+([0-9]+\.?[0-9]*)',
        'WBC': r'(?:White Blood Cell|WBC|TLC).*?[x\*]10\^?\d+[/\s]*[lL][\s\n]+([0-9]+\.?[0-9]*)',
        'RBC': r'(?:Total\s+)?(?:Red Blood Cell|RBC|RBCs).*?(?:[x\*]10\^?\d+[/\s]*[lL]|10\^6[lL]uL)[\s\n]+([0-9]+\.?[0-9]*)',
        'Platelets': r'Platelets?\s*Count.*?(?:[x\*]10\^?\d+[/\s]*[lL]|10\^9/L)[\s\n]+([0-9]+)',
        'HCT': r'(?:HCT|PCV|Hematocrit).*?%[\s\n]+([0-9]+\.?[0-9]*)',
        'MCV': r'(?:Mean Cell Volume|MCV).*?fl[\s\n]+([0-9]+\.?[0-9]*)',
        'MCH': r'(?:Mean Cell Hemoglobin|MCH)(?!C).*?pg[\s\n]+([0-9]+\.?[0-9]*)',
        'MCHC': r'(?:Mean Cell.*?Conc|MCHC).*?(?:g/dl|%)[\s\n]+([0-9]+\.?[0-9]*)',
        'Neutrophils': r'Neutrophils?[^\n]*?%[\s\n]+([0-9]+\.?[0-9]*)',
        'Lymphocytes': r'Lymphocytes?[^\n]*?%[\s\n]+([0-9]+\.?[0-9]*)',
        'Monocytes': r'Monocytes?[^\n]*?%[\s\n]+([0-9]+\.?[0-9]*)',
        'Eosinophils': r'Eosinophils?[^\n]*?%[\s\n]+([0-9]+\.?[0-9]*)',
        'ESR': r'ESR[^\n]*?([0-9]+\.?[0-9]*)'
    }
    
    print("\nPATTERN MATCHING RESULTS:")
    print("-" * 80)
    for test, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            # Show context around the match
            start = max(0, match.start() - 50)
            end = min(len(text), match.end() + 50)
            context = text[start:end].replace('\n', '\\n')
            print(f"✅ {test:15} = {match.group(1):10} | Context: ...{context}...")
        else:
            print(f"❌ {test:15} = NOT FOUND")
    
    print("\n" + "-" * 80)
    print("\nFULL EXTRACTION RESULT:")
    print("-" * 80)
    result = extract_cbc(text)
    for key, value in result.items():
        status = "✅" if value else "❌"
        print(f"{status} {key:15} = {value}")
    
    # Search for MCV specifically in the text
    print("\n" + "=" * 80)
    print("SEARCHING FOR MCV IN TEXT:")
    print("=" * 80)
    mcv_lines = [line for line in text.split('\n') if 'mcv' in line.lower()]
    if mcv_lines:
        for i, line in enumerate(mcv_lines[:5], 1):
            print(f"{i}. {line}")
    else:
        print("No lines containing 'MCV' found")
    
    return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python debug_cbc_extraction.py <path_to_pdf_file>")
        print("\nOr test with all PDFs in a directory:")
        print("python debug_cbc_extraction.py <path_to_directory>")
        sys.exit(1)
    
    path = sys.argv[1]
    
    if os.path.isfile(path):
        debug_cbc_extraction(path)
    elif os.path.isdir(path):
        pdf_files = [f for f in os.listdir(path) if f.lower().endswith('.pdf')]
        print(f"Found {len(pdf_files)} PDF files")
        for pdf_file in pdf_files[:3]:  # Test first 3 files
            debug_cbc_extraction(os.path.join(path, pdf_file))
    else:
        print(f"Error: {path} is not a valid file or directory")

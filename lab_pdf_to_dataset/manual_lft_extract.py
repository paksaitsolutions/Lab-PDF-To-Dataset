import os
import sys
sys.path.insert(0, '.')

from utils.pdf_reader import read_pdf_text
from extractors.lft_extractor import extract_lft
import pandas as pd

# Find LFT PDFs in uploads folder
lft_files = []
for root, dirs, files in os.walk('uploads'):
    for f in files:
        if f.lower().endswith('.pdf'):
            file_path = os.path.join(root, f)
            text = read_pdf_text(file_path)
            if 'liver function' in text.lower() or 'lft' in text.lower() or 'bilirubin' in text.lower():
                lft_files.append((f, file_path, text))

print(f"Found {len(lft_files)} LFT files")

# Extract data
lft_rows = []
for filename, filepath, text in lft_files:
    print(f"\n=== Processing: {filename} ===")
    result = extract_lft(text)
    print(f"Name: {result['Name']}")
    print(f"Age: {result['Age']}")
    print(f"Gender: {result['Gender']}")
    print(f"Total Bilirubin: {result['Total Bilirubin']}")
    print(f"ALT: {result['ALT']}")
    print(f"AST: {result['AST']}")
    print(f"ALP: {result['ALP']}")
    
    # Check if any test values extracted
    if any(result[k] for k in ['Total Bilirubin', 'ALT', 'AST', 'ALP', 'Albumin', 'Total Protein']):
        result['Source_PDF'] = filename
        lft_rows.append(result)
        print("✅ Added to dataset")
    else:
        print("❌ No values extracted")

# Save to CSV
if lft_rows:
    df = pd.DataFrame(lft_rows)
    df.to_csv('output/LFT_Dataset_manual.csv', index=False)
    print(f"\n✅ Saved {len(lft_rows)} rows to LFT_Dataset_manual.csv")
else:
    print("\n❌ No LFT data extracted")

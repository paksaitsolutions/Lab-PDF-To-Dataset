import os, zipfile
import pandas as pd
from utils.pdf_reader import read_pdf_text
from utils.docx_reader import read_docx_text, extract_docx_table_data
from extractors.cbc_extractor import extract_cbc

# Extract zip
zip_path = "uploads/cbc.zip"
extract_dir = "uploads/extracted"
os.makedirs(extract_dir, exist_ok=True)

with zipfile.ZipFile(zip_path, 'r') as z:
    z.extractall(extract_dir)

cbc_rows = []
total = 0
processed = 0

for root, dirs, files in os.walk(extract_dir):
    for f in files:
        ext = f.lower()
        if not (ext.endswith('.pdf') or ext.endswith('.docx') or ext.endswith('.doc')):
            continue
        
        total += 1
        file_path = os.path.join(root, f)
        print(f"\nProcessing: {f}")
        print(f"Path: {file_path}")
        
        try:
            if ext.endswith('.pdf'):
                text = read_pdf_text(file_path)
                row = extract_cbc(text)
            else:
                row = extract_docx_table_data(file_path)
                if not row or len(row) == 0:
                    print("Table extraction failed, trying text...")
                    text = read_docx_text(file_path)
                    row = extract_cbc(text)
            
            row['Source_PDF'] = f
            cbc_rows.append(row)
            processed += 1
            print(f"Extracted: {row}")
        except Exception as e:
            print(f"Error: {e}")

print(f"\n\nTotal: {total}, Processed: {processed}")
print(f"CBC rows: {len(cbc_rows)}")

if cbc_rows:
    df = pd.DataFrame(cbc_rows)
    df.to_csv('output/CBC_Dataset.csv', index=False)
    print("\nDataset saved to output/CBC_Dataset.csv")
    print(df.head())

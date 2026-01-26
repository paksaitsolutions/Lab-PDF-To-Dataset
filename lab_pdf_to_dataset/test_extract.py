import sys
import os
os.chdir('d:/Lab-PDF-To-Dataset/lab_pdf_to_dataset')

from utils.pdf_reader import read_pdf_text
from extractors.cbc_extractor import extract_cbc

pdf_path = 'uploads/extracted/dataset/cbd guj/1000-All.pdf'
text = read_pdf_text(pdf_path)
print("Extracted text length:", len(text))
print("\nExtracted CBC data:")
data = extract_cbc(text)
for k, v in data.items():
    print(f"{k}: {v}")

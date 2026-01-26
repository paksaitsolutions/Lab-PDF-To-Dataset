from utils.pdf_reader import read_pdf_text
from extractors.cbc_extractor import extract_cbc
import sys
import io

# Fix Unicode output for Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pdf_path = r"D:\Lab-PDF-To-Dataset\lab_pdf_to_dataset\uploads\extracted\dataset\cbd guj\730-All.pdf"

print("Reading PDF...")
text = read_pdf_text(pdf_path)
print(f"\n=== Extracted Text (first 1000 chars) ===")
print(text[:1000])
print(f"\n=== Full text length: {len(text)} chars ===")

print("\n\n=== Extracting CBC data ===")
result = extract_cbc(text)
print("\nExtracted data:")
for key, value in result.items():
    print(f"{key}: '{value}'")

missing = [k for k, v in result.items() if not v]
if missing:
    print(f"\n⚠️ Missing fields: {missing}")
else:
    print("\n✅ All fields extracted!")

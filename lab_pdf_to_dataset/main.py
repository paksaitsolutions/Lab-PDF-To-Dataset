# Main Entry Point
import zipfile, os, sys
import pandas as pd
from utils.pdf_reader import read_pdf_text
from extractors.cbc_extractor import extract_cbc
from extractors.lft_extractor import extract_lft
from extractors.rft_extractor import extract_rft

if len(sys.argv) < 2:
    print("Usage: python main.py <path_to_zip_or_pdf>")
    sys.exit(1)

input_path = sys.argv[1]
EXTRACT_DIR = "input/extracted"
OUTPUT_DIR = "output"

os.makedirs(EXTRACT_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

if input_path.lower().endswith(".zip"):
    with zipfile.ZipFile(input_path, "r") as z:
        z.extractall(EXTRACT_DIR)
    scan_dir = EXTRACT_DIR
elif input_path.lower().endswith(".pdf"):
    scan_dir = os.path.dirname(input_path) or "."
else:
    scan_dir = input_path

cbc_rows, lft_rows, rft_rows = [], [], []

for root, dirs, files in os.walk(scan_dir):
    for f in files:
        if not f.lower().endswith(".pdf"):
            continue

        pdf_path = os.path.join(root, f)
        text = read_pdf_text(pdf_path)
        folder = root.lower()

        if "cbc" in folder or "cbd" in folder:
            row = extract_cbc(text)
            row["Source_PDF"] = f
            cbc_rows.append(row)

        elif "lft" in folder:
            row = extract_lft(text)
            row["Source_PDF"] = f
            lft_rows.append(row)

        elif "rft" in folder:
            row = extract_rft(text)
            row["Source_PDF"] = f
            rft_rows.append(row)

pd.DataFrame(cbc_rows).to_excel(f"{OUTPUT_DIR}/CBC_Dataset_FULL.xlsx", index=False)
pd.DataFrame(lft_rows).to_excel(f"{OUTPUT_DIR}/LFT_Dataset_FULL.xlsx", index=False)
pd.DataFrame(rft_rows).to_excel(f"{OUTPUT_DIR}/RFT_Dataset_FULL.xlsx", index=False)

print("✅ All datasets generated successfully")

import os
import sys
sys.path.insert(0, '.')

from utils.pdf_reader import read_pdf_text

# Find first LFT PDF in uploads/extracted
for root, dirs, files in os.walk('uploads/extracted'):
    for f in files:
        if f.lower().endswith('.pdf'):
            file_path = os.path.join(root, f)
            text = read_pdf_text(file_path)
            
            if 'liver' in text.lower() or 'lft' in text.lower() or 'bilirubin' in text.lower():
                print(f"Found LFT PDF: {f}")
                print("\n" + "="*70)
                print("RAW TEXT FROM PDF:")
                print("="*70)
                print(text[:3000])  # First 3000 chars
                
                # Save to file
                with open('lft_sample_text.txt', 'w', encoding='utf-8') as out:
                    out.write(text)
                print("\n\nFull text saved to: lft_sample_text.txt")
                break
    else:
        continue
    break

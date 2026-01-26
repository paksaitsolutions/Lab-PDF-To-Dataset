from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import zipfile, os, shutil, traceback
import pandas as pd
from utils.pdf_reader import read_pdf_text
from utils.docx_reader import read_docx_text, extract_docx_table_data
from extractors.cbc_extractor import extract_cbc
from extractors.lft_extractor import extract_lft
from extractors.rft_extractor import extract_rft

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file'}), 400
        
        file = request.files['file']
        filepath = os.path.join(UPLOAD_DIR, file.filename)
        file.save(filepath)
        
        if filepath.lower().endswith('.zip'):
            extract_dir = os.path.join(UPLOAD_DIR, 'extracted')
            os.makedirs(extract_dir, exist_ok=True)
            with zipfile.ZipFile(filepath, 'r') as z:
                z.extractall(extract_dir)
            scan_dir = extract_dir
        else:
            scan_dir = UPLOAD_DIR
        
        cbc_rows, lft_rows, rft_rows = [], [], []
        total_files = 0
        processed_files = 0
        
        for root, dirs, files in os.walk(scan_dir):
            for f in files:
                ext = f.lower()
                if not (ext.endswith('.pdf') or ext.endswith('.docx') or ext.endswith('.doc')):
                    continue
                
                total_files += 1
                file_path = os.path.join(root, f)
                folder = root.lower()
                
                # Determine test type from folder or filename
                test_type = None
                folder_lower = folder.lower()
                filename_lower = f.lower()
                
                if 'cbc' in folder_lower or 'cbd' in folder_lower or 'cbc' in filename_lower:
                    test_type = 'cbc'
                elif 'lft' in folder_lower or 'lft' in filename_lower:
                    test_type = 'lft'
                elif 'rft' in folder_lower or 'rft' in filename_lower:
                    test_type = 'rft'
                
                # Extract data
                row = None
                try:
                    if ext.endswith('.pdf'):
                        text = read_pdf_text(file_path)
                        print(f"\n=== PDF: {f} ===")
                        
                        # Auto-detect test type from content if not specified
                        if not test_type:
                            if any(keyword in text.lower() for keyword in ['hemoglobin', 'hematology', 'complete blood count', 'wbc', 'rbc']):
                                test_type = 'cbc'
                            elif any(keyword in text.lower() for keyword in ['liver function', 'bilirubin', 'sgpt', 'sgot', 'alt', 'ast']):
                                test_type = 'lft'
                            elif any(keyword in text.lower() for keyword in ['renal function', 'kidney', 'creatinine', 'urea', 'bun']):
                                test_type = 'rft'
                            else:
                                print(f"⚠️ Skipping {f} - Unknown test type")
                                continue
                        
                        print(f"Detected test type: {test_type}")
                        if test_type == 'cbc':
                            row = extract_cbc(text)
                        elif test_type == 'lft':
                            row = extract_lft(text)
                        elif test_type == 'rft':
                            row = extract_rft(text)
                        print(f"Extracted row: {row}")
                    else:
                        # Word file - try table extraction first
                        print(f"Processing Word file: {f}")
                        row = extract_docx_table_data(file_path)
                        print(f"Table extraction result: {row}")
                        
                        if not row or len(row) < 3 or not any(row.values()):
                            # Fallback to text extraction
                            print(f"Falling back to text extraction for {f}")
                            text = read_docx_text(file_path)
                            print(f"Text length: {len(text)}")
                            if test_type == 'cbc':
                                row = extract_cbc(text)
                            elif test_type == 'lft':
                                row = extract_lft(text)
                            elif test_type == 'rft':
                                row = extract_rft(text)
                            print(f"Text extraction result: {row}")
                    
                    if row and any(v for k, v in row.items() if k not in ['Name', 'Age', 'Gender', 'Source_PDF']):
                        row['Source_PDF'] = f
                        if test_type == 'cbc':
                            cbc_rows.append(row)
                        elif test_type == 'lft':
                            lft_rows.append(row)
                        elif test_type == 'rft':
                            rft_rows.append(row)
                        processed_files += 1
                        print(f"✅ Successfully extracted data from {f}")
                    else:
                        print(f"⚠️ No test values extracted from {f}")
                except Exception as e:
                    print(f"Error processing {f}: {e}")
                    continue
        
        # Generate unique filenames if files already exist
        def get_unique_filename(base_path):
            if not os.path.exists(base_path):
                return base_path
            
            dir_name = os.path.dirname(base_path)
            base_name = os.path.basename(base_path)
            name, ext = os.path.splitext(base_name)
            
            counter = 1
            while True:
                new_path = os.path.join(dir_name, f"{name}_{counter}{ext}")
                if not os.path.exists(new_path):
                    return new_path
                counter += 1
        
        cbc_file = get_unique_filename(f'{OUTPUT_DIR}/CBC_Dataset.csv')
        lft_file = get_unique_filename(f'{OUTPUT_DIR}/LFT_Dataset.csv')
        rft_file = get_unique_filename(f'{OUTPUT_DIR}/RFT_Dataset.csv')
        
        pd.DataFrame(cbc_rows).to_csv(cbc_file, index=False)
        pd.DataFrame(lft_rows).to_csv(lft_file, index=False)
        pd.DataFrame(rft_rows).to_csv(rft_file, index=False)
        
        shutil.rmtree(UPLOAD_DIR)
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        
        return jsonify({
            'success': True, 
            'total_files': total_files,
            'processed_files': processed_files,
            'cbc_count': len(cbc_rows),
            'lft_count': len(lft_rows),
            'rft_count': len(rft_rows),
            'cbc_file': os.path.basename(cbc_file),
            'lft_file': os.path.basename(lft_file),
            'rft_file': os.path.basename(rft_file)
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

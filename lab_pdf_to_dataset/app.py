from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import zipfile, os, shutil, traceback, json
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
        
        # Get selected test types
        test_types_json = request.form.get('test_types', '{"cbc": true, "lft": true, "rft": true}')
        selected_types = json.loads(test_types_json)
        print(f"\n=== SELECTED TEST TYPES: {selected_types} ===")
        
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
                        
                        # Detect ALL test types in the file
                        detected_types = []
                        if not test_type:
                            if any(keyword in text.lower() for keyword in ['hemoglobin', 'hematology', 'complete blood count', 'wbc', 'rbc']):
                                detected_types.append('cbc')
                            if any(keyword in text.lower() for keyword in ['liver function', 'bilirubin', 'sgpt', 'sgot', 'alt', 'ast']):
                                detected_types.append('lft')
                            if any(keyword in text.lower() for keyword in ['renal function', 'kidney', 'creatinine', 'urea', 'bun']):
                                detected_types.append('rft')
                            
                            if not detected_types:
                                print(f"⚠️ Skipping {f} - Unknown test type")
                                continue
                        else:
                            detected_types = [test_type]
                        
                        print(f"Detected test types: {detected_types}")
                        
                        # Extract data for each detected type
                        for test_type in detected_types:
                            # Skip if test type not selected
                            if not selected_types.get(test_type, False):
                                print(f"⏭️ Skipping {test_type.upper()} extraction - not selected")
                                continue
                            
                            if test_type == 'cbc':
                                row = extract_cbc(text)
                                if any(v for k, v in row.items() if k not in ['Name', 'Age', 'Gender', 'Source_PDF']):
                                    row['Source_PDF'] = f
                                    cbc_rows.append(row)
                                    print(f"✅ CBC data extracted")
                            elif test_type == 'lft':
                                row = extract_lft(text)
                                if any(v for k, v in row.items() if k not in ['Name', 'Age', 'Gender', 'Source_PDF']):
                                    row['Source_PDF'] = f
                                    lft_rows.append(row)
                                    print(f"✅ LFT data extracted")
                            elif test_type == 'rft':
                                row = extract_rft(text)
                                if any(v for k, v in row.items() if k not in ['Name', 'Age', 'Gender', 'Source_PDF']):
                                    row['Source_PDF'] = f
                                    rft_rows.append(row)
                                    print(f"✅ RFT data extracted")
                        
                        if cbc_rows or lft_rows or rft_rows:
                            processed_files += 1
                    else:
                        # Word file processing
                        print(f"Processing Word file: {f}")
                        text = read_docx_text(file_path)
                        
                        # Detect test types
                        detected_types = []
                        if not test_type:
                            if any(keyword in text.lower() for keyword in ['hemoglobin', 'hematology', 'complete blood count', 'wbc', 'rbc']):
                                detected_types.append('cbc')
                            if any(keyword in text.lower() for keyword in ['liver function', 'bilirubin', 'sgpt', 'sgot', 'alt', 'ast']):
                                detected_types.append('lft')
                            if any(keyword in text.lower() for keyword in ['renal function', 'kidney', 'creatinine', 'urea', 'bun']):
                                detected_types.append('rft')
                            
                            if not detected_types:
                                continue
                        else:
                            detected_types = [test_type]
                        
                        # Extract data
                        for test_type in detected_types:
                            if not selected_types.get(test_type, False):
                                continue
                            
                            if test_type == 'cbc':
                                row = extract_cbc(text)
                                if any(v for k, v in row.items() if k not in ['Name', 'Age', 'Gender', 'Source_PDF']):
                                    row['Source_PDF'] = f
                                    cbc_rows.append(row)
                            elif test_type == 'lft':
                                row = extract_lft(text)
                                if any(v for k, v in row.items() if k not in ['Name', 'Age', 'Gender', 'Source_PDF']):
                                    row['Source_PDF'] = f
                                    lft_rows.append(row)
                            elif test_type == 'rft':
                                row = extract_rft(text)
                                if any(v for k, v in row.items() if k not in ['Name', 'Age', 'Gender', 'Source_PDF']):
                                    row['Source_PDF'] = f
                                    rft_rows.append(row)
                        
                        if cbc_rows or lft_rows or rft_rows:
                            processed_files += 1
                        
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
        
        cbc_file = get_unique_filename(f'{OUTPUT_DIR}/CBC_Dataset.csv') if selected_types.get('cbc') else None
        lft_file = get_unique_filename(f'{OUTPUT_DIR}/LFT_Dataset.csv') if selected_types.get('lft') else None
        rft_file = get_unique_filename(f'{OUTPUT_DIR}/RFT_Dataset.csv') if selected_types.get('rft') else None
        
        if cbc_file:
            pd.DataFrame(cbc_rows).to_csv(cbc_file, index=False)
        if lft_file:
            pd.DataFrame(lft_rows).to_csv(lft_file, index=False)
        if rft_file:
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
            'cbc_file': os.path.basename(cbc_file) if cbc_file else 'N/A',
            'lft_file': os.path.basename(lft_file) if lft_file else 'N/A',
            'rft_file': os.path.basename(rft_file) if rft_file else 'N/A'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)

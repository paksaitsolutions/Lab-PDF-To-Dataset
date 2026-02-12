from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import zipfile
import os
import shutil
import traceback
import json
import uuid
import pandas as pd

from utils.pdf_reader import read_pdf_text
from utils.docx_reader import read_docx_text
from extractors.cbc_extractor import extract_cbc
from extractors.lft_extractor import extract_lft
from extractors.rft_extractor import extract_rft
from extractors.tft_extractor import extract_tft

app = Flask(__name__)
CORS(app)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "output"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

DEFAULT_TEST_TYPES = {"cbc": True, "lft": True, "rft": True, "tft": True}

TEST_CONFIG = {
    "cbc": {
        "detector_keywords": ["hemoglobin", "hematology", "complete blood count", "wbc", "rbc"],
        "extractor": extract_cbc,
        "output_file": "CBC_Dataset.csv",
        "excel_output_file": "CBC_Dataset.xlsx",
        "required_fields": ["Name", "Age", "Gender", "Source_PDF"],
    },
    "lft": {
        "detector_keywords": ["liver function", "bilirubin", "sgpt", "sgot", "alt", "ast"],
        "extractor": extract_lft,
        "output_file": "LFT_Dataset.csv",
        "excel_output_file": "LFT_Dataset.xlsx",
        "required_fields": ["Name", "Age", "Gender", "Source_PDF"],
    },
    "rft": {
        "detector_keywords": ["renal function", "kidney", "creatinine", "urea", "bun"],
        "extractor": extract_rft,
        "output_file": "RFT_Dataset.csv",
        "excel_output_file": "RFT_Dataset.xlsx",
        "required_fields": ["Name", "Age", "Gender", "Source_PDF"],
    },
    "tft": {
        "detector_keywords": ["thyroid", "tsh", "t3", "t4", "ft3", "ft4"],
        "extractor": extract_tft,
        "output_file": "TFT_Dataset.csv",
        "excel_output_file": "TFT_Dataset.xlsx",
        "required_fields": ["Name", "Age", "Gender", "Source_PDF"],
    },
}


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


def is_supported_file(filename):
    lower = filename.lower()
    return lower.endswith('.pdf') or lower.endswith('.docx') or lower.endswith('.doc')


def infer_type_from_path(filepath):
    lower = filepath.lower()
    for test_type in TEST_CONFIG:
        if test_type in lower:
            return test_type
    return None


def detect_types_from_text(text):
    detected = []
    normalized = text.lower()
    for test_type, config in TEST_CONFIG.items():
        if any(keyword in normalized for keyword in config['detector_keywords']):
            detected.append(test_type)
    return detected


def get_candidate_paths(upload_path):
    candidate_paths = []
    skipped = []

    if upload_path.lower().endswith('.zip'):
        extract_dir = os.path.join(UPLOAD_DIR, f"extracted_{uuid.uuid4().hex}")
        os.makedirs(extract_dir, exist_ok=True)
        with zipfile.ZipFile(upload_path, 'r') as z:
            z.extractall(extract_dir)

        for root, _, extracted_files in os.walk(extract_dir):
            for extracted in extracted_files:
                extracted_path = os.path.join(root, extracted)
                if is_supported_file(extracted_path):
                    candidate_paths.append(extracted_path)
                else:
                    skipped.append({"file": extracted, "reason": "Unsupported file type"})
    elif is_supported_file(upload_path):
        candidate_paths.append(upload_path)
    else:
        skipped.append({"file": os.path.basename(upload_path), "reason": "Unsupported file type"})

    return candidate_paths, skipped


def build_response_counts(result_rows):
    return {f"{test_type}_count": len(rows) for test_type, rows in result_rows.items()}


@app.route('/upload', methods=['POST'])
def upload():
    try:
        files = request.files.getlist('file')
        if not files:
            return jsonify({'success': False, 'error': 'No file'}), 400

        test_types_json = request.form.get('test_types', json.dumps(DEFAULT_TEST_TYPES))
        selected_types = DEFAULT_TEST_TYPES.copy()
        selected_types.update(json.loads(test_types_json))

        result_rows = {test_type: [] for test_type in TEST_CONFIG}
        total_files = 0
        processed_files = 0
        skipped_files = []

        for uploaded_file in files:
            if not uploaded_file.filename:
                continue

            unique_name = f"{uuid.uuid4()}_{uploaded_file.filename}"
            upload_path = os.path.join(UPLOAD_DIR, unique_name)
            uploaded_file.save(upload_path)

            candidate_paths, skipped = get_candidate_paths(upload_path)
            skipped_files.extend(skipped)

            for candidate_path in candidate_paths:
                total_files += 1
                filename = os.path.basename(candidate_path)
                inferred_type = infer_type_from_path(candidate_path)

                try:
                    text = read_pdf_text(candidate_path) if candidate_path.lower().endswith('.pdf') else read_docx_text(candidate_path)
                except Exception as read_error:
                    skipped_files.append({"file": filename, "reason": f"Read error: {read_error}"})
                    continue

                detected_types = [inferred_type] if inferred_type else detect_types_from_text(text)
                if not detected_types:
                    skipped_files.append({"file": filename, "reason": "Could not detect test type"})
                    continue

                extracted_any_for_file = False

                try:
                    for test_type in detected_types:
                        if not selected_types.get(test_type, False):
                            continue

                        extractor = TEST_CONFIG[test_type]['extractor']
                        try:
                            row = extractor(text)
                            required_fields = TEST_CONFIG[test_type]['required_fields']
                            # Check if row has meaningful data (not just empty required fields)
                            if any(v for k, v in row.items() if k not in required_fields and v):
                                row['Source_PDF'] = filename
                                result_rows[test_type].append(row)
                                extracted_any_for_file = True
                            else:
                                # logging empty extraction as a skip reason if not already skipped
                                pass 
                        except Exception as ext_error:
                            print(f"Extraction error for {filename} ({test_type}): {ext_error}")
                            skipped_files.append({"file": filename, "reason": f"Extraction failed for {test_type}: {str(ext_error)}"})

                    if extracted_any_for_file:
                        processed_files += 1
                    elif not any(s['file'] == filename for s in skipped_files):
                         skipped_files.append({"file": filename, "reason": "No extractable values found"})
                except Exception as e:
                    print(f"Unexpected error processing {filename}: {e}")
                    skipped_files.append({"file": filename, "reason": f"Processing error: {str(e)}"})

        output_files = {}
        for test_type, config in TEST_CONFIG.items():
            if not selected_types.get(test_type, False):
                continue
            
            if not result_rows[test_type]:
                output_files[test_type] = 'N/A'
                output_files[f"{test_type}_excel"] = 'N/A'
                continue

            # CSV Output
            output_path = get_unique_filename(f"{OUTPUT_DIR}/{config['output_file']}")
            df = pd.DataFrame(result_rows[test_type])
            df.to_csv(output_path, index=False)
            output_files[test_type] = os.path.basename(output_path)
            
            # Excel Output
            excel_path = get_unique_filename(f"{OUTPUT_DIR}/{config['excel_output_file']}")
            df.to_excel(excel_path, index=False)
            output_files[f"{test_type}_excel"] = os.path.basename(excel_path)

        # Generate CSV for skipped/error files if any
        error_file = "N/A"
        if skipped_files:
            error_df = pd.DataFrame(skipped_files)
            error_path = get_unique_filename(f"{OUTPUT_DIR}/Processing_Errors.csv")
            error_df.to_csv(error_path, index=False)
            error_file = os.path.basename(error_path)

        report_path = get_unique_filename(f"{OUTPUT_DIR}/Processing_Report.json")
        with open(report_path, 'w', encoding='utf-8') as report_file:
            json.dump(
                {
                    'total_files': total_files,
                    'processed_files': processed_files,
                    'selected_types': selected_types,
                    'counts': build_response_counts(result_rows),
                    'skipped_files': skipped_files,
                    'output_files': output_files,
                    'error_file': error_file
                },
                report_file,
                indent=2,
            )

        shutil.rmtree(UPLOAD_DIR)
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        response_payload = {
            'success': True,
            'total_files': total_files,
            'processed_files': processed_files,
            'skipped_files': skipped_files,
            'skipped_count': len(skipped_files),
            'cbc_file': output_files.get('cbc', 'N/A'),
            'lft_file': output_files.get('lft', 'N/A'),
            'rft_file': output_files.get('rft', 'N/A'),
            'tft_file': output_files.get('tft', 'N/A'),
            'cbc_file_excel': output_files.get('cbc_excel', 'N/A'),
            'lft_file_excel': output_files.get('lft_excel', 'N/A'),
            'rft_file_excel': output_files.get('rft_excel', 'N/A'),
            'tft_file_excel': output_files.get('tft_excel', 'N/A'),
            'error_file': error_file,
            'report_file': os.path.basename(report_path),
        }
        response_payload.update(build_response_counts(result_rows))

        return jsonify(response_payload)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 500


@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(os.path.join(OUTPUT_DIR, filename), as_attachment=True)
    except Exception as e:
        return jsonify({'error': str(e)}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5000)

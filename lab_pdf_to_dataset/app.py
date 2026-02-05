from flask import Flask, request, jsonify
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
        "result_key": "cbc_count",
        "output_file": "CBC_Dataset.csv",
        "required_fields": ["Name", "Age", "Gender", "Source_PDF"],
    },
    "lft": {
        "detector_keywords": ["liver function", "bilirubin", "sgpt", "sgot", "alt", "ast"],
        "extractor": extract_lft,
        "result_key": "lft_count",
        "output_file": "LFT_Dataset.csv",
        "required_fields": ["Name", "Age", "Gender", "Source_PDF"],
    },
    "rft": {
        "detector_keywords": ["renal function", "kidney", "creatinine", "urea", "bun"],
        "extractor": extract_rft,
        "result_key": "rft_count",
        "output_file": "RFT_Dataset.csv",
        "required_fields": ["Name", "Age", "Gender", "Source_PDF"],
    },
    "tft": {
        "detector_keywords": ["thyroid", "tsh", "t3", "t4", "ft3", "ft4"],
        "extractor": extract_tft,
        "result_key": "tft_count",
        "output_file": "TFT_Dataset.csv",
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

        for uploaded_file in files:
            if not uploaded_file.filename:
                continue

            unique_name = f"{uuid.uuid4()}_{uploaded_file.filename}"
            upload_path = os.path.join(UPLOAD_DIR, unique_name)
            uploaded_file.save(upload_path)

            candidate_paths = []
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
            elif is_supported_file(upload_path):
                candidate_paths.append(upload_path)

            for candidate_path in candidate_paths:
                total_files += 1
                filename = os.path.basename(candidate_path)
                inferred_type = infer_type_from_path(candidate_path)

                try:
                    if candidate_path.lower().endswith('.pdf'):
                        text = read_pdf_text(candidate_path)
                    else:
                        text = read_docx_text(candidate_path)
                except Exception as read_error:
                    print(f"Error reading {filename}: {read_error}")
                    continue

                detected_types = [inferred_type] if inferred_type else detect_types_from_text(text)
                if not detected_types:
                    continue

                extracted_any_for_file = False

                for test_type in detected_types:
                    if not selected_types.get(test_type, False):
                        continue

                    extractor = TEST_CONFIG[test_type]['extractor']
                    row = extractor(text)
                    required_fields = TEST_CONFIG[test_type]['required_fields']
                    if any(v for k, v in row.items() if k not in required_fields):
                        row['Source_PDF'] = filename
                        result_rows[test_type].append(row)
                        extracted_any_for_file = True

                if extracted_any_for_file:
                    processed_files += 1

        output_files = {}
        for test_type, config in TEST_CONFIG.items():
            if selected_types.get(test_type, False):
                output_path = get_unique_filename(f"{OUTPUT_DIR}/{config['output_file']}")
                pd.DataFrame(result_rows[test_type]).to_csv(output_path, index=False)
                output_files[test_type] = os.path.basename(output_path)
            else:
                output_files[test_type] = 'N/A'

        shutil.rmtree(UPLOAD_DIR)
        os.makedirs(UPLOAD_DIR, exist_ok=True)

        return jsonify({
            'success': True,
            'total_files': total_files,
            'processed_files': processed_files,
            'cbc_count': len(result_rows['cbc']),
            'lft_count': len(result_rows['lft']),
            'rft_count': len(result_rows['rft']),
            'tft_count': len(result_rows['tft']),
            'cbc_file': output_files['cbc'],
            'lft_file': output_files['lft'],
            'rft_file': output_files['rft'],
            'tft_file': output_files['tft'],
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)

# Lab-PDF-To-Dataset

Developed by **Paksa IT Solutions**

## Overview
Lab-PDF-To-Dataset is an intelligent data extraction system that automatically converts medical laboratory test reports (PDF and Word documents) into structured, machine-readable CSV and Excel datasets. This tool eliminates the tedious manual data entry process and provides clean, ready-to-use datasets for analysis and research.

## Problem It Solves
Medical lab reports are typically stored as unstructured PDF or Word documents, making it extremely difficult to:
- Extract data for analysis
- Build datasets for machine learning models
- Conduct statistical research
- Perform comparative studies across multiple patients

Our system automates this entire process, converting hundreds of lab reports into structured datasets in minutes.

## Key Features
- **Multi-Format Support**: Extract data from PDF (text-based and scanned) and Word documents (.doc, .docx)
- **OCR Capabilities**: Automatically detects scanned PDFs and uses OCR (Tesseract) to extract text.
- **Multiple Test Types**: Supports CBC (Complete Blood Count), LFT (Liver Function Test), RFT (Renal Function Test), and TFT (Thyroid Function Test)
- **Dual Output**: Generates both **CSV** and **Excel (.xlsx)** datasets.
- **Batch Processing**: Upload ZIP files containing multiple reports for bulk processing
- **Robust Error Handling**: Skips problematic files without stopping the batch, logging errors to a dedicated CSV report.
- **Web Interface**: User-friendly React-based frontend with progress tracking and direct downloads.
- **Accurate Extraction**: Smart regex patterns to extract actual test results, avoiding ranges and dates.

## Benefits for Students

### 1. **Academic Research Projects**
   - Quickly build datasets for medical informatics projects
   - Analyze health trends across patient demographics
   - Complete assignments requiring real-world medical data

### 2. **Learning Data Processing**
   - Understand how unstructured data (including scanned images) is converted to structured formats
   - Learn about regex patterns, OCR, and text extraction techniques
   - Study the architecture of full-stack applications (Flask + React)

### 3. **Final Year Projects**
   - Use generated datasets for machine learning projects
   - Build predictive models for disease diagnosis
   - Create health analytics dashboards

## Benefits for Data Scientists

### 1. **Rapid Dataset Creation**
   - Convert thousands of lab reports into analysis-ready datasets in minutes
   - eliminate weeks of manual data entry work
   - Focus on analysis rather than data collection

### 2. **High-Quality Data**
   - **Excel Export**: Get data in a format ready for immediate analysis in Excel, pandas, or other tools.
   - **Error Logging**: detailed `Processing_Errors.csv` helps identify data quality issues source files.
   - **Consistent Formatting**: Standardized columns across all extracted files.

### 3. **Machine Learning Applications**
   - Build predictive models for disease detection
   - Train classification algorithms for abnormal test results
   - Develop patient risk assessment systems

## Installation

### Prerequisites
1. **Python 3.8+**
2. **Node.js 14+**
3. **Tesseract OCR** (For scanned PDFs):
   - **Windows**: [Download Installer](https://github.com/UB-Mannheim/tesseract/wiki) (Add to PATH)
   - **Linux**: `sudo apt install tesseract-ocr`
   - **Mac**: `brew install tesseract`
4. **Poppler** (For PDF-to-Image conversion):
   - **Windows**: [Download Release](https://github.com/oschwartz10612/poppler-windows/releases) (Add `bin` folder to PATH)
   - **Linux**: `sudo apt install poppler-utils`
   - **Mac**: `brew install poppler`

### Backend Setup
```bash
cd lab_pdf_to_dataset
pip install -r requirements.txt
python app.py
```

### Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

## Usage

1. **Start the Backend**: Run `python app.py` (Flask server on port 5000)
2. **Start the Frontend**: Run `npm run dev` (React app on port 5173)
3. **Upload Files**: 
   - Single or Multiple PDF/Word files (Text or Scanned)
   - ZIP archive containing multiple reports
4. **Select Test Types**: Check boxes for CBC, LFT, RFT, or TFT.
5. **Download Results**: 
   - Download **CSV** or **Excel** datasets directly from the UI.
   - Download **Error Log** if any files failed.

## Output Format

### CBC Dataset Columns
`Name, Age, Gender, HB, RBC, HCT, MCV, MCH, MCHC, Platelets, WBC, Neutrophils, Lymphocytes, Monocytes, Eosinophils, ESR, Source_PDF`

### LFT Dataset Columns
`Name, Age, Gender, Total Bilirubin, Direct Bilirubin, Indirect Bilirubin, ALT, AST, ALP, Albumin, Total Protein, Source_PDF`

### RFT Dataset Columns
`Name, Age, Gender, Urea, BUN, Creatinine, GFR, Uric Acid, Source_PDF`

### TFT Dataset Columns
`Name, Age, Gender, T3, T4, TSH, Free T3, Free T4, Source_PDF`

---

**Developed by Paksa IT Solutions**  
© 2026 Paksa IT Solutions. All rights reserved.


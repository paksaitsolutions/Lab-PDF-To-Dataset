# Lab-PDF-To-Dataset

Developed by **Paksa IT Solutions**

## Overview
Lab-PDF-To-Dataset is an intelligent data extraction system that automatically converts medical laboratory test reports (PDF and Word documents) into structured, machine-readable CSV datasets. This tool eliminates the tedious manual data entry process and provides clean, ready-to-use datasets for analysis and research.

## Problem It Solves
Medical lab reports are typically stored as unstructured PDF or Word documents, making it extremely difficult to:
- Extract data for analysis
- Build datasets for machine learning models
- Conduct statistical research
- Perform comparative studies across multiple patients

Our system automates this entire process, converting hundreds of lab reports into structured datasets in minutes.

## Key Features
- **Multi-Format Support**: Extract data from both PDF files and Word documents (.doc, .docx)
- **Multiple Test Types**: Supports CBC (Complete Blood Count), LFT (Liver Function Test), and RFT (Renal Function Test)
- **Batch Processing**: Upload ZIP files containing multiple reports for bulk processing
- **Web Interface**: User-friendly React-based frontend for easy file uploads
- **Accurate Extraction**: Smart regex patterns to extract actual test results (not normal ranges)
- **Structured Output**: Generates clean CSV files with consistent column formats
- **Auto-Versioning**: Automatically creates new versions (dataset_1, dataset_2) to prevent overwriting

## Benefits for Students

### 1. **Academic Research Projects**
   - Quickly build datasets for medical informatics projects
   - Analyze health trends across patient demographics
   - Complete assignments requiring real-world medical data

### 2. **Learning Data Processing**
   - Understand how unstructured data is converted to structured formats
   - Learn about regex patterns and text extraction techniques
   - Study the architecture of full-stack applications

### 3. **Final Year Projects**
   - Use generated datasets for machine learning projects
   - Build predictive models for disease diagnosis
   - Create health analytics dashboards

### 4. **Skill Development**
   - Gain hands-on experience with Python, Flask, and React
   - Learn about PDF/Word document processing
   - Understand data pipeline development

## Benefits for Data Scientists

### 1. **Rapid Dataset Creation**
   - Convert thousands of lab reports into analysis-ready datasets in minutes
   - Eliminate weeks of manual data entry work
   - Focus on analysis rather than data collection

### 2. **Machine Learning Applications**
   - Build predictive models for disease detection
   - Train classification algorithms for abnormal test results
   - Develop patient risk assessment systems
   - Create recommendation systems for medical diagnostics

### 3. **Healthcare Analytics**
   - Perform statistical analysis on patient populations
   - Identify correlations between different test parameters
   - Study disease patterns and trends
   - Generate insights for clinical decision support

### 4. **Research & Publications**
   - Quickly prepare datasets for medical research papers
   - Conduct retrospective studies on patient data
   - Validate hypotheses with real-world medical data
   - Collaborate with healthcare institutions on data-driven research

### 5. **Time & Cost Efficiency**
   - Reduce data preparation time by 95%
   - Lower project costs by eliminating manual data entry
   - Scale data collection efforts effortlessly

## Use Cases

1. **Medical Research**: Analyze lab test trends across patient demographics
2. **Disease Prediction**: Build ML models to predict diseases based on lab values
3. **Health Monitoring**: Track patient health metrics over time
4. **Clinical Studies**: Prepare datasets for retrospective clinical research
5. **Educational Projects**: Create datasets for teaching data science in healthcare
6. **Hospital Analytics**: Generate insights from historical lab data

## Tech Stack
- **Backend**: Python Flask (REST API)
- **Frontend**: React + Vite (Modern UI)
- **PDF Processing**: pdfplumber (Text extraction)
- **Word Processing**: python-docx, pywin32 (Support for .doc and .docx)
- **Data Export**: pandas (CSV generation)
- **Pattern Matching**: Regular expressions (Accurate data extraction)

## Installation

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
   - Single PDF/Word file
   - Multiple files
   - ZIP archive containing multiple reports
4. **Organize by Test Type**: Place files in folders named `cbc`, `lft`, or `rft`
5. **Download Results**: CSV files are generated in the `output/` folder

## Output Format

### CBC Dataset Columns
`Name, Age, Gender, HB, RBC, HCT, MCV, MCH, MCHC, Platelets, WBC, Neutrophils, Lymphocytes, Monocytes, Eosinophils, ESR, Source_PDF`

### LFT Dataset Columns
`Name, Age, Gender, Total Bilirubin, Direct Bilirubin, Indirect Bilirubin, ALT, AST, ALP, Albumin, Total Protein, Source_PDF`

### RFT Dataset Columns
`Name, Age, Gender, Urea, BUN, Creatinine, GFR, Uric Acid, Source_PDF`

## Example Workflow

1. Collect 1000 CBC lab reports (PDF/Word)
2. Organize them in a folder named `cbc`
3. Create a ZIP file
4. Upload via web interface
5. Receive `CBC_Dataset.csv` with 1000 rows of structured data
6. Import into Python/R for analysis
7. Build ML models or perform statistical analysis

## Future Enhancements
- Support for more test types (Lipid Profile, Thyroid Function, etc.)
- OCR support for scanned documents
- Data visualization dashboard
- API endpoints for programmatic access
- Cloud deployment for scalability

---

**Developed by Paksa IT Solutions**  
© 2026 Paksa IT Solutions. All rights reserved.


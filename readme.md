# Data Profiler

A Flask-based web application for generating automated data profiling reports using YData Profiling.

**Checkout here** → [Data-Profiler](https://data-profiler.onrender.com)

## Features

- **File Upload Support**: Upload CSV, XLS, and XLSX files
- **Intelligent Report Generation**: 
  - Files smaller than 100 MB: Generates full explorative reports
  - Files 100 MB or larger: Generates minimal reports for faster processing
- **Dynamic Report Naming**: Reports are named based on the uploaded file (e.g., `data.csv` → `data_report.html`)
- **Report Download**: Download generated reports with auto-redirect functionality

## File Size Thresholds

| File Size | Report Type | Settings |
|-----------|------------|----------|
| < 100 MB | Full Explorative | `explorative=True, minimal=False` |
| ≥ 100 MB | Minimal | `explorative=False, minimal=True` |

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python app.py`

## Supported File Formats

- CSV (.csv)
- Excel (.xls, .xlsx)

## Usage

1. Upload a data file via the web interface
2. The app automatically generates a profiling report based on file size
3. Download the generated report by clicking the download button

## Project Structure

```
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Web interface
├── uploads/               # Uploaded files and generated reports
└── readm.md              # This file
```

import os
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from ydata_profiling import ProfileReport

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config["UPLOAD_FOLDER"] = "uploads"

# Ensure upload folder exists
if not os.path.exists(app.config["UPLOAD_FOLDER"]):
    os.makedirs(app.config["UPLOAD_FOLDER"])

# Allowed extensions
ALLOWED_EXTENSIONS = {"csv", "xls", "xlsx"}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def read_file(filepath):
    """Read file based on extension"""
    ext = filepath.rsplit(".", 1)[1].lower()
    if ext == "csv":
        return pd.read_csv(filepath)
    elif ext in ["xls", "xlsx"]:
        return pd.read_excel(filepath)
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        # ✅ Check if file exists in request
        if "file" not in request.files:
            flash("❌ No file uploaded!", "danger")
            return redirect(request.url)

        file = request.files["file"]
        
        # ✅ Check if file is selected
        if file.filename == "":
            flash("⚠️ No file selected. Please choose a file.", "warning")
            return redirect(request.url)

        # ✅ Validate file extension before saving
        if not allowed_file(file.filename):
            flash("❌ Unsupported file format! Upload a CSV or Excel file.", "danger")
            return redirect(request.url)

        # ✅ Delete existing uploaded files before saving new one
        for f in os.listdir(app.config["UPLOAD_FOLDER"]):
            os.remove(os.path.join(app.config["UPLOAD_FOLDER"], f))

        # ✅ Save new file
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # ✅ Read file
        df = read_file(file_path)
        if df is None:
            flash("❌ Could not read file. Please upload a valid CSV or Excel file.", "danger")
            return redirect(request.url)

        # ✅ Generate profiling report
        report_path = os.path.join(app.config["UPLOAD_FOLDER"], "report.html")
        profile = ProfileReport(df, explorative=True)
        profile.to_file(report_path)

        # ✅ Flash success message
        flash("✅ Report generated successfully! Click 'Download Report' to get it.", "success")
        return redirect(url_for("download_report"))

    return render_template("index.html")

@app.route("/download")
def download_report():
    """Download the generated report"""
    report_path = os.path.join(app.config["UPLOAD_FOLDER"], "report.html")
    if os.path.exists(report_path):
        return redirect(report_path)
    flash("⚠️ No report available. Please upload a file first.", "warning")
    return redirect(url_for("upload_file"))

if __name__ == "__main__":
    app.run(debug=True)

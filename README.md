# 📂 Django + AWS S3 File Version Manager & Analyser

A full-stack Django application for uploading, versioning, analysing, and downloading files — backed by AWS S3.


## 🚀 Features

- 🔐 User authentication (signup/login/logout via Django Auth)
- 📤 Upload files to S3 using user-based paths (`username/filename`)
- 🔁 S3 versioning: list and download previous file versions
- 📊 CSV analysis:
  - View column names, shape, and top rows
  - Get per-column stats (mean, median, mode, etc.)
  - Plotly charts (numeric & date columns)
- 🧼 Minimal front-end using Bootstrap 5
- 🔒 Views protected

---


## 📦 Tech Stack

| Layer        | Technology               |
|--------------|---------------------------|
| **Backend**  | Django 5.x, Python 3.11+  |
| **Storage**  | AWS S3 (versioning enabled) |
| **Frontend** | HTML + Bootstrap 5        |
| **Data**     | Pandas, Plotly            |

---

## 📁 S3 Key Format

All uploaded files follow this structure:
username/filename.csv

---


🧪 How to Use
Follow these steps after launching the Django server:

1. 🔐 Sign Up / Log In
Navigate to the homepage

Create a new account or log in with an existing one

2. 📤 Upload a File
Click “Upload File”

Select a CSV or other file type

The file will be uploaded to S3 under username/filename

3. 📁 View Your Files
Click “View My Files”

Select a file to list all of its S3 versions

4. 📥 Download a Specific Version
Choose a version from the list

Download it with a versioned filename like file_Vabcd1234.csv

5. 📊 Analyze a File
Click “Analyze a File”

Choose a CSV you’ve uploaded

You’ll see:

Number of rows & columns

Column names

A preview of the first 3 rows

6. 📈 Drill Down into a Column
Pick a column from the dropdown

You’ll get:

📋 Stats: mean, median, std dev, top values, etc.

📉 Plotly Chart: histogram for numeric/date columns

All features are protected — you must be logged in to upload, download, or analyze files

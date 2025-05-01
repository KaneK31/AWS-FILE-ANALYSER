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


S3 versioning handles file history transparently.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/aws-file-manager.git
cd aws-file-manager


pip install -r requirements.txt

AWS_BUCKET_NAME=your-bucket-name
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key

python manage.py runserver


import os
import pandas as pd
from io import BytesIO
import plotly.express as px
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ..helpers.s3_helpers import bucket_name, s3_client, ensure_bucket_exists, check_key


@login_required()
def analysis_view(request):
    username = request.user.username
    prefix = f"{username}/"

    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files = []

    for obj in response.get("Contents", []):
        key = obj["Key"]
        if "csv" in key or "ods" in key:
            if "/" in key:
                files.append(key.split("/", 1)[1])

    if not files:
        return HttpResponse("❌ No PDF files found.")

    return render(request, "filemanager/analysis.html", {"files": files})


@login_required()
def analysis_csv(request):
    if request.method == "POST":
        file_key = request.POST.get("file_key")
        full_key = f"{request.user.username}/{file_key}"

        if not check_key(file_key, request.user.username):
            return HttpResponse("No such key")

        response = s3_client.get_object(Bucket=bucket_name, Key=full_key)

        try:
            df = pd.read_csv(BytesIO(response["Body"].read()), encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(BytesIO(response["Body"].read()), encoding="ISO-8859-1")

        return render(request, "filemanager/analysis_results.html", {
            "filename": file_key.split("/")[-1],
            "columns": df.columns,
            "shape": df.shape,
            "preview": df.head(3).to_html(classes="table table-striped", index=False)
        })
    return redirect("select_analysis")


@login_required()
def analysis_view_col(request):
    if request.method == "POST":
        col = request.POST.get("column")
        file_key = request.POST.get("file_key")

        response = s3_client.get_object(Bucket=bucket_name, Key=file_key)

        try:
            df = pd.read_csv(BytesIO(response["Body"].read()), encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(BytesIO(response["Body"].read()), encoding="ISO-8859-1")

        if col not in df.columns:
            return HttpResponse("Column not found")

        col_data = df[col].dropna()

        if pd.api.types.is_numeric_dtype(col_data):
            stats = col_data.describe().to_dict()
            fig = px.histogram(col_data, nbins=20, title=f"Distribution of '{col}'")
            plot_html = fig.to_html(full_html=False)
        elif pd.api.types.is_datetime64_any_dtype(col_data) or pd.to_datetime(col_data, errors='coerce').notna().all():
            col_data = pd.to_datetime(col_data, errors='coerce')
            stats = col_data.value_counts().head(10).to_dict()
            fig = px.histogram(col_data, nbins=20, title=f"Date Distribution of '{col}'")
            plot_html = fig.to_html(full_html=False)
        else:
            stats = col_data.value_counts().head(10).to_dict()
            plot_html = None

        return render(request, "filemanager/column_stats.html", {
            "column": col,
            "stats": stats,
            "plot_html": plot_html,
            "filename": os.path.basename(file_key),  # just filename.csv
            "file_key": file_key  # full path for hidden input
        })

    return redirect("select_analysis")

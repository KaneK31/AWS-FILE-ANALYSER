import os
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from ..helpers.s3_helpers import bucket_name, s3_client, ensure_bucket_exists, check_key


@login_required()
def upload_view(request):
    if ensure_bucket_exists():
        if request.method == "POST":
            file_obj = request.FILES.get("file")

            if file_obj:
                username = request.user.username
                original_name = file_obj.name
                s3_key = f"{username}/{original_name}"

                s3_client.upload_fileobj(
                    file_obj,
                    bucket_name,
                    s3_key,
                    ExtraArgs={"ContentType": file_obj.content_type}
                )
                return HttpResponse(f"✅ Uploaded as '{s3_key}'")
            return HttpResponse("❌ No file selected.")
        return render(request, "filemanager/upload.html")
    return HttpResponse("❌ Missing bucket.")


@login_required()
def select_file_view(request):
    username = request.user.username
    prefix = f"{username}/"

    response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    files = []

    for obj in response.get("Contents", []):
        key = obj["Key"]
        if "/" in key:
            files.append(key.split("/", 1)[1])

    return render(request, "filemanager/select_file.html", {"files": files})

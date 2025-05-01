import os
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ..helpers.s3_helpers import bucket_name, s3_client, ensure_bucket_exists, check_key

@login_required()
def list_versions(request):
    if request.method == "POST":
        file_key = request.POST.get("file_key")

        if not check_key(file_key):
            return HttpResponse("No such key")

        response = s3_client.list_object_versions(Bucket=bucket_name, Prefix=file_key)
        return render(request, "filemanager/list_versions.html", {
            "versions": response.get("Versions", []),
            "file_key": file_key
        })


@login_required()
def download_file(request):
    key = request.POST.get("file_key")
    version_id = request.POST.get("version_id")

    safe_filename = os.path.basename(key)
    ext = os.path.splitext(safe_filename)[-1]
    clean_name = os.path.splitext(safe_filename)[0]
    filename = f"{clean_name}_V{version_id[:8]}{ext}"

    with open(filename, 'wb') as data:
        s3_client.download_fileobj(
            Bucket=bucket_name,
            Key=key,
            Fileobj=data,
            ExtraArgs={"VersionId": version_id}
        )
    return HttpResponse("✅ Downloaded!")

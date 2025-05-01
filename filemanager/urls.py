from django.urls import path
from .views import (
    home_view,
    signup_view,
    upload_view,
    select_file_view,
    download_file,
    list_versions,
    analysis_view,
    analysis_csv,
    analysis_view_col
)

urlpatterns = [
    path("", home_view, name="home"),
    path("signup/", signup_view, name="signup"),
    path("upload/", upload_view, name="upload"),
    path("select-file/", select_file_view, name="select_file"),
    path("download/", download_file, name="download_file"),
    path("list-versions/", list_versions, name="list_versions"),
    path("analysis/", analysis_view, name="analysis"),
    path("analysis/csv/", analysis_csv, name="analysis_csv"),
    path("analysis/column/", analysis_view_col, name="analysis_col"),
]

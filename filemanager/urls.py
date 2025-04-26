from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # 🏠 home page
    path('signup/', views.signup_view, name='signup'),
    path('upload/', views.upload_view, name='upload'),
    path('versions/', views.list_versions, name='versions'),
    path('downloads/', views.download_file, name='download_version'),
    path('select/', views.select_file_view, name='select_file'),
    # Show the dropdown
    path('select_analysis/', views.analysis_view, name='select_analysis'),

    # Handle the CSV file POST
    path('analysis_csv/', views.analysis_csv, name='analyze_file'),
    path('analysis_view_col/', views.analysis_view_col, name='analysis_view_col'),

]

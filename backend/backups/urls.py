# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('dump/', views.DatabaseDumpView.as_view(), name='database_dump'),
    path('dump/api/tables/', views.GetTablesAPI.as_view(), name='get_tables'),
    path('dump/api/dump/', views.DumpDataAPI.as_view(), name='dump_data'),
    path('dump/download/', views.DownloadDumpView.as_view(), name='download_dump'),
]
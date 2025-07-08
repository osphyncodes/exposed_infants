from django.urls import path
from . import views

app_name = "tingathe_tools"

urlpatterns = [
    path('', views.index, name='tingathe_tools_index'),
]

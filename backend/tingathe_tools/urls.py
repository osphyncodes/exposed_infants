from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='tingathe_tools_index'),
]

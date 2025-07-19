"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from children.views import dashboard
from children.views import app_selector

urlpatterns = [
    path('admin/', admin.site.urls),
    path('children/', include('children.urls')),  # <--- updated to children app
    path('pact/', include('pact.urls')),  # <--- updated to pact app
    path('login/', auth_views.LoginView.as_view(template_name = 'registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('', app_selector, name='app_selector'),
    path('accounts/login/', app_selector, name="app_selector"),
    path('select-app/', app_selector, name='app_selector'),
    path('tingathe_tools/', include('tingathe_tools.urls')),
]
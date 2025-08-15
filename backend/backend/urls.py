from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from children.views import dashboard
from children.views import app_selector

urlpatterns = [
    path('admin/', admin.site.urls),
    path('exposed/', include('children.urls')),  # <--- updated to children app
    path('pact/', include('pact.urls')),  # <--- updated to pact app
    path('login/', auth_views.LoginView.as_view(template_name = 'registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('select-app/', app_selector, name='app_selector'),
    path('', app_selector, name='app_selector'),
    path('tingathe-tools/', include('tingathe_tools.urls', namespace='tingathe_tools')),
    path('art/', include('art.urls')),
    path('teen_club/', include('teen_club.urls')),
    path('select2/', include('django_select2.urls')),
    path('tracing/', include('tracing.urls'))
]
"""
URL configuration for music_store_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path,include
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from music import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('music/', include('music.urls')),
    path('', TemplateView.as_view(template_name='base_generic.html'), name='home'),

    path('login/', auth_views.LoginView.as_view(), name='login'),  # تسجيل الدخول
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # تسجيل الخروج


    # مسارات API للتسجيل وتسجيل الدخول
    path('api/signup/', views.signup, name='api_signup'),  # مسار التسجيل API
    path('api/login/', views.login_view, name='api_login'),  # مسار تسجيل الدخول API
    path('api/', include('music.api_urls')),
]

if settings.DEBUG:  # قم بتعريف هذا فقط في وضع التطوير
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
